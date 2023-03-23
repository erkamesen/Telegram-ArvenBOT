import datetime
import requests
from bs4 import BeautifulSoup


for_translate = str.maketrans("çğıöşü", "cgiosu")


class Ramadan:
    BASE_URL = "https://www.hurriyet.com.tr/ramazan/"
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0"
    }


    def __init__(self, city):
        self.city = city.lower().translate(for_translate)
        self.current_date = str(datetime.datetime.today().strftime('%Y/%m/%d')).replace("/", "-")
        self.tomorrow_date = str((datetime.datetime.today()+datetime.timedelta(1)).strftime('%Y/%m/%d')).replace("/", "-")
        self.current_time = datetime.datetime.today().strftime("%H:%M")
        self.URL = f"{Ramadan.BASE_URL}{self.city}-imsakiye/"

        response = requests.get(self.URL, headers=Ramadan.header)
        self.soup = BeautifulSoup(response.content, "html.parser")

        self.datas = {}

        self.get_times(self.current_date)
        self.get_times(self.tomorrow_date)



    def get_times(self, date):
        id = f"date{date}"
        try:
            row = self.soup.find("tr", id=id)
            tds = row.find_all("td")
            self.datas[f"{date}_sehri_time"] = tds[2].text
            self.datas[f"{date}_iftar_time"] = tds[6].text
        except:
            self.datas[f"{date}_sehri_time"] = "Unknown"
            self.datas[f"{date}_iftar_time"] = "Unknown"

        return self.datas
    
    def responses(self):

        to_iftar = None
        to_sehri = None
        if "Unknown" in self.datas.values():
            to_iftar = "Unknown"
            to_sehri = "Unknown"
        else:
            ct_hour = int(self.current_time.split(":")[0])
            ct_minute = int(self.current_time.split(":")[1])
            if self.current_time < self.datas[f"{self.current_date}_iftar_time"]:
                iftar_hour = int(self.datas[f"{self.current_date}_iftar_time"].split(":")[0])
                iftar_minute = int(self.datas[f"{self.current_date}_iftar_time"].split(":")[1])
                time = str(datetime.timedelta(hours=iftar_hour, minutes=iftar_minute)-datetime.timedelta(hours=ct_hour, minutes=ct_minute)).split(":")
                to_iftar = f"{time[0]} hours, {time[1]} minutes left."

            if self.current_time > self.datas[f"{self.current_date}_iftar_time"]:
                iftar_hour = int(self.datas[f"{self.tomorrow_date}_iftar_time"].split(":")[0])
                iftar_minute = int(self.datas[f"{self.tomorrow_date}_iftar_time"].split(":")[1])
                time = str(datetime.timedelta(hours=iftar_hour, minutes=iftar_minute)-datetime.timedelta(hours=ct_hour, minutes=ct_minute)).split(":")
                to_iftar = f"{time[0]} hours, {time[1]} minutes left."
            
            if self.current_time > self.datas[f"{self.current_date}_sehri_time"]:
                sehri_hour = int(self.datas[f"{self.tomorrow_date}_sehri_time"].split(":")[0])
                sehri_minute = int(self.datas[f"{self.tomorrow_date}_sehri_time"].split(":")[1])
                time = str(datetime.timedelta(hours=sehri_hour, minutes=sehri_minute)-datetime.timedelta(hours=ct_hour, minutes=ct_minute)).split(":")
                to_sehri = f"{time[0]} hours, {time[1]} minutes left."

            if self.current_time < self.datas[f"{self.current_date}_sehri_time"]:
                sehri_hour = int(self.datas[f"{self.current_date}_sehri_time"].split(":")[0])
                sehri_minute = int(self.datas[f"{self.current_date}_sehri_time"].split(":")[1])
                time = str(datetime.timedelta(hours=sehri_hour, minutes=sehri_minute)-datetime.timedelta(hours=ct_hour, minutes=ct_minute)).split(":")
                to_sehri = f"{time[0]} hours, {time[1]} minutes left."
        
        return {"to_iftar":to_iftar, "to_sehri":to_sehri}
       




    