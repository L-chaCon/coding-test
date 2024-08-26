## Octavio Montt Tails Task
### Instructions of use
1. Clone the Repository
If you are not extracting it from a ZIP file, clone the repository using:
```
git clone https://github.com/L-chaCon/coding-test.git octavio-task
```
2. Build and Run the Docker Image
Navigate to the project folder, build the Docker image, and run it:
```
cd octavio-task
docker build . --tag octavio-task
docker run -p 42069:42069 -d octavio-task
```
3. Access the Application
To view the application, go to [Welcome Page](http://127.0.0.1:42069/)
4. Update the data
Go to [store](http://127.0.0.1:42069/stores) and click the [clean database](http://127.0.0.1:42069/stores/clean) link. This take a bit(I'm sorry). To set the Latitude and Longitude run the [calculate latitude and longitude](http://127.0.0.1:42069/stores/calculate_lat_long).

### Considerations
- **Postcode Formatting:** One postcode in `store.json` is not in the same format as required by the API. I created a function to clean the database and align it with the API’s format to get the latitude and longitude information. I opted for a function rather than modifying the JSON file directly, as it provides a more general solution. However, this function can be quite slow.
- **Latitude and Longitude Calculation:**  I left the latitude and longitude calculation to the user to demonstrate how the functionality works. This means that the user is starting with a frech database each time. This is not optimal, but is just to show how it works.
- **API Limitations:** Towards the end of the task, I realized that the approach I took was limited by the API’s constraints. The API has a very low distance limit (130 meters) for POST requests with a radius. I left the initial code with a note explaining the approach taken.

## P.S.
Thank you for exploring this project! Forgive my spelling errors, and I hope you have fun.
