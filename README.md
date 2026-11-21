# Wyznaczanie optymalnej trasy w problemie komiwojażera za pomocą algorytmów ewolucyjnych

# Truck Route Optimizer

Aplikacja służąca do optymalizacji tras przejazdu samochodu ciężarowego z wykorzystaniem **algorytmu genetycznego**. Projekt został przygotowany w ramach przedmiotu *Algorytmy ewolucyjne*.

Program pozwala wybrać miasto początkowe, miasto docelowe oraz profil pojazdu, a następnie wykorzystuje algorytm genetyczny do poszukiwania korzystnej trasy w symulowanej sieci drogowej.

W procesie optymalizacji uwzględniane są między innymi czas przejazdu, zużycie paliwa, ograniczenia pojazdu oraz warunki panujące na poszczególnych odcinkach dróg.

## 1. Cel projektu

Głównym celem projektu jest praktyczne przedstawienie zastosowania algorytmów ewolucyjnych do rozwiązywania problemów optymalizacji tras transportowych.

Program wykorzystuje populację potencjalnych rozwiązań, które są stopniowo ulepszane za pomocą mechanizmów charakterystycznych dla algorytmów genetycznych:

- tworzenia populacji początkowej,
- oceny jakości osobników,
- selekcji,
- krzyżowania,
- mutacji,
- zachowania najlepszych rozwiązań.

Każdy osobnik reprezentuje możliwą trasę przejazdu ciężarówki pomiędzy wybranymi miastami.

Warto zaznaczyć, że zastosowany model stanowi wariant problemu wyznaczania trasy w sieci drogowej pomiędzy określonym punktem początkowym i docelowym. Nie jest to klasyczna wersja problemu komiwojażera, w której wymagane jest odwiedzenie wszystkich miast.

## 2. Wykorzystane technologie

| Technologia | Zastosowanie |
|---|---|
| Python | Główny język programowania |
| DEAP | Framework do tworzenia i uruchamiania algorytmów ewolucyjnych |
| NetworkX | Reprezentacja i obsługa grafu drogowego |
| Matplotlib | Wizualizacja sieci drogowej i wyznaczonej trasy |
| Tkinter | Graficzny interfejs użytkownika |

**Ważne rozróżnienie dotyczące wkładu własnego:**

Biblioteka DEAP dostarcza infrastrukturę algorytmu genetycznego, w tym mechanizmy selekcji, zarządzania populacją, przechowywania najlepszych osobników i obsługi funkcji przystosowania.

Logika związana z konkretnym problemem transportowym została opracowana w ramach projektu. Dotyczy to między innymi reprezentacji tras, ich generowania, walidacji, obliczania parametrów przejazdu oraz dostosowanych do problemu operatorów krzyżowania i mutacji.

## 3. Model sieci drogowej

Sieć drogowa została przedstawiona w postaci skierowanego grafu ważonego z wykorzystaniem biblioteki NetworkX.

- Wierzchołki reprezentują miasta.
- Krawędzie reprezentują bezpośrednie połączenia drogowe.
- Atrybuty krawędzi opisują parametry poszczególnych odcinków.

Aktualna sieć symulacyjna zawiera:

- **32 miasta**,
- **62 fizyczne połączenia drogowe**,
- **124 skierowane krawędzie** – po jednej dla każdego kierunku przejazdu.

Wśród miast znajdują się między innymi:

Warszawa, Kraków, Katowice, Wrocław, Poznań, Szczecin, Gdańsk, Gdynia, Olsztyn, Białystok, Lublin, Rzeszów, Łódź, Toruń, Bydgoszcz, Kielce, Opole, Tarnów i Nowy Sącz.

Każdy odcinek drogi może posiadać następujące parametry:

- długość w kilometrach,
- dopuszczalną prędkość,
- maksymalną dopuszczalną masę pojazdu,
- maksymalną wysokość pojazdu,
- maksymalną szerokość pojazdu,
- maksymalną długość pojazdu,
- współczynnik natężenia ruchu,
- współczynnik robót drogowych,
- informację o zamknięciu drogi.

Sieć jest modelem symulacyjnym, a nie bezpośrednim odwzorowaniem aktualnych danych z OpenStreetMap.

Rozmieszczenie miast na wizualizacji ma charakter schematyczny i służy przedstawieniu układu połączeń.

## 4. Model pojazdu

Program umożliwia wybór jednego z przygotowanych profili pojazdów ciężarowych:

- MAN TGX,
- Lekka ciężarówka,
- Zestaw ciężarowy.

Każdy profil posiada parametry wykorzystywane podczas sprawdzania możliwości przejazdu przez dany odcinek.

Uwzględniane są:

- masa własna pojazdu,
- dopuszczalna masa całkowita (DMC),
- masa ładunku,
- rzeczywista masa całkowita,
- wysokość,
- szerokość,
- długość,
- średnie zużycie paliwa.

Rzeczywista masa całkowita pojazdu obliczana jest według zależności:

`masa całkowita = masa własna + masa ładunku`

Przed wykorzystaniem odcinka w trasie sprawdzane jest, czy pojazd spełnia jego ograniczenia.

Odcinek może zostać odrzucony, jeżeli przykładowo:

- droga jest zamknięta,
- rzeczywista masa całkowita pojazdu przekracza dopuszczalną masę na drodze,
- wysokość pojazdu przekracza ograniczenie,
- szerokość lub długość pojazdu przekracza dopuszczalne wartości.

Dzięki temu algorytm nie ogranicza się wyłącznie do poszukiwania najkrótszej drogi. Musi również uwzględniać możliwość przejazdu wybranym pojazdem.

## 5. Reprezentacja osobnika

W algorytmie genetycznym pojedynczy osobnik reprezentuje kompletną trasę przejazdu.

Trasa jest zapisana jako lista kolejnych miast, przykładowo:

```python
[
    "Warszawa",
    "Łódź",
    "Katowice"
]
```

Pierwszy element listy oznacza miasto początkowe, a ostatni miasto docelowe.

Pozostałe elementy określają miasta pośrednie.

Poprawny osobnik powinien spełniać następujące warunki:

- rozpoczynać się w wybranym mieście początkowym,
- kończyć się w wybranym mieście docelowym,
- korzystać wyłącznie z istniejących połączeń drogowych,
- nie zawierać powtarzających się miast,
- uwzględniać ograniczenia wybranego pojazdu.

Zastosowanie takiej reprezentacji pozwala bezpośrednio interpretować osobnika jako trasę przejazdu.

## 6. Działanie algorytmu genetycznego

Algorytm rozpoczyna działanie od wygenerowania populacji początkowej, czyli zestawu potencjalnych tras.

Następnie wykonywane są kolejne generacje, w których osobniki podlegają ocenie i operacjom ewolucyjnym.

### 6.1. Generowanie populacji początkowej

Na początku tworzona jest populacja poprawnych tras pomiędzy wskazanymi miastami.

Do generowania tras wykorzystywany jest algorytm przeszukiwania wszerz (BFS – Breadth-First Search).

W implementacji zastosowano losową kolejność odwiedzania sąsiadów, co pozwala uzyskiwać różne warianty tras.

BFS uwzględnia:

- strukturę grafu,
- istnienie połączeń drogowych,
- ograniczenia wybranego pojazdu,
- zakaz ponownego odwiedzania już rozpatrzonych wierzchołków w ramach jednego przeszukiwania.

Algorytm BFS znajduje przejezdną ścieżkę o najmniejszej liczbie odcinków w danym przeszukiwaniu. Nie oznacza to jednak, że musi być ona najkrótsza czasowo lub pod względem dystansu.

Optymalizacja czasu i zużycia paliwa jest realizowana przez właściwy algorytm genetyczny.

### 6.2. Funkcja oceny

Każdy osobnik jest oceniany na podstawie parametrów reprezentowanej trasy.

W projekcie uwzględniane są dwa kryteria:

1. **Czas przejazdu** – wyznaczany na podstawie długości odcinków, dopuszczalnych prędkości oraz współczynników utrudnień.
2. **Zużycie paliwa** – obliczane na podstawie długości trasy i średniego spalania wybranego pojazdu.

Celem jest minimalizacja czasu przejazdu, a następnie zużycia paliwa.

Funkcja przystosowania jest reprezentowana jako dwuelementowa krotka:

```python
(time_hours, fuel_liters)
```

W bibliotece DEAP zastosowano wagi:

```python
weights = (-1.0, -1.0)
```

Oznaczają one minimalizację obu kryteriów.

**Istotne jest jednak to, że kryteria są porównywane leksykograficznie, a nie metodą Pareto.**

Oznacza to, że:

1. W pierwszej kolejności porównywany jest czas przejazdu.
2. Jeżeli czasy są jednakowe, rozstrzygające staje się zużycie paliwa.

W praktyce czas przejazdu ma zatem wyższy priorytet niż zużycie paliwa.

### 6.3. Selekcja

Selekcja odpowiada za wybór osobników, które będą uczestniczyły w tworzeniu kolejnego pokolenia.

W projekcie zastosowano selekcję turniejową udostępnianą przez bibliotekę DEAP.

Polega ona na wylosowaniu grupy osobników i wybraniu spośród nich najlepszego według przyjętej funkcji przystosowania.

Lepsze rozwiązania mają dzięki temu większą szansę na przekazanie swoich cech kolejnemu pokoleniu.

### 6.4. Krzyżowanie

Krzyżowanie polega na łączeniu informacji pochodzących od dwóch osobników rodzicielskich.

W projekcie operator krzyżowania:

1. Sprawdza, czy obie trasy mają taki sam punkt początkowy i docelowy.
2. Wyszukuje wspólne miasta pośrednie występujące w obu trasach.
3. Losuje jedno ze wspólnych miast.
4. Wymienia fragmenty tras znajdujące się za wybranym miastem.
5. Sprawdza poprawność otrzymanych potomków.

Jeżeli utworzona trasa zawiera powtarzające się miasta lub nie spełnia warunków przejezdności, zastępowana jest odpowiednim rozwiązaniem rodzicielskim.

Jeśli rodzice nie mają wspólnych miast pośrednich, pozostają bez zmian.

### 6.5. Mutacja

Mutacja wprowadza zmiany w strukturze trasy.

W projekcie polega na zastąpieniu wybranego fragmentu trasy inną poprawną ścieżką.

Operator:

1. Wybiera losową kolejność fragmentów trasy do sprawdzenia.
2. Wyznacza początek i koniec wybranego fragmentu.
3. Wykorzystuje BFS do znalezienia alternatywnego połączenia.
4. Wyklucza z nowej ścieżki pozostałe miasta aktualnej trasy.
5. Sprawdza, czy zmodyfikowana trasa nie zawiera powtórzeń.
6. Weryfikuje poprawność całej trasy.

Początkowe i docelowe miasto przejazdu pozostają bez zmian.

Jeżeli nie uda się znaleźć odpowiedniej alternatywy, zwracana jest oryginalna trasa.

### 6.6. Elitaryzm

W algorytmie zastosowano również elitaryzm.

Polega on na zachowaniu określonej liczby najlepszych osobników i przeniesieniu ich do kolejnej generacji bez konieczności ponownego tworzenia ich przez krzyżowanie lub mutację.

Dzięki temu najlepsze znalezione rozwiązania nie zostają przypadkowo utracone.

### 6.7. Przechowywanie najlepszego rozwiązania

Najlepszy znaleziony osobnik jest przechowywany w strukturze `HallOfFame` udostępnianej przez DEAP.

Struktura ta pozwala zachować najlepsze rozwiązanie znalezione podczas całego przebiegu algorytmu.

Po zakończeniu działania zwracana jest najlepsza znaleziona trasa wraz z obliczonymi parametrami przejazdu.

### 6.8. Zakończenie działania

Algorytm wykonuje określoną liczbę generacji.

Po każdej generacji zapisywane są statystyki opisujące jakość populacji.

Obejmują one między innymi:

- najlepszy czas przejazdu w populacji,
- najgorszy czas przejazdu,
- średni czas przejazdu,
- odchylenie standardowe czasu,
- najlepsze zużycie paliwa,
- najgorsze zużycie paliwa,
- średnie zużycie paliwa,
- odchylenie standardowe zużycia paliwa,
- najlepszy wynik znaleziony dotychczas.

Pozwala to analizować zmiany jakości populacji w kolejnych generacjach.

## 7. Parametry algorytmu

Domyślna konfiguracja wykorzystywana przez interfejs graficzny:

| Parametr | Wartość |
|---|---:|
| Wielkość populacji | 50 |
| Liczba generacji | 100 |
| Prawdopodobieństwo krzyżowania | 0,8 |
| Prawdopodobieństwo mutacji | 0,2 |
| Liczba osobników elitarnych | 2 |
| Rozmiar turnieju | 3 |
| Ziarno generatora losowego | 42 |

Ziarno generatora losowego pozwala uzyskać powtarzalne wyniki przy identycznych danych wejściowych i konfiguracji.

## 8. Obliczanie parametrów przejazdu

Dla każdego odcinka trasy obliczane są parametry przejazdu.

### 8.1. Czas przejazdu

Podstawą obliczeń jest długość odcinka oraz efektywna prędkość przejazdu.

Uwzględniane są współczynniki natężenia ruchu i robót drogowych.

Poziom robót drogowych przyjmuje wartości od 0 do 5:

| Poziom | Opis | Współczynnik |
|---|---|---:|
| 0 | Brak robót | 1,0 |
| 1 | Bardzo małe utrudnienia | 1,1 |
| 2 | Małe utrudnienia | 1,2 |
| 3 | Umiarkowane utrudnienia | 1,4 |
| 4 | Duże utrudnienia | 1,7 |
| 5 | Bardzo duże utrudnienia | 2,0 |

Efektywna prędkość obliczana jest według zależności:

`prędkość efektywna = prędkość dopuszczalna / (współczynnik ruchu × współczynnik robót drogowych)`

Czas przejazdu odcinka obliczany jest na podstawie jego długości i efektywnej prędkości.

### 8.2. Zużycie paliwa

Zużycie paliwa obliczane jest na podstawie długości trasy oraz średniego spalania wybranego pojazdu:

`zużycie paliwa = długość trasy × spalanie / 100`

W obecnym modelu spalanie jest stałe dla danego profilu pojazdu.

Nie jest dynamicznie uzależniane od masy ładunku, nachylenia drogi ani stylu jazdy.

### 8.3. Dystans

Dystans całkowity jest sumą długości wszystkich odcinków tworzących wyznaczoną trasę.

## 9. Interfejs graficzny

Program posiada interfejs graficzny przygotowany z wykorzystaniem biblioteki Tkinter.

Użytkownik może:

1. Wybrać miasto początkowe.
2. Wybrać miasto docelowe.
3. Wybrać profil pojazdu.
4. Zapoznać się z parametrami wybranego pojazdu.
5. Uruchomić optymalizację.
6. Wyświetlić znalezioną trasę na grafie.
7. Odczytać czas przejazdu, dystans i zużycie paliwa.
8. Zobaczyć listę kolejnych przejechanych odcinków.

Dostępny jest również edytor warunków drogowych.

Pozwala on zmieniać parametry odcinków, w tym:

- natężenie ruchu,
- poziom robót drogowych,
- dopuszczalną masę,
- ograniczenia wysokości,
- ograniczenia szerokości,
- ograniczenia długości,
- stan zamknięcia drogi.

Zmiany są stosowane w obu kierunkach danego połączenia i uwzględniane podczas kolejnej optymalizacji.

## 10. Eksperymenty i analiza wyników

Projekt zawiera osobny moduł umożliwiający przeprowadzanie serii eksperymentów z wykorzystaniem algorytmu genetycznego.

W ramach eksperymentów możliwe jest wykonanie co najmniej 10 niezależnych przebiegów algorytmu dla tej samej konfiguracji problemu.

Każdy przebieg może wykorzystywać inne ziarno generatora losowego.

Pozwala to sprawdzić, jak zmieniają się wyniki algorytmu w zależności od losowości procesu ewolucyjnego.

Moduł eksperymentalny umożliwia:

- wielokrotne uruchamianie algorytmu,
- zapisywanie wyników poszczególnych przebiegów,
- wyznaczanie najlepszego znalezionego rozwiązania,
- agregowanie statystyk kolejnych generacji,
- obliczanie średnich wartości,
- obliczanie odchyleń standardowych,
- przygotowywanie wykresów wyników.

Wyniki mogą być zapisywane w postaci plików CSV, JSON, TXT oraz wykresów PNG.

Dzięki temu możliwe jest późniejsze porównywanie przebiegów i przygotowanie analizy wyników do sprawozdania.

Wyniki zapisane w katalogu `experiment_results` powinny być interpretowane razem z konfiguracją eksperymentu. W szczególności należy zweryfikować, czy zostały wygenerowane na aktualnej wersji sieci drogowej.

## 11. Struktura projektu

Projekt został podzielony na moduły odpowiedzialne za poszczególne elementy aplikacji.

```text
algorytmy-ewolucujme/
│
├── .gitignore
├── LICENSE
├── README.md
│
└── TruckRouteOptimizer/
    │
    ├── main.py
    ├── requirements.txt
    ├── run_experiments.py
    │
    ├── experiment_results/
    │   ├── aggregate_history.csv
    │   ├── best_solution.txt
    │   ├── experiment_config.json
    │   ├── fuel_results.png
    │   ├── run_summary.csv
    │   └── time_results.png
    │
    ├── src/
    │   └── truck_route_optimizer/
    │       ├── __init__.py
    │       ├── experiments.py
    │       ├── experiment_visualization.py
    │       ├── genetic_algorithm.py
    │       ├── gui.py
    │       ├── road_network.py
    │       ├── route_metrics.py
    │       ├── route_operators.py
    │       ├── route_validator.py
    │       ├── vehicle.py
    │       └── visualization.py
    │
    └── tests/
        ├── test_experiments.py
        ├── test_genetic_algorithm.py
        ├── test_route_metrics.py
        ├── test_route_operators.py
        ├── test_route_validator.py
        └── test_vehicle.py
```

### Najważniejsze moduły

| Plik | Odpowiedzialność |
|---|---|
| `main.py` | Punkt wejściowy aplikacji |
| `road_network.py` | Tworzenie symulowanej sieci drogowej |
| `vehicle.py` | Definicja pojazdów i ich ograniczeń |
| `route_validator.py` | Sprawdzanie przejezdności tras |
| `route_metrics.py` | Obliczanie czasu, dystansu i zużycia paliwa |
| `route_operators.py` | Generowanie tras oraz operatory krzyżowania i mutacji |
| `genetic_algorithm.py` | Konfiguracja i uruchamianie algorytmu genetycznego z wykorzystaniem DEAP |
| `visualization.py` | Rysowanie grafu i znalezionej trasy |
| `gui.py` | Interfejs użytkownika |
| `experiments.py` | Przeprowadzanie wielokrotnych eksperymentów i agregowanie wyników |
| `experiment_visualization.py` | Przygotowywanie wizualizacji wyników eksperymentów |
| `run_experiments.py` | Uruchamianie eksperymentów |

## 12. Instalacja i uruchomienie

### 12.1. Wymagania

Do uruchomienia projektu wymagane są:

- Python 3,
- pip,
- biblioteki wymienione w pliku `requirements.txt`.

### 12.2. Pobranie projektu

Po sklonowaniu repozytorium należy przejść do katalogu projektu:

```powershell
cd TruckRouteOptimizer
```

### 12.3. Instalacja zależności

Zalecane jest utworzenie środowiska wirtualnego:

```powershell
python -m venv .venv
```

Aktywacja środowiska w PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalacja wymaganych bibliotek:

```powershell
python -m pip install -r requirements.txt
```

### 12.4. Uruchomienie aplikacji

Z katalogu `TruckRouteOptimizer`:

```powershell
python main.py
```

Uruchomiona zostanie aplikacja z interfejsem graficznym.

## 13. Testowanie

Projekt zawiera testy jednostkowe sprawdzające poprawność najważniejszych elementów aplikacji.

Testy obejmują między innymi:

- poprawność operatorów genetycznych,
- generowanie tras,
- walidację rozwiązań,
- obliczanie parametrów tras,
- działanie algorytmu optymalizacji,
- działanie modułu eksperymentalnego,
- poprawność modelu pojazdu.

Testy można uruchomić z katalogu `TruckRouteOptimizer`:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## 14. Ograniczenia projektu

Projekt jest demonstracyjnym modelem optymalizacji tras, dlatego przyjęto pewne uproszczenia:

- sieć drogowa jest symulowana i nie pobiera aktualnych danych z map;
- rozmieszczenie miast na wizualizacji ma charakter schematyczny;
- model nie uwzględnia rzeczywistych korków ani bieżącej sytuacji drogowej;
- zużycie paliwa jest obliczane na podstawie stałego spalania pojazdu;
- spalanie nie jest dynamicznie uzależniane od masy ładunku;
- czas przejazdu jest szacowany na podstawie parametrów odcinków i współczynników utrudnień;
- algorytm genetyczny jest metodą heurystyczną, dlatego nie gwarantuje znalezienia globalnie optymalnej trasy;
- wygenerowana przez BFS trasa początkowa nie musi być najlepsza pod względem czasu ani dystansu;
- wyniki zależą od konfiguracji algorytmu, danych wejściowych i ziarna generatora losowego.

## 15. Podsumowanie

Projekt przedstawia praktyczne wykorzystanie algorytmu genetycznego do rozwiązywania problemu optymalizacji tras samochodów ciężarowych.

Najważniejszym elementem jest zastosowanie mechanizmów ewolucyjnych do stopniowego ulepszania populacji tras.

Dzięki reprezentacji osobników jako list miast oraz zastosowaniu odpowiednio dostosowanych operatorów możliwe jest poszukiwanie poprawnych rozwiązań w symulowanej sieci drogowej.

Uwzględnienie ograniczeń pojazdu i warunków drogowych pozwala rozszerzyć klasyczne podejście do wyznaczania tras o dodatkowe kryteria związane z transportem ciężarowym.

Biblioteka DEAP odpowiada za mechanizmy algorytmu genetycznego, natomiast logika problemowa, model sieci drogowej, walidacja, obliczenia, operatory dostosowane do problemu oraz integracja z interfejsem zostały opracowane w ramach projektu.
