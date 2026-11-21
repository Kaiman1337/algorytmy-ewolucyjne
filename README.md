# algorytmy-ewolucujme
Temat: Wyznaczanie optymalnej trasy w problemie komiwojażera za pomocą algorytmów ewolucyjnych. 

# Truck Route Optimizer

Aplikacja służąca do optymalizacji tras przejazdu samochodu ciężarowego z wykorzystaniem **algorytmu genetycznego**. Projekt został przygotowany w ramach przedmiotu *Algorytmy ewolucyjne*.

Program pozwala wybrać miasto początkowe, miasto docelowe oraz profil pojazdu, a następnie wykorzystuje algorytm genetyczny do poszukiwania korzystnej trasy w symulowanej sieci drogowej.

W procesie optymalizacji uwzględniane są między innymi czas przejazdu, zużycie paliwa, ograniczenia pojazdu oraz warunki panujące na poszczególnych odcinkach dróg.

## 1. Cel projektu

Głównym celem projektu jest praktyczne przedstawienie zastosowania algorytmów ewolucyjnych do rozwiązywania problemu optymalizacji tras transportowych.

Zamiast sprawdzać wszystkie możliwe trasy, program wykorzystuje populację potencjalnych rozwiązań, które są stopniowo ulepszane za pomocą mechanizmów charakterystycznych dla algorytmów genetycznych:

- tworzenia populacji początkowej,
- oceny jakości osobników,
- selekcji,
- krzyżowania,
- mutacji,
- zachowania najlepszych rozwiązań.

Każdy osobnik reprezentuje możliwą trasę przejazdu ciężarówki pomiędzy wybranymi miastami.

## 2. Wykorzystane technologie

| Technologia | Zastosowanie |
|---|---|
| Python | Główny język programowania |
| DEAP | Framework do tworzenia algorytmów ewolucyjnych |
| NetworkX | Reprezentacja i obsługa grafu drogowego |
| Matplotlib | Wizualizacja sieci drogowej i wyznaczonej trasy |
| Tkinter | Graficzny interfejs użytkownika |

**Ważne rozróżnienie:** biblioteka DEAP dostarcza mechanizmy i infrastrukturę algorytmu genetycznego. Logika związana z konkretnym problemem transportowym, w tym reprezentacja tras, ich walidacja, obliczanie parametrów przejazdu oraz dostosowane operatory, została przygotowana w ramach projektu.

## 3. Model sieci drogowej

Sieć drogowa została przedstawiona w postaci skierowanego grafu ważonego.

- Wierzchołki reprezentują miasta.
- Krawędzie reprezentują bezpośrednie połączenia drogowe.
- Atrybuty krawędzi opisują parametry poszczególnych odcinków.

W symulowanej sieci uwzględniono osiem miast:

- Warszawa,
- Gdańsk,
- Szczecin,
- Poznań,
- Łódź,
- Wrocław,
- Katowice,
- Kraków.

Sieć zawiera 13 połączeń drogowych, reprezentowanych jako 26 skierowanych krawędzi, po jednej dla każdego kierunku przejazdu.

Każdy odcinek może posiadać następujące parametry:

- długość w kilometrach,
- dopuszczalną prędkość,
- maksymalną masę pojazdu,
- maksymalną wysokość,
- maksymalną szerokość,
- maksymalną długość,
- współczynnik natężenia ruchu,
- poziom robót drogowych,
- informację o zamknięciu drogi.

Sieć jest modelem symulacyjnym, a nie bezpośrednim odwzorowaniem aktualnych danych z OpenStreetMap.

## 4. Model pojazdu

Program umożliwia wybór profilu pojazdu ciężarowego.

Każdy profil posiada parametry wykorzystywane podczas sprawdzania możliwości przejazdu przez dany odcinek.

Uwzględniane są między innymi:

- masa pojazdu,
- wysokość,
- szerokość,
- długość,
- średnie zużycie paliwa.

Przed wykorzystaniem odcinka w trasie sprawdzane jest, czy pojazd spełnia jego ograniczenia.

Odcinek może zostać odrzucony, jeżeli przykładowo:

- droga jest zamknięta,
- dopuszczalna masa jest mniejsza od masy pojazdu,
- wysokość pojazdu przekracza ograniczenie,
- szerokość lub długość pojazdu przekracza dopuszczalne wartości.

Dzięki temu algorytm nie ogranicza się wyłącznie do poszukiwania najkrótszej drogi. Musi również uwzględniać możliwość rzeczywistego przejazdu wybranym pojazdem w ramach przyjętego modelu.

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
- spełniać ograniczenia wybranego pojazdu.

Zastosowanie takiej reprezentacji pozwala bezpośrednio interpretować osobnika jako trasę przejazdu.

## 6. Działanie algorytmu genetycznego

Algorytm rozpoczyna działanie od wygenerowania populacji początkowej, czyli zestawu potencjalnych tras.

Następnie wykonywane są kolejne generacje, w których osobniki podlegają ocenie i operacjom ewolucyjnym.

### 6.1. Generowanie populacji początkowej

Na początku tworzona jest populacja poprawnych tras pomiędzy wskazanymi miastami.

Do generowania tras wykorzystywana jest logika uwzględniająca strukturę grafu oraz ograniczenia pojazdu.

Dzięki temu algorytm rozpoczyna poszukiwanie od rozwiązań, które mają możliwość realizacji przejazdu.

### 6.2. Funkcja oceny

Każdy osobnik jest oceniany na podstawie parametrów reprezentowanej trasy.

W projekcie uwzględniane są dwa kryteria:

1. Czas przejazdu – wyznaczany na podstawie długości odcinków, dopuszczalnych prędkości oraz współczynników utrudnień.
2. Zużycie paliwa – obliczane na podstawie długości trasy i średniego spalania wybranego pojazdu.

Celem jest minimalizacja obu wartości.

DEAP wykorzystuje dwuelementową funkcję przystosowania z wagami `(-1.0, -1.0)`, co oznacza, że oba kryteria są traktowane jako minimalizowane.

### 6.3. Selekcja

Selekcja odpowiada za wybór osobników, które będą uczestniczyły w tworzeniu kolejnego pokolenia.

W projekcie zastosowano selekcję turniejową.

Polega ona na wylosowaniu grupy osobników i wybraniu spośród nich najlepszego według przyjętej funkcji przystosowania.

Lepsze rozwiązania mają dzięki temu większą szansę na przekazanie swoich cech kolejnemu pokoleniu.

### 6.4. Krzyżowanie

Krzyżowanie polega na łączeniu informacji pochodzących od dwóch osobników rodzicielskich.

W przypadku projektu rodzicami są dwie możliwe trasy przejazdu.

Operator krzyżowania wykorzystuje wspólne miasta występujące na trasach, aby utworzyć nowe rozwiązanie z fragmentów tras rodziców.

Ważne jest zachowanie poprawności rozwiązania, czyli między innymi ciągłości połączeń drogowych oraz braku powtarzających się miast.

### 6.5. Mutacja

Mutacja wprowadza niewielkie zmiany w strukturze trasy.

Jej zadaniem jest zwiększanie różnorodności populacji i umożliwienie algorytmowi sprawdzania nowych możliwości.

W projekcie mutacja wykorzystuje dostępne połączenia drogowe do modyfikowania fragmentów trasy.

Zmodyfikowana trasa musi nadal spełniać warunki poprawności oraz ograniczenia pojazdu.

### 6.6. Elitaryzm

W algorytmie zastosowano również elitaryzm.

Polega on na zachowaniu określonej liczby najlepszych osobników i przeniesieniu ich do kolejnej generacji bez konieczności ponownego tworzenia ich przez krzyżowanie lub mutację.

Dzięki temu najlepsze znalezione rozwiązania nie zostają przypadkowo utracone.

### 6.7. Zakończenie działania

Algorytm wykonuje określoną liczbę generacji.

Najlepsze znalezione rozwiązanie jest przechowywane w strukturze Hall of Fame udostępnianej przez DEAP.

Po zakończeniu działania zwracana jest najlepsza znaleziona trasa wraz z obliczonymi parametrami przejazdu.

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

Ziarno generatora losowego pozwala uzyskać powtarzalne wyniki eksperymentów przy identycznych danych wejściowych i konfiguracji.

## 8. Obliczanie parametrów przejazdu

Dla każdego odcinka trasy obliczane są parametry przejazdu.

### Czas przejazdu

Podstawą obliczeń jest długość odcinka oraz efektywna prędkość przejazdu.

Uwzględniane są współczynniki natężenia ruchu i robót drogowych.

Poziom robót drogowych przyjmuje wartości od 0 do 5:

| Poziom | Współczynnik |
|---|---:|
| 0 – brak robót | 1,0 |
| 1 – bardzo małe utrudnienia | 1,1 |
| 2 – małe utrudnienia | 1,2 |
| 3 – umiarkowane utrudnienia | 1,4 |
| 4 – duże utrudnienia | 1,7 |
| 5 – bardzo duże utrudnienia | 2,0 |

Efektywna prędkość obliczana jest według zależności:

`prędkość efektywna = prędkość dopuszczalna / (współczynnik ruchu × współczynnik robót drogowych)`

Czas przejazdu odcinka jest następnie obliczany na podstawie jego długości i efektywnej prędkości.

### Zużycie paliwa

Zużycie paliwa obliczane jest na podstawie długości trasy oraz średniego spalania wybranego pojazdu:

`zużycie paliwa = długość trasy × spalanie / 100`

W obecnym modelu spalanie jest stałe dla danego profilu pojazdu. Nie jest dynamicznie uzależniane od masy ładunku, nachylenia drogi ani stylu jazdy.

## 9. Interfejs graficzny

Program posiada interfejs graficzny przygotowany z wykorzystaniem biblioteki Tkinter.

Użytkownik może:

1. Wybrać miasto początkowe.
2. Wybrać miasto docelowe.
3. Wybrać profil pojazdu.
4. Uruchomić optymalizację.
5. Wyświetlić znalezioną trasę na grafie.
6. Odczytać czas przejazdu, dystans i zużycie paliwa.
7. Zobaczyć listę kolejnych przejechanych odcinków.

Dostępny jest również edytor warunków drogowych.

Pozwala on zmieniać parametry odcinków, w tym:

- natężenie ruchu,
- poziom robót drogowych,
- dopuszczalną masę,
- ograniczenia wymiarowe,
- stan zamknięcia drogi.

Zmiany są stosowane w obu kierunkach danego połączenia i uwzględniane podczas kolejnej optymalizacji.

## 10. Struktura projektu

Najważniejsze moduły aplikacji:

| Plik | Odpowiedzialność |
|---|---|
| `road_network.py` | Tworzenie symulowanej sieci drogowej |
| `vehicle.py` | Definicja pojazdów i ich ograniczeń |
| `route_validator.py` | Sprawdzanie poprawności tras |
| `route_metrics.py` | Obliczanie czasu, dystansu i zużycia paliwa |
| `route_operators.py` | Generowanie tras oraz operatory krzyżowania i mutacji |
| `genetic_algorithm.py` | Konfiguracja i uruchamianie algorytmu genetycznego z wykorzystaniem DEAP |
| `visualization.py` | Rysowanie grafu i znalezionej trasy |
| `gui.py` | Interfejs użytkownika |

## 11. Instalacja i uruchomienie

Projekt wymaga zainstalowanego Pythona.

Z poziomu katalogu głównego repozytorium można zainstalować wymagane biblioteki:

```powershell
python -m pip install deap networkx matplotlib
```

Przy układzie projektu wykorzystującym katalog `src` aplikację można uruchomić z katalogu głównego repozytorium poleceniami:

```powershell
$env:PYTHONPATH = "src"
python -c "from truck_route_optimizer.gui import run_gui; run_gui()"
```

## 12. Testowanie

Projekt zawiera testy sprawdzające między innymi:

- poprawność operatorów genetycznych,
- generowanie tras,
- walidację rozwiązań,
- obliczanie parametrów tras,
- działanie algorytmu optymalizacji.

Testy można uruchomić z katalogu głównego projektu:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## 13. Ograniczenia projektu

Projekt jest demonstracyjnym modelem optymalizacji tras, dlatego przyjęto pewne uproszczenia:

- sieć drogowa jest symulowana i nie pobiera aktualnych danych z map;
- model nie uwzględnia rzeczywistych korków ani bieżącej sytuacji drogowej;
- zużycie paliwa jest obliczane na podstawie stałego spalania pojazdu;
- nie jest modelowany ładunek ani jego wpływ na spalanie;
- czas przejazdu jest szacowany na podstawie parametrów odcinków i współczynników utrudnień;
- algorytm genetyczny jest metodą heurystyczną, dlatego nie gwarantuje znalezienia globalnie optymalnej trasy.

## 14. Podsumowanie

Projekt przedstawia praktyczne wykorzystanie algorytmu genetycznego do rozwiązywania problemu optymalizacji tras samochodów ciężarowych.

Najważniejszym elementem jest zastosowanie mechanizmów ewolucyjnych do stopniowego ulepszania populacji tras. Dzięki reprezentacji osobników jako list miast oraz zastosowaniu odpowiednio dostosowanych operatorów możliwe jest poszukiwanie poprawnych rozwiązań w grafie drogowym.

Biblioteka DEAP odpowiada za mechanizmy algorytmu genetycznego, natomiast logika problemowa, model sieci drogowej, walidacja, obliczenia oraz integracja z interfejsem zostały opracowane w ramach projektu.
