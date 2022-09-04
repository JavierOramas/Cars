import json
from os import path
import os
from urllib import request
import requests
from bs4 import BeautifulSoup

def get_all_cars(dump=True):

    url = 'https://www.auto-data.net/en/allbrands'
    base = 'https://www.auto-data.net'

    print(f"Starting scraping of {url}")
    # get brands names
    response = requests.get(url)

    if response.status_code == 200:
        print("Main Page Loaded")
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all("div", {"class":"brands"})
        print("getting separate brands")
        models = {}
        brands = []
        for div in divs:
            # print(div.text)
            if div != None:
                brands += div.find_all("a", {"class":"marki_blok"})
        print("got brands")
        print("count: ", len(brands))

        json_data = {}

        for brand in brands:
            link = 'https://www.auto-data.net/'+brand.get('href')
            
            brand_page = requests.get(link)
            if brand_page.status_code == 200:
                brand_soup = BeautifulSoup(brand_page.text, 'html.parser')
                models = brand_soup.find_all('a', {"class": "modeli"})
                
                for model in models:
                    print("model: ", model.text)
                    model_page = requests.get(base+model.get("href"))
                    if model_page.status_code == 200:
                        model_soap = BeautifulSoup(model_page.text, "html.parser")
                        sub_models = model_soap.find_all("td", {"class":"i"})
                        for sub_model in sub_models:
                            print("sub model"+sub_model.text)
                            sub_model_link = sub_model.find("a").get("href")
                            
                            print(base+sub_model_link)
                            sub_model_page = requests.get(base+sub_model_link)
                            
                            if sub_model_page.status_code == 200:
                                sub_model_soup = BeautifulSoup(sub_model_page.text, "html.parser")
                                
                                carslist = sub_model_soup.find("table", {"class":"carlist"})
                                
                                # print("carlist: ",carslist)

                                if carslist != None:
                                    carslist = carslist.find_all("th", {"class":"i"})

                                    print("\ncarlist: ",carslist)
                                    
                                    carslist_links = []
                                    for car in carslist:
                                        carslist_links += car.find_all("a")

                                    print("\ncarlist_links: ",carslist_links)

                                    for car in carslist_links:
                                        print("car "+car.text)
                                        html = car.get("href")
                                        html = 'https://www.auto-data.net' + html
                                        print("\n Car page: ", html)
                                        

                                        details_page = requests.get(html)
                                        if details_page.status_code == 200:
                                            details_soup = BeautifulSoup(details_page.text, "html.parser")
                                            details = details_soup.find("table", {"class":"cardetailsout"})
                                            details = details.find_all("tr")
                                            car_json = {}
                                            for row in details:
                                                try:
                                                    key = row.find("th").text.strip()
                                                    value = row.find("td").text.strip()
                                                    car_json[key] = value
                                                except:
                                                    pass
                                            print("\n\nCar Json: ", car_json)
                                            # replace " " with _ in brand
                                            car_json["Brand"] = car_json["Brand"].replace(" ", "_")
                                            car_json["Model"] = car_json["Model"].replace(" ", "_")
                                            car_json["Generation"] = car_json["Generation"].replace(" ", "_")
                                            # create folder for model if not exists
    
                                            image = details_soup.find("img", {"class":"inspecs"})
                                            # dowload image
                                            if image != None:
                                                image = image.get("src")
                                                image = 'https://www.auto-data.net' + image
                                                print("image: ", image)
                                                image_name = image.split("/")[-1]
                                                image_name = image_name.split("?")[0]
                                                print("image_name: ", image_name)
                                                image_path = f"images/{car_json['Brand']}/{car_json['Model']}"
                                                if not os.path.exists(image_path):
                                                    os.makedirs(image_path)
                                                image_path = f"{image_path}/{image_name}"
                                                print("image_path: ", image_path)
                                                request.urlretrieve(image, image_path)
                                                car_json["image"] = image_path
    
    
                                            if not os.path.exists(f'cars/{car_json["Brand"]}'):
                                                print("creating folder for brand")
                                                os.mkdir(f"cars/{car_json['Brand']}")
                                            if not os.path.exists(f'cars/{car_json["Brand"]}/{car_json["Model"]}'):
                                                print("creating folder for model")
                                                os.mkdir(f"cars/{car_json['Brand']}/{car_json['Model']}")

                                            path = f'cars/{car_json["Brand"]}/{car_json["Model"]}/{car_json["Generation"]}.json'
                                            with open(path, 'w') as f:
                                                f.write(json.dumps(car_json, indent=4))
get_all_cars()