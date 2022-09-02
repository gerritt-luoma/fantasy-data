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
- [ ] Add headers to requests to better mock an actual user/computer
- [ ] Continue building out the scraper
- [ ] Clean up requirements.txt to remove any unnecessary modules.  Right now I am installing things like the python notebook kernel in the docker container which is very unnecessary
## Setup
1. Clone this repository and cd into the directory
2. To run this project it is recommended to use Docker.  After installing the Docker desktop application or docker on the CLI, run:
   ```
   $ docker build -t fantasy-data-scraper .
   ```
3. Once the build completes, run the container
   ```
   $ docker run fantasy-data-scraper
   ```