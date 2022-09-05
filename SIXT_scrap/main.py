import requests
from bs4 import BeautifulSoup
import json
import os

url = 'https://www.hertz.es/rentacar/vehicleguide/index.jsp?targetPage=vehicleGuideHomeView.jsp&countryCode=MX&category=Coche%20est%C3%A1ndar'

def get_car_data(url):
    codes = []
    class_codes = 'select destination country'
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    codes_soup = soup.find("select", {"aria-label":class_codes})
    codes = codes_soup.find_all('option')
    codes = [code.get('value') for code in codes]
    
    code_length = len(codes)
    count = 0
    for code in codes:
        count += 1
        print(count,"/",code_length)
        base_url = f'https://www.hertz.es/rentacar/vehicleguide/index.jsp?targetPage=vehicleGuideHomeView.jsp&countryCode={code}&category=Coche%20est%C3%A1ndar'
        print("Scraping Country:", code)
        print("URL:", base_url)
        
        page = requests.get(base_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        car_types = soup.find("ul", {"class":"multiLevelTabUL"})
        if car_types is None:
            continue
        links = [link.get("href") for link in car_types.find_all('a')]

        for link in links:
            category_page = requests.get("https://www.hertz.es/rentacar/vehicleguide/"+link)
            category_soup = BeautifulSoup(category_page.text, 'html.parser')
            
            cars = category_soup.find_all("div", {"class":"vgVehicle"})
            
            for car in cars:
                
                
                car_json = {}
                car_json['Brand'] = car.find("div", {"class":"vgVehicleNameOnly"}).text.replace(" ", "_").replace("\n", "").replace("\t", "")
                
                print(car_json['Brand'])
                print()
                
                car_json["Description"] = [car.find("div", {"class":"vgSippDescription gblRemoved"}).text]
                try:
                    car_json["FuelEco"] = car.find("span", {"class":"vgFuelEco"}).text
                except:
                    car_json["FuelEco"] = "N/D"
                
                car_json["Description"].append(car.find("div", {"class":"vgVehicleAmenities"}).text)
                image_path = car.find("div", {"class":"gblRemoved vgPopupImagePath"}).text
                image_name = image_path.split("/")[-1]
                car_json['Image'] = "images/" + car_json['Brand'] + "_" + image_name.replace("/", "_") + ".jpg"
                
                details = car.find("div", {"class":"vgCarFeatures gblRemoved"})
                details = details.find_all("li")
                car_json["Details"] = []
                for detail in details:
                    car_json["Details"].append(detail.text)

                # download image in car_json['Image'] path
                image = requests.get(image_path)

                # create folder if not exists
                if not os.path.exists("images"):
                    print("creating images Directory")
                    os.makedirs("images")

                with open(car_json['Image'], 'wb') as f:
                    f.write(image.content)

                if not os.path.exists("cars"):
                    print("creating cars Directory")
                    os.makedirs("cars")

                # dump json to cars folder
                with open('cars/' + car_json['Brand'] + '.json', 'w') as outfile:
                    json.dump(car_json, outfile, indent=4)
                
get_car_data(url)