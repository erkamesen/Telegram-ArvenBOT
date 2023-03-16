import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.turksat.com.tr/tr/turksat-frekans-listesi")

soup = BeautifulSoup(response.content, "html.parser")


tb = soup.find("table", class_="vgt-table bordered ")

print(tb)