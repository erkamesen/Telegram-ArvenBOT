import requests
from bs4 import BeautifulSoup


currency_list = []

response = requests.get("https://finans.mynet.com/doviz/")

soup = BeautifulSoup(response.content, "html.parser")

tbl = soup.find("tbody", class_="tbody-type-default")


rows = tbl.find_all("tr")

currency_reply = ""
for count,row in enumerate(rows):
    if "change-down" in row.span["class"]:
        sign = "⬇️"
    else:
        sign = "⬆️"
    
    head = row.text.strip().split("\n\n\n\n\n")[0]
    buy, sale, dont_use, percentage, time = row.text.strip().split("\n\n\n\n\n")[1].split()
    currency_list.append((head, sign, buy, sale, f"{percentage} %", time))
    currency_reply += f"\n<strong>{head}</strong> {sign}\nBuy: {buy}\nSale: {sale}\nDifferance:{percentage} %\nLast Update: {time}\n{'-'*10}"






