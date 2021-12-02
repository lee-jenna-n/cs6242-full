CS 6242 Final Project - Team 121

DESCRIPTION
Our app will aim to help users discover new music based on the activity they are doing when they listen to music. Users will be able to input their activity (e.g., driving, cooking, working out) and age directly into our interface and our algorithm will use that activity to create a custom playlist. 

This code is organized into backend/ and frontend/ directories. The backend is a Flask app and the frontend is a ReactJS app.



INSTALLATION
In order to install the code, you must first perform data analysis, data cleanup, feature engineering, and machine learning modeling (K-means clustering). This is done in a Jupyter Notebook.

Pre-requisites
- Jupyter notebook environment
- An account with Plotly and an API Key generated if you need to view the charts within the Jupyter notebook (https://community.plotly.com/t/how-could-i-get-my-api-key/3088)
- Download the input file tracks_features.csv from https://www.kaggle.com/rodolfofigueroa/spotify-12m-songs/

Steps
- Download the tracks_features.csv file from https://www.kaggle.com/rodolfofigueroa/spotify-12m-songs/ and place it in the 'data' folder
- Set environment variables PLOTLY_USERNAME and PLOTLY_APIKEY using the user name and API Key generated using the Plotly account. Ignore this step if you do not want to visualize the 3-D chart which uses Plotly within the Jupyter notebook. You will have to manually comment out this section within the Jupyter notebook if so.


Afterwards, you must install the dependencies for the Flask app

Pre-requisites
- Python

Steps
- cd /backend/FlaskAPI
- pip install -r requirements.txt


Lastly, you must install the dependencies for the React app

Pre-requisites
- yarn

Steps:
- cd /frontend
- yarn install



EXECUTION

To run a local demo, you must start the backend and frontend separately.

The backend will run on localhost:5000 by default. To start it, run "flask run" in /backend/FlaskAPI

The frontend will run on localhost:3000 by default. To start it, run "yarn start" in /frontend

