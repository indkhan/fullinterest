import allapi
import requests
api =allapi.weatherapi

def weatherreport(city):

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    request_url = f"{base_url}?appid={api}&q={city}"
    response = requests.get(request_url)
    data = response.json()
    weather = data["weather"][0]["description"]
    temp = round(int(data["main"]["temp"]) - 273.15,2)
    feel = round(int(data["main"]["feels_like"]) - 273.15)
    humidity = round(data["main"]["humidity"])


    return({'weather' :weather, 'temp' :temp,'feel' :feel,'humidity' :humidity})


if __name__ == "__main__":
    city = input("enter the city name: ")
    print(weatherreport(city))