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
 "cena dostawy"     :"float",
 "dostawca"         :"string",
 "czas_dostarczenia":"time",
 "link"             :"string"
}
```

### nazwy.csv
`nazwa1, nazwa2, nazwa3, ..., nazwan`

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
