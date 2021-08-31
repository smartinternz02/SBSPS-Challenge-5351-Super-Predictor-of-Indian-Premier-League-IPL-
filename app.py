from flask import Flask,render_template,request,redirect

import pandas as pd
import numpy as np
import joblib


filename='static/linear_model.pkl'
linear_model=joblib.load(filename)




app=Flask(__name__)

matches=pd.read_csv('static/matches.csv')



@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/historicalRecords')
def historicalRecords():
    return render_template('historical_records.html')


@app.route('/redirectTeams',methods=['POST','GET'])
def redirectTeams():
    teamName=request.form.get('team')
    year=request.form.get('year')
    return redirect('/teams/{}/year/{}'.format(teamName,year))


@app.route('/teams/<teamName>/year/<year>',methods=['GET'])
def teams(teamName,year):
    year_wise=matches.loc[matches['season']==int(year)]
    as_team1=year_wise.loc[year_wise['team1']==teamName]
    as_team2=year_wise.loc[year_wise['team2']==teamName]
    as_team1=as_team1.values.tolist()
    as_team2=as_team2.values.tolist()

    # print(as_team1)

    return render_template('historical_records_result.html',as_team1_matches=as_team1,as_team2_matches=as_team2,team=teamName,season=year)


# @app.route('/static_dashboard')
# def static_dashboard():
#     return render_template('static_dashboard.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')


@app.route('/prediction-result',methods=['POST'])
def prediction_result():
    temp_data=[]
    if request.method=="POST":
        runs=int(request.form.get('runs',False))
        wickets=int(request.form.get('wickets',False))
        overs=float(request.form.get('overs',False))
        runs_in_previous_5_overs=int(request.form.get('runs-in-previous-five-overs',False))
        wickets_in_previous_5_overs=int(request.form.get('wickets-in-previous-five-overs',False))
        batting_team=request.form.get('batting-team',False)
        bowling_team=request.form.get('bowling-team',False)

        temp_data=temp_data+[runs,wickets,overs,runs_in_previous_5_overs,wickets_in_previous_5_overs]

        if batting_team=='Chennai Super Kings':
            temp_data=temp_data+[1,0,0,0,0,0,0,0]
        elif batting_team=='Delhi Daredevils':
            temp_data=temp_data+[0,1,0,0,0,0,0,0]
        elif batting_team=='Kings XI Punjab':
            temp_data=temp_data+[0,0,1,0,0,0,0,0]
        elif batting_team=='Kolkata Knight Riders':
            temp_data=temp_data+[0,0,0,1,0,0,0,0]
        elif batting_team=='Mumbai Indians':
            temp_data=temp_data+[0,0,0,0,1,0,0,0]
        elif batting_team=='Rajasthan Royals':
            temp_data=temp_data+[0,0,0,0,0,1,0,0]
        elif batting_team=='Royal Challengers Bangalore':
            temp_data=temp_data+[0,0,0,0,0,0,1,0]
        elif batting_team=='Sunrisers Hyderabad':
            temp_data=temp_data+[0,0,0,0,0,0,0,1]

        if bowling_team=='Chennai Super Kings':
            temp_data=temp_data+[1,0,0,0,0,0,0,0]
        elif bowling_team=='Delhi Daredevils':
            temp_data=temp_data+[0,1,0,0,0,0,0,0]
        elif bowling_team=='Kings XI Punjab':
            temp_data=temp_data+[0,0,1,0,0,0,0,0]
        elif bowling_team=='Kolkata Knight Riders':
            temp_data=temp_data+[0,0,0,1,0,0,0,0]
        elif bowling_team=='Mumbai Indians':
            temp_data=temp_data+[0,0,0,0,1,0,0,0]
        elif bowling_team=='Rajasthan Royals':
            temp_data=temp_data+[0,0,0,0,0,1,0,0]
        elif bowling_team=='Royal Challengers Bangalore':
            temp_data=temp_data+[0,0,0,0,0,0,1,0]
        elif bowling_team=='Sunrisers Hyderabad':
            temp_data=temp_data+[0,0,0,0,0,0,0,1]

        final_data=np.array([temp_data])

        score_prediction=int(linear_model.predict(final_data))

        return render_template('prediction_result.html',lower_range=score_prediction-5,upper_range=score_prediction+5)


if __name__=='__main__':
    app.run(debug=False)
