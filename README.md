#### Marek Świergoń 261750 Języki Formalne i Techniki Translacji

## Kompilator prostego języka imperatywnego do kodu maszyny wirtualnej.

W celu uruchomienia kompilatora należy mieć zainstalowany język Python w wersji 3.8 oraz bibliotekę sly w wersji co najmniej 0.5:

#### Instalacja języka Python:

`sudo apt install python3.8`

#### Instalacja biblioteki sly:

`pip3 install sly`

#### Uruchomienie kompilatora jest w postaci polecenia:

`python3 kompilator.py [in] [out]`

gdzie:

* `[in]` - ścieżka do pliku wejściowego z programem w prostym języku imperatywnym
* `[out]` - ścieżka, na której ma być zapisany plik z wyjściowym kodem maszyny wirtualnej
