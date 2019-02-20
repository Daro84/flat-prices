Skrypt pobierający aktualne dane z jednego z wiodących portali ogłoszeniowych w Polsce.
Opiera się na webscrapingu z wykorzystaniem bibliotek Pandas i BeautifulSoup. 
W przypadku dużych miast pobieranie może chwilę potrwać (np. w przypadku Warszawy skrypt ma do przeskanowania ok. 350 stron).
Zwracane dane to: cena mieszkania, powierzchnia, dzielnica/osiedle, piętro. 
Opcjonalnie jest możliwość wyeksportowania danych do formatu .xlsx lub .csv.