import pytest
from task.lib.stores import (get_lat_long_for_postcodes,
                             stores_in_poscode_radius)


class TestStoresLib():
    @pytest.mark.parametrize("postcode, expected", [
        (["RM9 6SJ"], {"RM9 6SJ": (51.530577, 0.145621)}), 
        (["RM9 6SJ", "SW20 0JQ"], {"RM9 6SJ": (51.530577, 0.145621), "SW20 0JQ": (51.405047, -0.238151)}),
        (["GU19 5DG", "TN23 7DH" ], {"GU19 5DG": (None, None), "TN23 7DH": (51.135177, 0.870721)})
    ])
    def test_get_lat_long_for_postcodes(self, app, postcode, expected):
        with app.app_context():
            postcodes_with_lat = get_lat_long_for_postcodes(postcode)
            assert expected == postcodes_with_lat


    @pytest.mark.parametrize("postcode, radius,expected", [
        ("RM9 6SJ", 0, ["RM9 6SJ"]), 
    ])
    def test_stores_in_poscode_radius(self, app, postcode, radius, expected):
        with app.app_context():
            list_of_stores = stores_in_poscode_radius(postcode, radius)
            postcodes_of_stores = [store.postcode for store in list_of_stores] 
            assert expected == postcodes_of_stores
