# Break Word Traps
BreakWordTraps.pl jest projektem stworzonym podczas HackYeah 2024. Jest to aplikacja pozwalająca na przeprowadzenie analizy wideo z przemową, która ma na celu sprawdzenie jej poprawności i zasugerowanie możliwych zmian. Do analizowania danych aplikacja używa NLP, LLM-ów, przetwarzania ścieżek audio i wideo.
# Moduły
Aplikacja korzysta z modułów zajmujących się poszczególnymi elementami analizy:
- analiza dźwięku
- analiza wideo
- analiza transkrypcji
  
Upload plików oraz podsumowanie wyników odbywają się poprzez interfejs webowy.

                                                                                                            
 # Konfiguracja i Instrukcje Uruchomienia Projektu         

Żeby obliczanie Współczynnika Mglistości Gunninga (Gunning Fog Index) i Indeksu Czytelności Flescha działało poprawnie dla transkryptów krótszych niż sto wyrazów należy zainstalować bibliotekę py-readability-metrics podanym poniżej poleceniem.

`pip install git+https://github.com/kanapka0/py-readability-metrics.git`
                                                                                                             
## Backend (API)                                                                                            
                                                                                                             
1. Upewnij się, że masz zainstalowany `pyenv`. Jeśli nie, zainstaluj go z [oficjalnego repozytorium pyenv na GitHubie](https://github.com/pyenv/pyenv).                                                                      
                                                                                                             
2. W katalogu głównym projektu utwórz plik `.python-version` z wersją Pythona 3.11:

```bash
echo "3.11.0" > .python-version
```                                                                                             
                                                                                                             
3. Zainstaluj Pythona 3.11 używając pyenv:

```bash
pyenv install 3.11.0
```                                                                                                
                                                                                                             
4. Utwórz wirtualne środowisko za pomocą pyenv:

```bash
pyenv virtualenv 3.11.0 your_project_env
```

Zastąp `your_project_env` nazwą swojego wirtualnego środowiska.                                        
                                                                                                             
5. Aktywuj wirtualne środowisko:

```bash
pyenv activate your_project_env
```                                                                                             
                                                                                                             
6. Zainstaluj wymagane zależności:

```bash
pip install -r requirements.txt
```                                                                                             
                                                                                                             
7. Skonfiguruj zmienne środowiskowe:

```bash
cp .env.template .env
```

Otwórz plik `.env` i uzupełnij potrzebne wartości.                                                      
                                                                                                             
8. Uruchom backend API (upewnij się, że znajdujesz się w katalogu głównym projektu):

```bash
python3 -m api.run
```                                                                                             
                                                                                                             
## Frontend                                                                                                 
                                                                                                             
1. Przejdź do katalogu `front-end`:

```bash
cd front-end
```                                                                                             
                                                                                                             
2. Zainstaluj wymagane pakiety npm:

```bash
npm install
```                                                                                             
                                                                                                             
3. Skonfiguruj zmienne środowiskowe:

```bash
cp .env.template .env
```

Otwórz plik `.env` i uzupełnij potrzebne wartości.                                                      
                                                                                                             
4. Uruchom serwer deweloperski:

```bash
npm run start
```                                                                                             
                                                                                                             
## Uruchamianie Backend i Frontend Jednocześnie                                                                             
                                                                                                             
1. Otwórz dwa okna terminala.                                                                               
                                                                                                             
2. W pierwszym terminalu przejdź do katalogu głównego projektu, aktywuj wirtualne środowisko i uruchom backend:

```bash
pyenv activate your_project_env
python3 -m api.run
```                                                                                             
                                                                                                             
3. W drugim terminalu przejdź do katalogu `front-end` i uruchom frontend:

```bash
npm run start
```                                                                                             
                                                                                                             
Upewnij się, że zarówno backend, jak i frontend działają, aby aplikacja funkcjonowała poprawnie. Sprawdź również, czy wartość `REACT_APP_API_URL` w pliku `.env` frontendu wskazuje na poprawny adres backendu.

Pamiętaj, aby zastąpić wszelkie wartości domyślne w plikach `.env` rzeczywistymi wartościami.
