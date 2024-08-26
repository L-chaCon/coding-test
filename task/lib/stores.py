import math

import requests

from task.models.stores import (Stores, get_stores,
                                update_lat_long_stores_in_bulk,
                                update_postcode_stores_in_bulk)


def get_lat_long_for_postcodes(postcodes: list = []) -> dict[str, tuple]:
    """
    By default search for all stores in the database. You can give a list
    of postcodes and is going to build the dictionary with thoes ones
    """
    postcode_map = {}
    postcodes_list = []
    if not postcodes:
        stores = get_stores()
        for store in stores:
            postcodes_list.append(store.postcode)
    else:
        postcodes_list = postcodes
    url = "https://api.postcodes.io/postcodes"
    paylode = {"postcodes": postcodes_list}
    response = requests.post(url, json=paylode)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 200:
            for item in data.get('result'):
                if not item.get('result'):
                    postcode_map[item.get('query')] = (None, None)
                else:
                    postcode_response = item.get('result')
                    postcode_map[postcode_response['postcode']] = (postcode_response['latitude'], postcode_response['longitude'])
        else:
            raise ValueError(f"{data.get('error')}")
    else:
        raise Exception(f"Failed to get data from Postcodes.io API. Status code: {response.status_code}")
    return postcode_map


def get_result_info_for_one_store(store: Stores) -> dict:
    url = f"https://api.postcodes.io/postcodes/{store.postcode}"
    response = requests.get(url)
    result = {}
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 200:
            result = data.get('result')
        else:
            raise ValueError(f"{data.get('error')}")
    else:
        result['error'] = f"status code: {response.status_code} - {response.json()['error']}"
    return result


def clean_postcode_in_database(postcodes: list = []) -> bool:
    stores = get_stores(postcodes)
    update_data = []
    data_updated = False
    for store in stores:
        postcode_info = get_result_info_for_one_store(store)
        if postcode_info.get('error'):
            continue
        if postcode_info['postcode'] != store.postcode:
            store_data = {}
            store_data['id'] = store.id
            store_data['postcode'] = postcode_info['postcode']
            update_data.append(store_data)
    if update_data:
        try:
            update_postcode_stores_in_bulk(update_data)
            data_updated = True
        except:
            # NOTE: This can be a log
            print("Not able to clean database")
    return data_updated


def update_lat_long_of_stores(postcodes: list = []) -> bool:
    stores = get_stores(postcodes)
    update_data = []
    data_updated = False
    try:
        postcode_lat_long_map = get_lat_long_for_postcodes(postcodes)
    except Exception as e:
        raise Exception(e)
    for store in stores:
        store_data = {}
        store_data['id'] = store.id
        store_data['latitude'] = postcode_lat_long_map[store.postcode][0]
        store_data['longitude'] = postcode_lat_long_map[store.postcode][1]
        update_data.append(store_data)
    try:
        update_lat_long_stores_in_bulk(update_data)
        data_updated = True
    except:
        # NOTE: This can be Loged
        print("Not able to update lat long")
    return data_updated

# NOTE: This was my first aproach but realiced that the limit of radius was 150 meters.
# so there were just one store in the radius all the time
#
# def stores_in_poscode_radius(postcode: str, radius: float) -> list[Stores]:
#     try:
#         postcode_lat_long_map = get_lat_long_for_postcodes([postcode])
#         lat = postcode_lat_long_map[postcode][0]
#         long = postcode_lat_long_map[postcode][1] 
#     except:
#         raise Exception()
#     postcode_list = []
#     url = "https://api.postcodes.io/postcodes"
#     paylode = {
#         "geolocations" : [{
#             "longitude": long,
#             "latitude": lat,
#             "radius": radius
#         }]
#     }
#     response = requests.post(url, json=paylode)
#     if response.status_code == 200:
#         data = response.json()
#         if data.get('status') == 200:
#             result = data.get('result')[0]
#             geodata_list = result.get('result')
#             for item in geodata_list:
#                 postcode_list.append(item['postcode'])
#         else:
#             raise ValueError(f"{data.get('error')}")
#     else:
#         raise Exception(f"Failed to get data from Postcodes.io API. Status code: {response.status_code}")
#
#     if postcode_list:
#         stores = get_stores(postcode_list)
#         if stores:
#             sorted_stores = sort_stores_north_to_south(stores)
#             return sorted_stores
#     return []


def haversine(lat_1: float, long_1: float, lat_2: float, long_2: float) -> float:
    lat_1 = math.radians(lat_1)
    long_1 = math.radians(long_1)
    lat_2 = math.radians(lat_2)
    long_2 = math.radians(long_2)

    # Haversine formula
    delta_lat = lat_2 - lat_1
    delta_long = long_2 - long_1
    a = math.sin(delta_lat / 2)**2 + math.cos(lat_1) * math.cos(lat_2) * math.sin(delta_long / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    r = 6371.0
    distance = r * c
    return distance


def stores_in_poscode_radius(postcode: str, radius: float) -> list[Stores]:
    try:
        postcode_lat_long_map = get_lat_long_for_postcodes([postcode])
        lat_of_postcode = postcode_lat_long_map[postcode][0]
        long_of_postcode = postcode_lat_long_map[postcode][1] 
    except:
        raise Exception()

    stores_in_radius = []
    stores = get_stores()
    for store in stores:
        store_lat = store.latitude
        store_long = store.longitude
        if store_lat and store_long:
            distance_to = haversine(lat_of_postcode, long_of_postcode, store_lat, store_long)
            if distance_to <= radius:
                stores_in_radius.append(store)
        else:
           # NOTE: This can be Loged
            print("Not able to update lat long")
 
    if stores_in_radius:
        sorted_stores = sort_stores_north_to_south(stores_in_radius) 
        return sorted_stores
    return []

