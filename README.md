# Scraper de Preços de Combustíveis

Script em Python que faz scrape dos preços do combustível, do website do [Contas Poupança](https://contaspoupanca.pt/carro/combustiveis).
Que tem como objetivo colocar no final de um ficheiro de CSV (e criar se este não existir) os preços da gasolina e gasóleo.

## Automatização

Basta executar o script `setjob.py` para adicionar um cronjob que executa todas as sextas feiras às 2000.

## TODO

- [x] Fazer vários cronjobs durante o fim de semana (caso o post saia mais tarde do que o habitual)
- [x] Verificar se a data já se encontra no csv para não estar sempre a reescrever os mesmos valores.
