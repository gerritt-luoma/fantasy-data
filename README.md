# Fantasy Football Data Project

## Intentions
- I want to use this as a project to add to whenever I get that random inspiration.
- This will keep my python skills more up to date and won't allow them to get quite as rusty.
- I will use python notebooks for initially testing out my code but will then refactor it into proper divided modules.
- Maybe turn this into a CLI?  Or I could use it as a back end.

## Plan
1. Using the `schedule` library I want to have a scraper run on the ESPN weekly football scores.
2. With these scores, I will scrape each game for each players accrued statistics from the box score
3. These will be parsed and stored in my local mongo db server to be accessed in a node application
## Setup
1. This project is coded using `Python 3.10.5`.  Visit the [Python download page](https://www.python.org/downloads/) to install the correct version or use your installed python versioning tool to switch to this version.
2. For best results, use a python virtual environment (optional)
   ```
   $ python3 -m pip3 install --user virtualenv
   $ python3 -m virtualenv <envirnoment name of your choice>
   $ source <env name>/bin/activate
   ```
3. Install all needed dependencies
   ```
   $ python -m pip install -r requirements.txt
   ```
4. If running testing notebooks, there may be some unaccounted for steps depending on your machine.  I am using VSCode with the Jupyter notebooks extension so I am able to select my virtual environment as my interpreter.