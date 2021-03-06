# SI507-FinalProject

#### 3 milestones:
- Project Proposal, due March 22
- Data Checkpoint & Interactive Presentation Design, due April 12
- Final Project Demo and Repository Link Submission, due April 26


#### Goals of Project:
- Access data from the web
- Use advanced data structures and operations to analyze and process data in 
"interesting" ways
- Use a presentation tool or framework to present data to a user
- Support basic interactivity by allowing a user to choose among different 
data presentation options

#### Package Requirements:
- requests
- xmltodict
- webbrowser

#### Files: 
- **Final_Proj_API.py** 
  > Python File with code for accessing Board Game 
Geek's API and reading the data from XML to json in order to clean and 
parse the data. Then, the json objects are written to a json file. 
- **bgg_list.json** 
  > The final file created by the code in 
Final_Proj_API.py.
- **hot_boardgames.json** 
  > Test json file used as initial example for 
figuring our the process of writing xmltodict and then saving that dict to 
json.
- **Final_Proj_Tree.py** 
  > Code for reading in the bgg_list.json file, 
parsing 
the data based on the outline of the tree structure and user 
question/answer flow, then loading that data into the tree structure. This 
file also include the control flow for interacting with the user and 
displaying necessary game information based on their answers to the 
computer's questions. 

#### Overview of My Project
First, I began by accessing ~20k board game records from a combination of 
xml data access via Board Game Geek's (BGG) API, along with a Kaggle csv 
of additional board game attribute data scraped from BGG by another user. 
Using the xmltodict package, I was able to parse the xml data and save it 
to a python dictionary. From there, I enhanced the dictionary objects with 
additional board game attributes from the Kaggle csv. 

After getting a better understanding of the data, I was able to think 
through various methods of categorizing the data in order to create a tree 
with a series of user questions. These user questions would allow the 
computer to filter through a subset of the ~20k board game objects and 
recommend the right one for the user. 
