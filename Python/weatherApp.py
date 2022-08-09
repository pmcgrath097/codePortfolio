#Patrick McGrath
#Weather Application using APIs

from typing import List
from guizero import *
import urllib.request
import json
from matplotlib import *
import matplotlib.pyplot as plt
from datetime import *
from pytz import timezone

apiURL = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid=6b352f833cf6fd3787c28236d636b810"

boston = [42.36,-71.06]
losangeles = [34.05,-118.24]
austin = [30.27,-97.74]
miami = [25.76,-80.19]
seattle = [47.61,-122.33]
phoenix = [33.45,-112.07]

x = []
y = []

def getWeather(lat, long):
    url = urllib.request.urlopen(apiURL.format(lat, long))
    data = url.read()
    jsonData = json.loads(data)

    if(str(url.getcode()) == "200"):
        #Pulls timezone and time in seconds from 1970 from the JSON data to create a datetime object for the loca ltime of the selected city
        timeZone = str(jsonData["timezone"])
        timeInSec = jsonData["current"]["dt"]
        localTime = datetime.fromtimestamp(timeInSec, timezone(timeZone))

        #Populates labels in the GUI with data from the JSON data of the API request
        tzText.value = "      Time Zone: " + str(timezone(timeZone)).replace("_", " ")
        currentTime.value = "      Local Time: " + str(localTime.strftime("%I:%M %p"))
        weatherText.value = "      Current Weather: " + str(jsonData["current"]["weather"][0]["main"])
        tempCelcius.value = "      Current Temperature: " + str(jsonData["current"]["temp"]) + " " + u"\N{DEGREE SIGN}" + "C"
        feelsLike.value = "      Feels Like: " + str(jsonData["current"]["feels_like"]) + " " + u"\N{DEGREE SIGN}" + "C"
        humidity.value = "      Humidity: " + str(jsonData["current"]["humidity"]) + "%"
        windSpeed.value = "      Wind Speed: " + "%2.1f"%(jsonData["current"]["wind_speed"] * 3.6) + " km/h"
    else: #Print that an error occured if the HTML code returned was not 200
        print("An error has occured. Please try again.")

def plotWeather(lat, long, condition):
    url = urllib.request.urlopen(apiURL.format(lat, long))
    data = url.read()
    jsonData = json.loads(data)

    if(str(url.getcode()) == "200"):
        
        for i in jsonData["hourly"]:
            timeAt_i = datetime.fromtimestamp(i["dt"], timezone(jsonData["timezone"])).strftime("%I:%M %p")
            if(condition == ("Tempurature" + " " + u"\N{DEGREE SIGN}" + "C")):
                y.append(i["temp"])
            elif(condition == "Feels Like" + " " + u"\N{DEGREE SIGN}" + "C"):
                y.append(i["feels_like"])
            elif(condition == "Humidity (%)"):
                y.append(i["humidity"])
            elif(condition == "Wind Speed (km/h)"):
                y.append(i["wind_speed"] * 3.6)
            elif(condition == "Atmospheric Pressure (Pascals)"):
                y.append(i["pressure"])
            elif(condition == "UV Index"):
                y.append(i["uvi"])
            x.append(timeAt_i)
        
        x1 = []
        x2 = []
        y1 = []
        y2 = []
        for i in range(24):
            x1.append(x[i])
            y1.append(y[i])
        for i in range(24, 48):
            x2.append(x[i])
            y2.append(y[i])

        plt.figure(num = "Requested Weather Data", figsize = [15, 5])

        plt.subplot(121)
        plt.plot(x1,y1)
        plt.xlabel("Time")
        plt.ylabel(condition)
        plt.title("Hourly data for {} over the first 24 hours for {}".format(condition, cities.value))
        plt.gcf().autofmt_xdate()

        plt.subplot(122)
        plt.plot(x2,y2)
        plt.xlabel("Time")
        plt.ylabel(condition)
        plt.title("Hourly data for {} over the second 24 hours for {}".format(condition, cities.value))
        plt.gcf().autofmt_xdate()

        plt.show()
    else:
        print("An error has occured. Please try again.")
    #plot data from JSON data

#callback functions for the ButtonGroup and PushButton objects respectively
def updateWeather():
    if(cities.value == "Boston, MA"):
        getWeather(boston[0], boston[1])
    elif(cities.value == "Los Angeles, CA"):
        getWeather(losangeles[0],losangeles[1])
    elif(cities.value == "Austin, TX"):
        getWeather(austin[0],austin[1])
    elif(cities.value == "Miami, FL"):
        getWeather(miami[0],miami[1])
    elif(cities.value == "Seattle, WA"):
        getWeather(seattle[0],seattle[1])
    elif(cities.value == "Phoenix, AZ"):
        getWeather(phoenix[0],phoenix[1])

def createPlot():
    if(cities.value == "Boston, MA"):
        plotWeather(boston[0], boston[1], conditions.value)
    elif(cities.value == "Los Angeles, CA"):
        plotWeather(losangeles[0],losangeles[1], conditions.value)
    elif(cities.value == "Austin, TX"):
        plotWeather(austin[0],austin[1], conditions.value)
    elif(cities.value == "Miami, FL"):
        plotWeather(miami[0],miami[1], conditions.value)
    elif(cities.value == "Seattle, WA"):
        plotWeather(seattle[0],seattle[1], conditions.value)
    elif(cities.value == "Phoenix, AZ"):
        plotWeather(phoenix[0],phoenix[1], conditions.value)

def main():
    #Code below creates the GUI to display the information requested by the user
    app = App(title = "Lab11_Web_JSON_Weather - Patrick McGrath", layout = "grid", height = 500, width = 1025)
    
    global titleText
    titleText = Text(app, text = "Select a city from the list below to view the current weather conditions", grid = [1,0], size = 16)
    global cities
    citiesLabel = Text(app, text = "Cities:", grid = [0,2])
    cities = ButtonGroup(app, options = ["Boston, MA","Los Angeles, CA","Austin, TX","Miami, FL","Seattle, WA","Phoenix, AZ"], command = updateWeather, grid = [0,3,1,6])
    global tzText
    tzText = Text(app, text = "      Time Zone: ", grid = [1,3], align = "left", size = 10)
    global currentTime
    currentTime = Text(app, text = "      Local Time: ", grid = [1,4], align = "left", size = 10)
    global weatherText
    weatherText = Text(app, text = "      Current Weather: ", grid = [1,5], align = "left", size = 10)
    global tempCelcius
    tempCelcius = Text(app, text = "      Current Temperature: ", grid = [1,6], align = "left", size = 10)
    global feelsLike
    feelsLike = Text(app, text = "      Feels Like: ", grid = [1,7], align = "left", size = 10)
    global humidity
    humidity = Text(app, text = "      Humidity: ", grid = [1,8], align = "left", size = 10)
    global windSpeed
    windSpeed = Text(app, text = "      Wind Speed: ", grid = [1,9], align = "left", size = 10)
    blankSpace = Text(app, text = "", grid = [1,10], width = "fill")
    buttonDesc = Text(app, text = "Select a weather condition and press the button to plot hourly data for the selected weather condition of the selected city.", grid = [1,11])
    global conditions
    conditions = ButtonGroup(app, options = ["Tempurature" + " " + u"\N{DEGREE SIGN}" + "C", "Feels Like" + " " + u"\N{DEGREE SIGN}" + "C", "Humidity (%)","Wind Speed (km/h)","Atmospheric Pressure (Pascals)", "UV Index"], grid = [1,12,6,1], horizontal = True)
    plotButton = PushButton(app, text = "Plot", command = createPlot , grid = [1,13])
    
    getWeather(boston[0],boston[1])

    app.display()

if __name__ == "__main__":
    main()