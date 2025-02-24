import matplotlib.pyplot as plt
import csv
import numpy as np

def read_csv(file_path):
    weeks = []
    gasolina_prices = []
    gasoleo_prices = []

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header row
        for row in reader:
            week = row[0]
            gasolina = row[1].replace(',', '.') if row[1] != 'N/A' else None
            gasoleo = row[2].replace(',', '.') if row[2] != 'N/A' else None

            weeks.append(week)
            gasolina_prices.append(float(gasolina) if gasolina else np.nan)
            gasoleo_prices.append(float(gasoleo) if gasoleo else np.nan)

    return weeks, gasolina_prices, gasoleo_prices

def fill_na_with_last_value(prices):
    prices = np.array(prices)  # Convert to numpy array
    for i in range(1, len(prices)):
        if np.isnan(prices[i]):
            prices[i] = prices[i - 1]
    return prices

def generate_graph(weeks, gasolina_prices, gasoleo_prices, output_path):
    gasolina_prices = fill_na_with_last_value(gasolina_prices)
    gasoleo_prices = fill_na_with_last_value(gasoleo_prices)

    plt.figure(figsize=(10, 5))

    # Plot gasolina prices
    plt.plot(weeks, gasolina_prices, marker='o', label='Gasolina', color='blue')

    # Plot gasoleo prices
    plt.plot(weeks, gasoleo_prices, marker='o', label='Gasóleo', color='green')

    plt.xlabel('Semana')
    plt.ylabel('Preço')
    plt.title('Variação dos Preços de Gasolina e Gasóleo')
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig(output_path)
    plt.show()

if __name__ == '__main__':
    file_path = 'prices.csv'
    output_path = 'prices_graph.png'

    weeks, gasolina_prices, gasoleo_prices = read_csv(file_path)
    generate_graph(weeks, gasolina_prices, gasoleo_prices, output_path)