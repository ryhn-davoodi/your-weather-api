from flask import Flask,render_template
import pandas as pd

app=Flask(__name__)
# get the stations data from csv file to show
df_stations=pd.read_csv("data_small/stations.txt",skiprows=17)
df_stations=df_stations[["STAID","STANAME                                 "]]



@app.route("/")
def home():
    return render_template("home.html",data=df_stations.to_html())

@app.route("/api/v1/<station>/<date>")
def about(station,date):
    filename="data_small/TG_STAID" +str(station).zfill(6)+ ".txt"
    df = pd.read_csv(filename, skiprows=20,parse_dates=["    DATE"])
    temperature =df.loc[df["    DATE"] == date]["   TG"].squeeze()/10
    return {
            'station': station,
            'date': date,
            'temperature': temperature
           }


@app.route("/api/v1/<station>")
def add_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df_stanum=pd.read_csv(filename,skiprows=20,parse_dates=["    DATE"])
    result=df_stanum.to_dict(orient="records")
    return result




@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station,year):

    filename="data_small/TG_STAID"+str(station).zfill(6)+".txt"
    years=pd.read_csv(filename,skiprows=20)
    years["    DATE"]=years["    DATE"].astype(str)
    result=years[years["    DATE"].str.startswith(str(year))]
    result=result.to_dict(orient="records")
    return result





if __name__=="__main__":
    app.run(debug=True)