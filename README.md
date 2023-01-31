# Projekt-IO
## Opis
Projekt ma na celu zbudowanie aplikacji webowej, która ma ułatwić zakupy internetowe. 

### UML działania aplikacji

![image](https://user-images.githubusercontent.com/48855984/202875575-943e1324-acc2-4f01-8d02-9344975bf825.png)

### przedmioty.json
```
{
 "id"               :"int"
 "nazwa"            :"string",
 "cena"             :"float",
 "cena_dostawy"     :"float",
 "sklep"            :"string",
 "link"             :"string"
}
```

### nazwy.txt
```txt
nazwa1
nazwa2
nazwa3
.
.
nazwan
```

### lokalna baza danych
![image](https://user-images.githubusercontent.com/48855984/214115030-ef674153-a5af-438d-8e5b-31c1d2ed717c.png)

### zasada działania (wstępna)
Otrzymujemy pliki.json, łączymy w megaliste, wyniki wyświetlamy domyślnie posortowane po cenie (osobno różne typy zabawek), jeżeli będzie sortowanie po dostawcy to wyniki od tych samych dostawców się mergują.

## How to start

Aby uruchomić aplikację, potrzebujesz dockera.

```bash
  docker compose up -d
```

Powyższa komenda automatycznie buduje i uruchamia kontener aplikacji i bazę danych

## Dokumentacja
### stronka
Folder, w którym snajduje się kod źródłowy strony.
### ceneo
Folder, w którym znajduje się mechanizm pobierający dane na serwisie ceneo. 
Pliki:
- chromedriver - silnik wyszukiwarki chrome dla urządzeń Linux
- chromedriver.exe - silnik wyszukiwarki chrome dla urządzeń Windows
- `main.py`, `my_ceneo.py` - moduły w których napisany jest mechanizm szukający

### static i templates
Foldery, w których napisany jest frontend strony. Zawiera:
- css
- html
- obrazki
- pliki wysłane na serwer

### Moduły:
- `algorithmSort.py` - algorytm który jest używany do dobierania najtańszych produktów i produktów z najmniejszej ilości sklepów
- `forms.py` - formularze używane do logowania i rejestracji
- `models.py` - architektura bazy danych
- `routes.py` - warstwa komunikacji frontendu z backendem
- `sendmail.py` - moduł wysyłający mail potwierdzający