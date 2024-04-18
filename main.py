import openai
import requests
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
abstract_key = os.getenv("ABSTRACT_API_KEY")
weather_key=os.getenv("OPENWEATHERMAP_API_KEY")

#Abstract API
responseLoc = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={abstract_key}")
print(responseLoc.status_code)
if responseLoc = status_code == 200:

    print(responseLoc.content)
    locationData = responseLoc.json()
    
    # get the users location
    lat = locationData['latitude']
    lon = locationData['longitude']
    print("long and lat :" , lat, " ", lon)
else:
    Print("Error fetching location data!")

#OpenWeatherMap API
units = 'metric' # standard = temp in Kelvin and windspeed in meter/sec, imperial = fahrenheit and miles/hour, metric = celsius and meter/sec
url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units={units}&appid={weather_key}"


response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # Gets all weather data for current time from api, can add more types of data if needed
    timezone = data['timezone']
    location = f"{locationData['city']}, {locationData['region']}"
    currenttemp = data['current']['temp']
    currentfeelslike = data['current']['feels_like']
    currentpressure = data['current']['pressure']
    currenthumidity = data['current']['humidity']
    currentwind = data['current']['wind_speed']
    currentpressure = data['current']['pressure']
    currentclouds = data['current']['clouds']
    currentdesc = data['current']['weather'][0]['description']
    currenticon = data['current']['weather'][0]['icon']
    
    # Data for future forecasts, hourly, and  daily data
    temp1hour = data['hourly'][0]['temp']
    icon1hour = data['hourly'][0]['weather'][0]['icon']
    
    temp2hour = data['hourly'][1]['temp']
    icon2hour = data['hourly'][1]['weather'][0]['icon']
    
    temp3hour = data['hourly'][2]['temp']
    icon3hour = data['hourly'][2]['weather'][0]['icon']
    
    temp4hour = data['hourly'][3]['temp']
    icon4hour = data['hourly'][3]['weather'][0]['icon']
    
    temp5hour = data['hourly'][4]['temp']
    icon5hour = data['hourly'][4]['weather'][0]['icon']
    
    temp6hour = data['hourly'][5]['temp']
    icon6hour = data['hourly'][5]['weather'][0]['icon']
    
    temp7hour = data['hourly'][6]['temp']
    icon7hour = data['hourly'][6]['weather'][0]['icon']

    temp8hour = data['hourly'][7]['temp']
    icon8hour = data['hourly'][7]['weather'][0]['icon']
    
    temp9hour = data['hourly'][8]['temp']
    icon9hour = data['hourly'][8]['weather'][0]['icon']
    
    temp10hour = data['hourly'][9]['temp']
    icon10hour = data['hourly'][9]['weather'][0]['icon']
    
    temp11hour = data['hourly'][10]['temp']
    icon11hour = data['hourly'][10]['weather'][0]['icon']
    
    temp12hour = data['hourly'][11]['temp']
    icon12hour = data['hourly'][11]['weather'][0]['icon']
    
    temp1day = data['daily'][0]['temp']['day']
    icon1day = data['daily'][0]['weather'][0]['icon']
    
    temp2day = data['daily'][1]['temp']['day']
    icon2day = data['daily'][1]['weather'][0]['icon']
    
    temp3day = data['daily'][2]['temp']['day']
    icon3day = data['daily'][2]['weather'][0]['icon']
    
    temp4day = data['daily'][3]['temp']['day']
    icon4day = data['daily'][3]['weather'][0]['icon']
    
    temp5day = data['daily'][4]['temp']['day']
    icon5day = data['daily'][4]['weather'][0]['icon']
    
    temp6day = data['daily'][5]['temp']['day']
    icon6day = data['daily'][5]['weather'][0]['icon']
    
    temp7day = data['daily'][6]['temp']['day']
    icon7day = data['daily'][6]['weather'][0]['icon']
    
    todaySummary = data['daily'][0]['summary']
    
    
    #Alert System
    alert = False
    try:
        alertSender = data['alerts'][0]['sender_name']
        alertEvent = data['alerts'][0]['event']
        alertDesc = data['alerts'][0]['description']
        print("Danger Alert: Natural distaster of unuseual weather conditions detected!")
        alert = True
    except:
        print("There are no current alerts for your area.")
        
    if (alert):
        print(f"- {alertEvent}: {alertDesc}")
        print(f"Sender: {alertSender}")
    
    
else:
    print('Error fetching weather data')
    
print('Your location is:', location)
print('Your timezone is: ', timezone)
print("The current temperature is: ", currenttemp)
print("The current pressure is: ",currentpressure)
print("The current humidity is: ",currenthumidity)
print("The current wind speed is: ",currentwind)
print("Description: ",currentdesc)
print(todaySummary)

print("Temperature in 1h: ", temp1hour)
print("Temperature in 2h: ", temp2hour)
print("Temperature in 3h: ", temp3hour)
print("Temperature in 4h: ", temp4hour)
print("Temperature in 5h: ", temp5hour)
print("Temperature in 6h: ", temp6hour)
print("Temperature in 7h: ", temp7hour)
print("Temperature in 8h: ", temp8hour)
print("Temperature in 9h: ", temp9hour)
print("Temperature in 10h: ", temp10hour)
print("Temperature in 11h: ", temp11hour)
print("Temperature in 12h: ", temp12hour)

print("Temperature in 1 day: ", temp1day)
print("Temperature in 2 day: ", temp2day)
print("Temperature in 3 day: ", temp3day)
print("Temperature in 4 day: ", temp4day)
print("Temperature in 5 day: ", temp5day)
print("Temperature in 6 day: ", temp6day)
print("Temperature in 7 day: ", temp7day)


#ChatGPT
client = openai.OpenAI()
instruct = "You are a weather assistant that will help users and give a description of todays weather and help them with what type of outfit to where or to bring an umbrella etc. Keep response at a normal paragraph length. You will also be given weather information, you must use this in your response to the user."

#Assistant creation
my_assistant = client.beta.assistants.create(
    model="gpt-3.5-turbo",
    instructions = instruct,
    name = "Weather App Assistant",
    tools =[{"type": "code_interpreter"}],
)

#Thread Creation
thread = client.beta.threads.create()

thread_message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"The user is located at: {location}. API data to use: {data}",
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=my_assistant.id,
)

# Handles ChatGPT message and wait time
while run.status in ["queued", "in_progress"]:
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")
    
    if keep_retrieving_run.status == "completed":
        
        all_messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        #print(f"User: {thread_message.content[0].text.value}")
        print(f"Assistant: {all_messages.data[0].content[0].text.value}")
        
        break
    elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
        pass
    else:
        print(f"Run status: {keep_retrieving_run.status}")
        break
 
