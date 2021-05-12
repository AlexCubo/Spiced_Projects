# This project is a team work of Alessandro Cubeddu, Laurin Brinkmann and Marco Arent (2021)

## project structure
- `data`
    - `raw`: place to store all data sources as we get them
    - `processed`: place to store data after we did some wrangling and tranformation
    - 'output': place the final csv file produced by the simulationto store 
- `src`: python code that we run to do all the magic (imagine this folder to be the place for out production code)
		- clean.py: load the csv from raw and make data wrangling
		- probability_matrix.py: calculate the markov chain for the supermarket problem
		- classes.py: contains the Supermaket_map class, Customer class and Doodlemarket class 
				This file is also used as main to run the main simulation after cleaning and
				after the calculation of probability matrix

## Usage:
- first, run cleanup.py --> $ python cleanup.py : This pupulates the data/processed
- second, run classes.py --> $ python classes.py : This populates data/output and makes the magic (displays the market with customers)
- third, quit the app pressing "q"
