import requests

def get_times(city,country):
    timesp = requests.get(f"https://api.aladhan.com/v1/timingsByCity/18-09-2023?city={city}&country={country}&method=4")
    fullt = timesp.json()
    times = fullt["data"]["timings"]
    #return times
    fajr ,fajrEnd ,duhr ,asr ,mag ,isha ,ishaEnd = times["Fajr"] , times["Sunrise"] ,times["Dhuhr"] ,times["Asr"] , times["Maghrib"] , times["Isha"] , times["Midnight"]
    output = (f"fajr starts at : {fajr} \nfajr ends at : {fajrEnd} \nduhr starts at : {duhr} \nasr starts at : {asr} \nmaghrib starts at : {mag} \nisha starts at : {isha} \nisha ends at : {ishaEnd}")
    return output

def main():
    
    city = input("Enter your city : ")
    country = input("Enter your country : ")
    print(get_times(city,country))
    




if __name__ == "__main__":
    while True:
        try:
            main()
            break
        except:
            print("enter a valid city and country")
            