# Break Word Traps
BreakWordTraps.pl jest projektem stworzonym podczas HackYeah 2024. Jest to aplikacja pozwalająca na przeprowadzenie analizy wideo z przemową, która ma na celu sprawdzenie jej poprawności i zasugerowanie możliwych zmian. Do analizowania danych aplikacja używa NLP, LLM-ów, przetwarzania ścieżek audio i wideo.
# Moduły
Aplikacja korzysta z modułów zajmujących się poszczególnymi elementami analizy:
- analiza dźwięku
- analiza wideo
- analiza transkrypcji
  
Upload plików oraz podsumowanie wyników odbywają się poprzez interfejs webowy.
# Instrukcja uruchamiania
Przed uruchomieniem aplikacji upewnij się, że wszystkie biblioteki z pliku **requirements.txt** są zainstalowane.
Żeby obliczanie Współczynnika Mglistości Gunninga (Gunning Fog Index) i Indeksu Czytelności Flescha działało poprawnie dla transkryptów krótszych niż sto wyrazów należy zainstalować bibliotekę py-readability-metrics podanym poniżej poleceniem.

`pip install git+https://github.com/kanapka0/py-readability-metrics.git`
# Strona internetowa
[https://breakwordtraps.pl](https://breakwordtraps.pl/)
