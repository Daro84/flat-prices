import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import os

# określenie miasta, dla którego mają zostać pobrane ceny
city = 'Warszawa'

# ustalenie liczby stron, które skrypt będzie musiał przeskanować
r = requests.get('https://www.oferty.net/mieszkania/szukaj?ps%5Blocation%5D%5Btype%5D=1&ps%5Btype%5D=1&ps%5B'\
                'transaction%5D=1&ps%5Blocation%5D%5Btext%5D=' + city)
c = r.content
soup = BeautifulSoup(c, 'html.parser')
last_page = int(soup.find_all('li',{'class': 'navigate'})[-1].text.strip('\n'))
print("Liczba stron w serwisie 'oferty.net' z ofertami mieszkań w mieście {}: {}".format(city,last_page))


# utworzenie obiektu Pandas DataFrame i nadanie struktury danym
offers_df = pd.DataFrame(columns=['district', 'area', 'floor', 'price'])

# skanowanie poszczególnych stron i zbieranie danych
for i in range(1, last_page + 1):
    # utworzenie obiektu Pandas DataFrame dla pojedynczej strony
    offers = pd.DataFrame()

    # użycie funkcji Pandas.read_html do pobrania wszystkich danych z pojedynczej strony html
    data = pd.read_html(
        'https://www.oferty.net/mieszkania/szukaj?ps%5Blocation%5D%5Btype%5D=1&ps%5Blocation%5D%5Btext%5D='
        + city + '&ps%5Btype%5D=1&ps%5Btransaction%5D=1&page=' + str(i))

    # usunięcie zbędnych kolumn
    data[0].drop(['foto', 'ulica', 'l. pokoi', 'cena m²'], axis=1, inplace=True)
    df = data[0][1:]

    # utworzenie kolumny 'district' (zmienna typu string) poprzez wyekstraktowanie nazwy dzielnicy/osiedla
    offers['district'] = df['gmina/dzielnica'].apply(lambda x: str(x).split('myTools')).apply(
        lambda x: x[0].split(',') if x else np.nan).apply(lambda x: x[-1])

    # utworzenie kolumny 'area' i przekształcenie zmiennej na typ float
    offers['area'] = df['pow. m²'].apply(lambda x: str(x).replace(' m²', '').replace(',', '.')).apply(float)

    # utworzenie kolumny 'floor' i przekształcenie zmiennej na typ float
    offers['floor'] = df['piętro'].apply(lambda x: str(x).replace('parter', '0')).apply(float)

    # utworzenie kolumny 'price' i odfiltrowanie ogłoszeń w których cena nie jest precyzyjnie określona;
    # przekształcenie zmiennej na typ float
    offers['price'] = df['cena PLN'].apply(lambda x: x if not str(x).startswith(('inf', 'ok')) else np.nan)
    offers['price'] = offers['price'].apply(lambda x: str(x).replace(' PLN', '').replace(' ', '')).apply(float)

    # usunięcie wierszy z brakami danych
    offers.dropna(inplace=True)

    # konkatenacja wyników pobranych dla danej strony ze zbiorczą tabelą
    offers_df = pd.concat([offers_df, offers])

# ustalenie nowego indeksu dla zbiorczej tabeli ze wszystkimi ofertami i zwrócenie informacji z całkowitą
# liczbą pobranych ofert w danym mieście
offers_all = offers_df.reset_index(drop=True)
print('Liczba ofert mieszkań w mieście {}: {}'.format(city, len(offers_all)))


# ustalenie formatu pliku, w jakim dane mają zostać zapisane (.xlsx lub .csv) oraz podanie ścieżki na dysku
file_format = '.xlsx'
path = r'C:\flat_prices'
if not os.path.exists(path):
    os.mkdir(path)

# utworzenie ostatecznej nazwy pliku i stworzenie pełnej ścieżki
file = 'prices_' + city + file_format
full_path = os.path.join(path, file)

# zapisanie pliku na dysku w zadeklarowanym formacie
if file_format == '.xlsx':
    offers_all.to_excel(full_path)
elif file_format == '.csv':
    offers_all.to_csv(full_path)