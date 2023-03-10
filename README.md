# CSE6242_Project
Team Project for CSE6242

# How to use
NOTE: should be updated as changes are pushed.

### Setup
Create virtual environment (should only need to do once):  
$`python -m venv ./venv`  (or `python3`)  

Activate virutal environment (do each session)  
$`source ./venv/Scripts/activate`  

install packages (do at start, and when requirements.txt changes)  
$`pip install -r ./requirements.txt`  

### get data:
#### Note on kaggle api use:
```
In order to use the Kaggle’s public API, you must first authenticate using an API token. From the site header, click on your user profile picture, then on “My Account” from the dropdown menu. This will take you to your account settings at https://www.kaggle.com/account. Scroll down to the section of the page labelled API:

To create a new token, click on the “Create New API Token” button. This will download a fresh authentication token onto your machine.

If you are using the Kaggle CLI tool, the tool will look for this token at ~/.kaggle/kaggle.json on Linux, OSX, and other UNIX-based operating systems, and at C:\Users<Windows-username>.kaggle\kaggle.json on Windows. If the token is not there, an error will be raised. Hence, once you’ve downloaded the token, you should move it from your Downloads folder to this folder.
```
Once you have the json file in place, from root of project run:  
$`python ./src/data/get_data.py`  
it may take a few minutes due to file size.  



# Project Structure:
.
├── .gitignore  
├── README.md  
├── data  
│   ├── processed       cleaned data ready for visualization  
│   └── raw             raw data files  
├── requirements.txt      
├── src                 code  
│    ├── EDA            code to do exploratory stuff  
│    ├── data           code to pull/clean data  
│    ├── model          ml models etc.  
│    └── viz            code to visualize data  
└── tests               tests      
