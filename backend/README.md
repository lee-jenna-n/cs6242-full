# CSE6242

## 1. Perform Data Analysis, Data Cleanup, Feature Engineering, Machine Learning Modeling (K-means Clustering) using Jupyter Notebook
### Pre-requisites
* Jupyter notebook environment
* An account with Plotly and an API Key generated if you need to view the charts within the Jupyter notebook (https://community.plotly.com/t/how-could-i-get-my-api-key/3088)
* Download the input file tracks_features.csv from https://www.kaggle.com/rodolfofigueroa/spotify-12m-songs/

### Steps
* Download the tracks_features.csv file from https://www.kaggle.com/rodolfofigueroa/spotify-12m-songs/ and place it in the 'data' folder
* Set environment variables PLOTLY_USERNAME and PLOTLY_APIKEY using the user name and API Key generated using the Plotly account. Ignore this step if you do not want to visualize the 3-D chart which uses Plotly within the Jupyter notebook. You will have to manually comment out this section within the Jupyter notebook if so. 

## 2. Run a Flask API app to accept input from UI through a REST API call. 
### Pre-requisites
* Make sure Step1 above is completed 
* Create a virtual environment and install all dependencies from the requirements.txt file

### Steps
* Install all dependencies from the requirements.txt file 
* You can run the app locally by navigating to the FlaskAPI folder and typing "flask run"
* The app will run by default at http://localhost:5000/
* In order to test the REST API, use Postman or any other API testing tool by using the below parameters
    * Method - GET
    * URL - http://localhost:5000/song-recommendations/api/v1.0/getsongs
    * In the body of the request, enter the below parameters under 'form-data'
        * ***activity*** - Try 'driving' or look at the code to identify supported activities
        * ***numSongs*** - An integer for the number of songs to be displayed 
        * ***explicitYN*** - Y or N depending on whether songs with explicit lyrics need to be displayed 
        * ***dob_year*** - Year of birth of the user
