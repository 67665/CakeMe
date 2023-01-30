import requests
from bs4 import BeautifulSoup
import urllib.request, re
from bs4 import *
from dataclasses import dataclass
from urllib.request import urlopen
from collections import OrderedDict #dla obrazkow zeby sie nie powtarzaly
from itertools import zip_longest #zeby miec wszystkie elementy w classie
#wczytanie obrazkow
from IPython.display import Image
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import urllib
import numpy as np
import cv2


link = "https://www.allrecipes.com/recipes/276/desserts/cakes/"
page = urllib.request.urlopen(link)
kod=page.read().decode('utf-8')

soup = BeautifulSoup(kod, 'html.parser')

linki = []
elements = soup.find_all('a', attrs={'id': lambda x: x and x.startswith('mntl-card-list-items_')})
for element in elements:
    linki.append(element['href'])
linki

obrazki = OrderedDict()
img_tags = soup.find_all('img', class_='card__img')
for img in img_tags:
    url = img.get('src', img.get('data-src'))
    obrazki[url] = None

obrazki = list(obrazki.keys())

for obraz in obrazki:
    print(obraz)
print(len(obrazki))


span_tags = soup.find_all('span', class_='card__title-text')
tytuly = [span.text for span in span_tags]
print(tytuly)
print(len(tytuly))
#lematyzacja

#wczytanie pliku tekstowego
import urllib.request
strona = urllib.request.urlopen("https://lewoniewski.info/diffs.txt")
linie = [linia.decode("utf-8") for linia in strona.readlines()]

slownik = {}
for linia in linie:
  klucz, wartosc = linia.split()
  slownik[klucz] = wartosc

def lematyzacja(slowa):
  return [slownik.get(slowo, slowo) for slowo in slowa]
#tokenizacja
import string
#interpunkcje=string.punctuation
interpunkcje = "!'#$%&()*+,-./:;<=>?®@[\\]^_`{|}~"
def tokenizacja(s):
  for znak in interpunkcje:
      s = s.replace(znak," ")
  slowa = s.strip().split()
  return [slowo for slowo in slowa]

skladniki = []
for link in linki:
  page1 = urllib.request.urlopen(link)
  kod=page1.read().decode('utf-8')
  soup = BeautifulSoup(kod)
  s_html = soup.find_all("span", {"data-ingredient-name": "true"})
  skladniki_przepis = []
  for s in s_html:
    s_przepis = s.text.lower()
    s_przepis = tokenizacja(s_przepis)
    [skladniki_przepis.append(skladnik) for skladnik in s_przepis]
  skladniki_przepis = lematyzacja(skladniki_przepis)
  skladniki.append(skladniki_przepis)
skladniki


tresci = []
for link in linki:
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")
    ele2 = soup.find("div", {"id": "recipe__steps_1-0"})
    element2 = ele2.text.replace("\n\n\n", "\n")
    ele1 = soup.find("div", {"id": "mntl-structured-ingredients_1-0"})
    element1 = ele1.text.replace("\n\n\n", "\n")
    element = element1 + element2
    tresci.append(element)

print(tresci[3])


class Przepis:
    def __init__(self, link, obrazek, tytul, skladniki, tresc):
        self.link = link
        self.obrazek = obrazek
        self.tytul = tytul
        self.skladniki = skladniki
        self.tresc = tresc
    def __repr__(self):
      return f"{self.tytul} {self.link} {self.obrazek} {self.skladniki} {self.tresc}"

    def czy_zawiera_skladniki(self, ingredients):
      return set(ingredients).issubset(self.skladniki)

    def drukuj(self):
        print("Tytul: ", self.tytul)
        print("Obrazek: ", self.obrazek)
        print("Link: ", self.link)
        print("Tresc: ", self.tresc)

ingredients = tokenizacja(input().lower())
ingredients = lematyzacja(ingredients)

przepisy = []
for link, obrazek, tytul, skladnik, tresc in zip(linki, obrazki, tytuly, skladniki, tresci):
    przepis = Przepis(link, obrazek, tytul, skladnik, tresc)
    przepisy.append(przepis)

f_przepisy = [p for p in przepisy if p.czy_zawiera_skladniki(ingredients)]
print(f"Liczba przepisów: {len(f_przepisy)}")

def wczytanie_obrazka(url):
    with urllib.request.urlopen(url) as url:
      s = url.read()
    img = cv2.imdecode(np.frombuffer(s, np.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    imshow(np.transpose(img, (1, 0, 2)))
    plt.axis('off')
    plt.show()


if f_przepisy == []:
  print("Na stronie nie ma przepisu z podanymi składnikami" )
for p in f_przepisy:
  print(p.tytul)
  print(p.link)
  wczytanie_obrazka(p.obrazek)
  print(p.tresc)


