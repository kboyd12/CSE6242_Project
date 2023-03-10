# CSE6242_Project
Team Project for CSE6242

# How to use
NOTE: should be updated as changes are pushed.
Only thing to so far is 
Create virtual environment (should only need to do once):
$`python -m venv ./venv`  (or `python3`)

Activate virutal environment (do each session)
$`source ./venv/Scripts/activate`

install packages (do at start, and when requirements.txt changes)
$`pip install -r ./requirements.txt`

# Project Structure:
.
├── .gitignore
├── README.md
├── data
│   ├── processed       cleaned data ready for visualization
│   └── raw             raw data files
├── requirements.txt    
├── src                 code
│    ├── __init__.py
│    ├── EDA            code to do exploratory stuff
│    ├── data           code to pull/clean data
│    ├── model          ml models etc.
│    └── viz            code to visualize data
└── tests               tests    
