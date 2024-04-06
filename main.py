import openai
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv()






# get users location, maybe convert to long, lat for api (geocoding api)
lat = 51.5
lon = -0.12
units = 'metric' # standard = temp in Kelvin and windspeed in meter/sec, imperial = fahrenheit and miles/hour, metric = celsius and meter/sec
api_key = "68a7c54e00bb87f6376a5105a36a2f24"
url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units={units}&appid={api_key}"


response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # Gets all data for current time, can add more types of data if needed
    location = data['timezone']
    currenttemp = data['current']['temp']
    currentpressure = data['current']['pressure']
    currenthumidity = data['current']['humidity']
    currentwind = data['current']['wind_speed']
    currentdesc = data['current']['weather'][0]['description']
    currenticon = data['current']['weather'][0]['icon']
    
    # Data for future forecasts, hourly, and  daily data
    temp1hour = data['hourly'][0]['temp']
    temp2hour = data['hourly'][1]['temp']
    print("temp in 1 hour:", temp1hour)
    print("temp in 2 hour:", temp2hour)
    
    todaySummary = data['daily'][0]['summary']
    
    try:
        alertSender = data['alerts'][0]['sender_name']
        alertEvent = data['alerts'][0]['event']
        alertDesc = data['alerts'][0]['description']
    except:
        print("There are no current alerts for your area.")
    
    
else:
    print('Error fetching weather data')
    
print('Your location is: ', location)
print("The current temperature is: ", currenttemp)
print("The current pressure is: ",currentpressure)
print("The current humidity is: ",currenthumidity)
print("The current wind speed is: ",currentwind)
print("Description: ",currentdesc)
print(todaySummary)


#chatgpt stuff
client = openai.OpenAI()
instruct = "You are a weather assistant that will help users and give a description of todays weather and help them with what type of outfit to where or to bring an umbrella etc. Keep response at a normal paragraph length. You will also be given weather information, you must use this in your response to the user."

my_assistant = client.beta.assistants.create(
    model="gpt-3.5-turbo",
    instructions = instruct,
    name = "Weather App Assistant",
    tools =[{"type": "code_interpreter"}],
)

#thread stuff
thread = client.beta.threads.create()

thread_message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"{data}",
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=my_assistant.id,
)

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
 