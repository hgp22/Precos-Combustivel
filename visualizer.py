import matplotlib.pyplot as plt
import csv
import numpy as np
import argparse

def read_csv(file_path):
    weeks = []
    gasolina_values = []
    gasolina_signs = []
    gasoleo_values = []
    gasoleo_signs = []

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header row
        for row in reader:
            week = row[0]
            gasolina = row[1].replace(',', '.') if row[1] != 'N/A' else '0'
            gasoleo = row[2].replace(',', '.') if row[2] != 'N/A' else '0'

            weeks.append(week)

            if gasolina.startswith('+'):
                gasolina_values.append(float(gasolina[1:]))
                gasolina_signs.append(1)
            elif gasolina.startswith('-'):
                gasolina_values.append(float(gasolina[1:]))
                gasolina_signs.append(-1)
            else:
                gasolina_values.append(float(gasolina))
                gasolina_signs.append(1)

            if gasoleo.startswith('+'):
                gasoleo_values.append(float(gasoleo[1:]))
                gasoleo_signs.append(1)
            elif gasoleo.startswith('-'):
                gasoleo_values.append(float(gasoleo[1:]))
                gasoleo_signs.append(-1)
            else:
                gasoleo_values.append(float(gasoleo))
                gasoleo_signs.append(1)

    return weeks, gasolina_values, gasolina_signs, gasoleo_values, gasoleo_signs

def calculate_prices(values, signs):
    variations = np.array(values) * np.array(signs)
    prices = np.cumsum(variations)
    return prices

def generate_graph(weeks, gasolina_values, gasolina_signs, gasoleo_values, gasoleo_signs, output_path):
    gasolina_prices = calculate_prices(gasolina_values, gasolina_signs)
    gasoleo_prices = calculate_prices(gasoleo_values, gasoleo_signs)

    plt.figure(figsize=(12, 6))

    # Plot gasolina prices
    plt.plot(weeks, gasolina_prices, marker='o', label='Gasolina', color='blue', linestyle='-', linewidth=2)

    # Plot gasoleo prices
    plt.plot(weeks, gasoleo_prices, marker='o', label='Gasóleo', color='green', linestyle='-', linewidth=2)

    plt.xlabel('Semana')
    plt.ylabel('Preço acumulado')
    plt.title('Variação dos Preços de Gasolina e Gasóleo')
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, linestyle='--', alpha=0.7)  # Add a grid for better readability
    plt.tight_layout()

    plt.savefig(output_path)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a graph from a CSV file.')
    parser.add_argument('input_csv', type=str, help='Path to the input CSV file')
    parser.add_argument('output_image', type=str, help='Path to the output image file')

    args = parser.parse_args()

    weeks, gasolina_values, gasolina_signs, gasoleo_values, gasoleo_signs = read_csv(args.input_csv)
    generate_graph(weeks, gasolina_values, gasolina_signs, gasoleo_values, gasoleo_signs, args.output_image)
