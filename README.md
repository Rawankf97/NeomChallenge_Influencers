# Identifying Twitter Influencers in Real-time for NEOM’s Tourism Advertising Purpose 



## Source files description

### Files Description

The complate source code of the web in **falsk_app** file, which included the following files:
    
    serve.py                Start runs the program
    streamData.py           Initialize the user parameters, capture the stream and save the data in the database.
    sliding_window.py       Slides the window on the database and sends the actions to action_based.py.
    action_based.py         Create the model, calculate the influence set and the influence scores to get the top influencers.
    
    static                  JavaScript and CSS files of the web.
    templates               HTML files of the web pages (Search and dashboard).



### Functions Description
**streamData.py functions:**

    initializeQuery         User initialize the required parameters for the query to identify top_k influencers
    calculateActionScore    Convert theaction priority scale to action weight 
    startStreamListiner     Thefunctiontocapturethereal-time stream 
    insertBuffer            Insert the buffer data tothedatabase 
    on_data                 Receives the tweets and insert them in the buffer 
    on_error                Function to catchstreamerrors 
    on_status               Function to print the streamstatus

**sliding_window.py functions:**

    connect                 Connect the database with window class
    close                   Close the database connection with the window
    start                   Start sliding the window over the database 
    initialize              Initialize window at the beginning 
    slide                   Slides the window once 
    update_time_limit       Updates time limit for the current slide 
    count_expiries          Counts the number of data that are outside the window’s new time limit
    remove_expiries         Removes expired data from the window

**action_based.py functions:**

    process                 Remove data and add the new ones then calls the process functions
    remove                  Remove the old actions from the model
    insert                  Insert the actions in the model
    influence_set_insert    Calculate the influence set of the action after insert it into the model
    Influence_set_remove    Remove the data of influence set after remove it from the model
    Influence_score         Calculate the influencer scores and the results from the in- fluence set and user filters
    
**serve.py functions:**

     data                   When a GET request is received on route ’/data’ returns the latest results
     update                 When a GET request is received on route ’/updated’ waits for new results from the model then responds with a mes- sage signaling the data has been updated and is ready to be sent
     index                  When a GET request is received on route ’/’ renders the search.html page. When a POST request is received on route ’/’ sends the query parameters and starts the stream- ing process
     dashboard              When a GET request is received on route ’/dashboard’ ren- ders the dashboard.html page
     
**search.js functions:**

     wait_for_update        Creates a GET requests to route ’/updated’ and waits for the response upon which calls load_data
     load_data              Creates a GET request to route ’/data’ and receives latest results if the request is successful the window is assigned location ’/dashboard’
     getFormFields          Initializes query form variables from the currently active tab
     getFormValues          Gets the query form values when the submit button i clicked
     validate               Checks if the query form is filled correctly and input is valid
     submitForm             Creates a POST request to route ’/’ if the query form passes validation then displays the loading screen
     validateLocation       If a location is provided as a query parameter, checks if it corresponds to an actual location on the map by making a request to openstreetmap

**dashboard.js functions:**

     wait_for_update        Creates a GET requests to route ’/updated’ and waits for the response upon which calls load_data
     load_data              Creates a GET request to route ’/data’ and receives latest re- sults if the request is successful the document gets updated with the new results
     updateMetaData         Updates the timer and the available meta data values every time new data is loaded
     draw                   Creates the graphs and charts every time new data is loaded

## Required packages and steps to run the program

### Step1 
Download or use python IDE to run the program, we used Visual Studio Code.

### Step2

* Install Python packages:

**Tweepy**

To install using pip:
```
pip install tweepy 
```
Using Git: 
```
git clone https://github.com/tweepy/tweepy.git 
cd tweepy 
pip install 
```
Install directly from the GitHub repository: 
```
pip install git+https://github.com/tweepy/tweepy.git
```
**Flask**

Using pip:
```
pip install flask
```

**sqlite3**

For Python version 3:
```
pip install pysqlite3 
```

### Step 3

Run serve.py in flask_app file, then click on the link in the output to open the web in the browser.
