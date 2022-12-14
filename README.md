# Fantasy Football Data Project

## Intentions
- I want to use this as a project to add to whenever I get that random inspiration.
- This will keep my python skills more up to date and won't allow them to get quite as rusty.
- I will use python notebooks for initially testing out my code but will then refactor it into proper divided modules.
- Use this application only to scrape the data.  I will build out an API using express and Typescript to handle working with the mongodb server which the scraper will then send post requests to.

## Plan
1. Using the `schedule` library I want to have a scraper run on the PFR weekly football scores.
   1. Using PFR will be very useful.  This is because they have basic stats as well as advanced stats like ADOT and air yards
   2. This is also useful because they don't hide their data like ESPN making it much easier to scrape.
2. With these scores, I will scrape each game for each players accrued statistics from the box score
3. These will be parsed and stored in my local mongo db server to be accessed in a node application

## TODO
- [ ] Improve logging to not include requests library debug logs (set them to warning or greater). The fix I initially tried did not work.
- [ ] Refactor RequestUtils.py to use a session and a class approach.  Create a session with the site and then use get for all remaining requests
- [ ] Think of way to inform me of if there was a scraping error?  Like send me an email or a message or something?
- [ ] Clean up requirements.txt to remove any unnecessary modules.  Right now I am installing things like the python notebook kernel in the docker container which is very unnecessary
- [x] **ADD THE WEEK TO THE PLAYERS**
- [x] Alter scraping to be just one list of objects to add en masse.  This will make querying much easier.  This means I will need to include the team abbreviation in player info.  Get rid of week subcollections and just have a collection for each year
- [x] Refactor DBUtils.py to take a class approach.  This way I can connect **ONCE** before scraping instead of connecting every time I try to write to the db.
- [x] Should set up actual logging
- [x] Alter scraping to only add fields that contain values.  (Ex. Wide receivers that don't have passing stats should not have passing data stored)
- [x] Fix dotenv not loading user and password from .env in docker container
- [x] Fix port binding connection between mongodb and container on rpi
- [x] Continue building out the scraper
- [x] Add headers to requests to better mock an actual user/computer
- [x] Find way to easily determine which week of the season it is
## Setup
1. Clone this repository and cd into the directory
2. To run this project it is recommended to use Docker.  After installing the Docker desktop application or docker on the CLI, run:
   ```
   $ docker build -t fantasy-data-scraper .
   ```
3. Once the build completes, run the container
   ```
   $ docker run -d --restart always --add-host=mongoservice:172.17.0.1 -v ~/logs:/usr/logs/ fantasy-data-scraper
   ```
