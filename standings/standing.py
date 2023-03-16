import requests
from bs4 import BeautifulSoup



response = requests.get("https://www.mackolik.com/puan-durumu/t%C3%BCrkiye-s%C3%BCper-lig/2022-2023/482ofyysbdbeoxauk19yg7tdt")

soup = BeautifulSoup(response.content, "html.parser")



table = soup.find("tbody")
row = table.find_all("tr")

standing_list = []
for count,team in enumerate(row, start=1):
        standing_list.append(team.text.strip().replace(f"{count}          ", "").split("   "))

if __name__ == "__main__":
    for count,i in enumerate(row, start=1):
        print(i.text.strip().replace(f"{count}          ", "").split("   "))