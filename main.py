from typer import Typer
import json
from bs4 import BeautifulSoup
import requests
import urllib.request
from brands import get_brands_and_images

app = Typer()

@app.command('brands')
def get_brands():
    brands = get_brands_and_images(dump=False)

@app.command('cars')
def get_all_cars():
    return {}

if __name__ == '__main__':
    app()