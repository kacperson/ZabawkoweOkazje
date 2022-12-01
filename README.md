# Projekt-IO
## Opis
Projekt ma na celu zbudowanie aplikacji webowej, która ma ułatwić zakupy internetowe.

### UML działania aplikacji

![image](https://user-images.githubusercontent.com/48855984/202875575-943e1324-acc2-4f01-8d02-9344975bf825.png)

### przedmioty.json
```
{
 "nazwa"            :"string",
 "cena"             :"float",
 "dostawca"         :"string",
 "sklep"            :["allegro","ceneo"],
 "czas_dostarczenia":"time",
 "link"             :"string"
}
```

### nazwy.csv
`nazwa1, nazwa2, nazwa3, ..., nazwan`

### lokalna baza danych
![image](https://user-images.githubusercontent.com/48855984/202875828-defdb5cf-73ba-45fd-b48b-4b2647d95c05.png)

### zasada działania (wstępna)
Otrzymujemy pliki.json, łączymy w megaliste, wyniki wyświetlamy domyślnie posortowane po cenie (osobno różne typy zabawek), jeżeli będzie sortowanie po dostawcy to wyniki od tych samych dostawców się mergują.

