import openai
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv()

client = openai.OpenAI()
model = "gpt-3.5-turbo"

# weather_app_assist = client.beta.assistants.create(
#     name="Weather App Assistant",
#     instructions="""You are a weather assistant that will help users and give a description of todays weather and help them with what type of outfit to where or to bring an umbrella etc.
#         Keep response at a normal paragraph length. You will also be given weather information, you must use this in your response to the user.""",
#     model=model,
# )

# assistant_id = weather_app_assist.id
# print(weather_app_assist.id)

# get users location, maybe convert to long, lat for api (geocoding api)
lat = 51.5
lon = -0.12
api_key = "68a7c54e00bb87f6376a5105a36a2f24"
url = f"https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&appid={api_key}"


response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    temp = data['current']['temp']
    pressure = data['current']['pressure']
    humidity = data['current']['humidity']
    wind = data['current']['wind_speed']
    #desc = data['current']['weather']['description']
    
else:
    print('Error fetching weather data')
    
print(temp)
print(pressure)
print(humidity)
print(wind)
#print(desc) dunno why this doesnt work

# hardcode id's
assistant_id = "asst_TbB3sXt4jF5DmOVwdgW1ueL0"
thread_id = "thread_ddHIXxR5LfoIpo9FXi5PsVGG"
# thread


# thread_id = thread.id
# print(thread_id)