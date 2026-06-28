=======================================
Wprowadzenie oraz linki do repozytoriów
=======================================

:Autor:
    Paweł Łosowski

Cel i zakres projektu
=====================

Niniejszy dokument stanowi oficjalne sprawozdanie z prac zrealizowanych podczas zajęć laboratoryjnych z przedmiotu Bazy Danych. Projekt ten miał na celu praktyczne sprawdzenie wiedzy związanej z projektowaniem, wdrażaniem oraz zarządzaniem systemami relacyjnymi.

W ramach prac przeprowadzono pełny cykl deweloperski bazy danych: począwszy od teoretycznej analizy i kwestii bezpieczeństwa, poprzez stworzenie modelu konceptualnego i logicznego, aż po ostateczną implementację fizyczną przy użyciu silników PostgreSQL oraz SQLite. Dodatkowo przygotowano skrypty odpowiedzialne za wsadowe ładowanie danych oraz dedykowany interfejs w języku Python (Data Access Layer), pozwalający na wykonywanie zaawansowanych, analitycznych zapytań SQL.

Kluczowe wnioski z przeprowadzonych prac
========================================

Poniżej zestawiono najważniejsze spostrzeżenia wynikające z przeprowadzonych ćwiczeń i implementacji systemu:

* **Istota normalizacji:** Doprowadzenie schematu bazy do trzeciej postaci normalnej (3NF) na etapie projektowania logicznego jest krytyczne dla uniknięcia redundancji i zabezpiecza przed anomaliami podczas modyfikacji rekordów.
* **Porównanie środowisk bazodanowych:** Równoległa implementacja w dwóch systemach uwypukliła rygorystyczne podejście PostgreSQL do typowania danych i obsługi więzów integralności. Z kolei SQLite okazał się bardziej elastyczny w użyciu, jednak jego ograniczeniem jest brak niektórych natywnych typów (jak np. dedykowany typ DATE).
* **Optymalizacja zapytań wsadowych:** Użycie mechanizmów wsadowych (takich jak funkcja ``executemany()`` w Pythonie) drastycznie poprawia wydajność ładowania dużych zbiorów danych, minimalizując opóźnienia komunikacyjne na linii aplikacja-baza.
* **Przetwarzanie po stronie serwera bazy:** Delegowanie skomplikowanych operacji (takich jak złączenia JOIN, czy operatory zbiorowe UNION i INTERSECT) bezpośrednio do silnika bazy danych znacząco odciąża aplikację kliencką i pozwala na sporą oszczędność pamięci operacyjnej RAM.

Wykaz repozytoriów projektu
===========================

Kod źródłowy oraz dokumentacja zostały zorganizowane w systemie kontroli wersji Git z podziałem na osobne repozytoria, co pozwoliło na zachowanie porządku i przejrzystości struktury.

1. Repozytorium ze sprawozdaniem (Sphinx)
-----------------------------------------
W tym miejscu przechowujemy pełną strukturę dokumentacji tekstowej, historię zmian (commitów) oraz niezbędne pliki konfiguracyjne do kompilacji projektu.

* **Adres URL:** https://github.com/pawlos1337/Bazy-danych-temat

2. Repozytorium z zasobami technicznymi bazy
--------------------------------------------
Znajdują się tu kody źródłowe, definicje struktur dla obu wykorzystanych silników, fizyczny plik bazy oraz zbiory danych w formacie CSV użyte do zasilenia tabel.

* **Adres WWW:** https://github.com/pawlos1337/Bazy-danych-pliki

3. Repozytoria pozostałych podgrup
---------------------------------------------
Poniżej zamieszczono linki do prac badawczych innych zespołów, które zostały włączone do niniejszego sprawozdania (w Rozdziale 2) jako submoduły:

* **Grupa 1:** https://github.com/karaskamil/Sprzet-dla-bazy-danych.git
* **Grupa 2:** https://github.com/Youarecheck/Bazy_Danych_Tematyczne_Repo_MK.git
* **Grupa 4:** https://github.com/OskarProgrammer/monitorowanie_i_diagnostyka.git
* **Grupa 5:** https://github.com/KMachoK/Tematyczne.git
* **Grupa 6:** https://github.com/domino0472/Partycjonowani-Danych
* **Grupa 7:** https://github.com/oski486/BazyDanych-Subject.git
* **Grupa 8:** https://github.com/Koko9077/Kopie-zapasowe-i-odzyskiwanie-danych.git
