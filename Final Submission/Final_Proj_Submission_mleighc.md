# SI507 Final Project Submission

### Github Repo
[mleighc/SI507-FinalProject](https://github.com/mleighc/SI507-FinalProject.git)           


### Project Code
**Packages**:             
> requests   
> xmltodict    
> webbrowser   
     
## README
**Files**:                  
* **Final_Proj_API.py**
> Python File with code for accessing Board Game Geek's API and reading the data from XML to json in order to clean and parse the data. Then, the json objects are written to a json file.

* **bgg_list.json**
> The final file created by the code in Final_Proj_API.py.

* **hot_boardgames.json**
> Test json file used as initial example for figuring our the process of writing xmltodict and then saving that dict to json.

* **Final_Proj_Tree.py**
> Code for reading in the bgg_list.json file, parsing the data based on the outline of the tree structure and user question/answer flow, then loading that data into the tree structure. This file also include the control flow for interacting with the user and displaying necessary game information based on their answers to the computer's questions.

**Description of the Program**:      
     
First, I began by accessing about 20k board game records from a combination of xml data accessed via Board Game Geek's (BGG) API, along with a Kaggle csv of additional board game attribute data scraped from BGG by another user. Using the xmltodict package, I was able to parse the xml data and save it to a python dictionary. From there, I enhanced the dictionary objects with additional board game attributes from the Kaggle csv and saved a selected subset of the records (about 500) to a json file.

After getting a better understanding of the data, I was able to think through various methods of categorizing the data (i.e. solo vs. multiplayer games, short vs. long play time, family vs. party games, etc.) in order to create a tree of questions to be asked of the user. These user questions would allow the computer to filter through the subset of the ~20k board game objects and recommend the right list for the user. From there, the user can access details from individual records to make their final selection. I used a subset of data for ease of processing on my limited computer memory, but I believe a larger subset could be worked through and loaded, as well as the addition of more subquestions to shorten the result lists that are returned.

### Data Sources
* [BoardGameGeek XML API2](https://boardgamegeek.com/wiki/page/BGG_XML_API2)       
    * API Data is in XML format
    * Accessed data using *requests* and *xmltodict* modules
* [Kaggle Dataset of Board Game Attributes](https://www.kaggle.com/datasets/andrewmvd/board-games)        
    * csv of game attributes also accessed from Board Game Geek's website      

### More Info on BGG Data
* [Diving into BoardGameGeek](https://jvanelteren.github.io/blog/2022/01/19/boardgames.html).   
    * Article with insights on BGG's ratings just for some research/context
* [BoardGameGeek Data Dictionary on Ratings](https://boardgamegeek.com/wiki/page/ratings)      
    * Additional context and details on the rating system on BGG's website.
* [BoardGameGeek API Terms of Use](https://boardgamegeek.com/wiki/page/XML_API_Terms_of_Use#)       
    * This is a link to BGG's Terms of Service for the data for my reference.

### Data Structure


    

### Interaction and Presentation
    


       

### Demo Video


       
