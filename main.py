import locale
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import csv
import os

def getLink(post_date) -> str:
    locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8')

    post_date_obj = datetime.strptime(post_date, '%Y-%m-%d')

    days_until_monday = (7 - post_date_obj.weekday() + 7) % 7

    if days_until_monday == 0:
        days_until_monday = 7

    next_monday = post_date_obj + timedelta(days=days_until_monday)

    following_sunday = next_monday + timedelta(days=6)

    if next_monday.month != following_sunday.month:
        week_range = f"{next_monday.day}-de-{next_monday.strftime('%B').lower()}-a-{following_sunday.day}-de-{following_sunday.strftime('%B').lower()}"
    else:
        week_range = f"{next_monday.day}-a-{following_sunday.day}-de-{next_monday.strftime('%B').lower()}"


    url = 'https://contaspoupanca.pt/carro/combustiveis/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pattern = re.compile(
        rf'/carro/combustiveis/.*-combustiveis--precos-na-proxima-semana--{week_range}--\w+'
    )

    for link in soup.find_all('a', href=True):
        href = link['href']
        if pattern.search(href) and '?' not in href:
            return 'https://contaspoupanca.pt' + href
    return None

def getPrices(url) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    prices = {}

    gasolina_element = soup.find('span', string=re.compile(r'Gasolina'))
    gasoleo_element = soup.find('span', string=re.compile(r'Gasóleo'))

    if gasolina_element:
        gasolina_text = gasolina_element.find_next('span').text
        gasolina_variation = re.search(r'\(([-+]?\d+)', gasolina_text)
        if gasolina_variation:
            prices['Gasolina'] = gasolina_variation.group(1)

    if gasoleo_element:
        gasoleo_text = gasoleo_element.text
        gasoleo_variation = re.search(r'Gasóleo \(([-+]?\d+)', gasoleo_text)
        if gasoleo_variation:
            prices['Gasóleo'] = gasoleo_variation.group(1)

    return prices

def writeCSV(date, prices, path):
    new_row = [date, prices.get('Gasolina', 'N/A'), prices.get('Gasóleo', 'N/A')]
    
    if os.path.exists(path):
        with open(path, 'r', newline='', encoding='utf-8') as file:
            existing_data = file.readlines()
        
        with open(path, 'w', newline='', encoding='utf-8') as file:
            file.write(f"{date};{new_row[1]};{new_row[2]}\n")
            file.writelines(existing_data)
    else:
        with open(path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['date', 'gasolina', 'gasoleo'])
            writer.writerow(new_row)


if __name__ == '__main__':
    print(getLink('2025-01-24'))
