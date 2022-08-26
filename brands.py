import urllib.request
import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.auto-data.net/en/allbrands'

print(f"Starting scraping of {url}")

# get brands names
response = requests.get(url)

if response.status_code == 200:
    print("Main Page Loaded")
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all("div", {"class":"brands"})
    print("getting separate brands")
    brands = []
    for div in divs:
        # print(div.text)
        if div != None:
            brands += div.find_all("a", {"class":"marki_blok"})
    print("got brands")
    print(len(brands))
    
    json_data = {}
    
    for brand in brands:
        print(brand)
        name = brand.get('title')
        name = name[:name.find('-')-1]
        
        img = brand.find("img").get("src")
        
        url = "https://www.auto-data.net/"
        urllib.request.urlretrieve(url+img, f"img/{name}.jpg")
        
        json_data[name] = name+".jpg"
        
    # dump json_data to brands.json
    with open('brands.json', 'w') as outfile:
        json.dump(json_data, outfile)