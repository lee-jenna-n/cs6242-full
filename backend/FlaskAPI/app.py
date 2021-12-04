from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# def db_connection():
#     conn = None
#     try:
#         conn = sqlite3.connect("clusters.sqlite")
#     except sqlite3.error as e:
#         print(e)
#     return conn

@app.route("/song-recommendations/api/v1.0/getsongs", methods=['GET'])
#@cross_origin()
def getsongList():

    numSongs = 10 if request.args.get('numSongs') == None else int(request.args.get('numSongs'))
    dob_year = 0 if  request.args.get('dob_year') == None else int(request.args['dob_year'])
    explicit = 'N' if request.args.get('explicitYN') == None else request.args.get('explicitYN')
    activity = None if request.args.get('activity') == None else request.args.get('activity').lower()

    acceptedActivities = list(pd.read_parquet('data/acceptedActivities.parquet')['activity'])

    #print("Activity passed", activity)
    if activity == 'None' or activity not in acceptedActivities:
        return ({"error" : "Activity missing in request or different from accepted ones! Currently accepted activities are 'driving', 'cooking', 'studying', 'working out', 'cleaning', 'being creative'"})

    if dob_year < 1900 or dob_year > 2021:
        return ({"error" : "DOB Year seems to have an invalid value. Needs to be 1900 <= YYYY <= 2021"})

    seedIndexes = pd.read_parquet('data/seedInfo.parquet')

#    print ("Activity passed is",activity)
#    print ("Seed Indexes\n",seedIndexes)

    cluster = seedIndexes.loc[seedIndexes['Activity'] == activity]['Cluster'].iloc[0]

#    print ("Cluster is ", cluster)


    songswithcluster = pd.read_parquet('data/clusters_trimmed.parquet')

    # FIlter the songs dataset for this cluster
    filtrd = songswithcluster[songswithcluster['Cluster'] == cluster]

    # If Explicit is NO, then use only non-Explicit, if not, include all
    filtrd = filtrd[filtrd['explicit'] == 0] if explicit == 'N' else filtrd

    # Add customers Date of birth to the dataset
    filtrd = filtrd.assign(custDOB=dob_year)

    # Identify customer age at the time of song's release year
    filtrd['ageAtSongRelease'] = filtrd['year'] - filtrd['custDOB']  # .assign(ageAtSongRelease = custDOB - year)

    #Filter sogns which might have released around or after the user turned 15
    filtrd = filtrd[filtrd['ageAtSongRelease'] > 14]

    #Read PCA Output Files
    distArrayPd = pd.read_parquet('data/featureColumns_'+activity.replace(" ","") + '.parquet')

    # Add the distance also to the filtered dataset
    filtrd['distance'] = distArrayPd['distance']

    # Sort the dataframe by distance .. Ascending
    filtrd = filtrd.sort_values(by='distance').reset_index()

    i = 0
    songindexes = []
    checkdups = {'name': [], 'artist': [], 'album': []}
    while len(songindexes) < numSongs:
        songName = filtrd.iloc[i]['name']
        artist = filtrd.iloc[i]['artists']
        album = filtrd.iloc[i]['album']
        age = filtrd.iloc[i]['ageAtSongRelease']
        if songName in checkdups['name'] or artist in checkdups['artist'] or album in checkdups['album'] or abs(
                age) > 50:
            i += 1
            continue
        else:
            songindexes += [i]
            checkdups['name'] += [songName]
            checkdups['artist'] += [artist]
            checkdups['album'] += [album]
            i += 1

    filteredSongs = filtrd.iloc[songindexes]
    outputDict = {}
    for i in range(len(filteredSongs)):
        songlist = {'songName': None, 'artistName': None, 'releaseDate': None}
        songlist['songName'] = filteredSongs.iloc[i]['name']
        songlist['artistName'] = filteredSongs.iloc[i]['artists']
        songlist['albumName'] = filteredSongs.iloc[i]['album']
        songlist['releaseDate'] = filteredSongs.iloc[i]['release_date']
        outputDict[i] = songlist

    return outputDict
## end of code with FILE

    # output = {}
    # output['0'] = {'songName': 'En direct des arshitechs du son (Skit)',
    #                 'artistName': "['Taktika']",
    #                 'releaseDate': '2008-10-07',
    #                 'albumName': 'Le coeur et la raison'}
    # output['1'] = {'songName': 'Max It Up (Road Mix)',
    #                 'artistName': "['Destra']",
    #                 'releaseDate': '2006-04-26',
    #                 'albumName': 'Independent Lady'}
    # output['2'] = {'songName': 'Corny Jokes',
    #                 'artistName': "['Spitfire']",
    #                 'releaseDate': '2004-07-01',
    #                 'albumName': 'Thrills and Kills'}
    # output['3'] = {'songName': 'Canta (Hands Up)',
    #                 'artistName': "['Merengue Latin Band']",
    #                 'releaseDate': '2008-03-01',
    #                 'albumName': 'Merengue Party'}
    # output['4'] = {'songName': 'Mujeres, Mujeres',
    #                 'artistName': "['Dionis y La Banda Flakka']",
    #                 'releaseDate': '2015-05-12',
    #                 'albumName': 'Ponte En 4'}

   #  #output
    return output


# running REST interface, port=5000 for direct test
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)