# TMDB Visualisation Project

This project is a cool little collection of scripts that interact with The Movie Database (TMDB) API in order to create a dashboard of data visualisations that show users some interesting information about the dataset.

## Installation and Setup
Initially you will want to clone this repository and make sure that at least version 3.14.4 of [Python](https://www.python.org/downloads/) is installed on your machine.

Once that is done, you should set up a python virtual environment and install the project's dependencies using the following command:
```
pip install -r requirements.txt
```
After this you will need to get a TMDB API key, which you can request via this [link](https://developer.themoviedb.org/docs/getting-started)

You should then set up an environment variable `API_KEY` which should be assigned to your specific API key.

Once that is done, you can run the dashboard using the following command:
```
python src/app.py
```
Then access the local host link, and check out the dashboard!
