=========================
Wstęp i odnośniki
=========================

:Autor:
    Paweł Łosowski

Wprowadzenie do projektu
========================

Poniższy dokument stanowi szczegółowe podsumowanie prac zrealizowanych w ramach zajęć laboratoryjnych z przedmiotu Bazy Danych. Głównym założeniem projektu było wykorzystanie w praktyce wiedzy dotyczącej projektowania, wdrażania oraz administracji relacyjnymi systemami bazodanowymi.

Realizacja zadania obejmowała kompletny cykl życia bazy danych: począwszy od analizy zabezpieczeń i teorii, przez budowę modelu konceptualnego i logicznego, kończąc na implementacji fizycznej z wykorzystaniem systemów PostgreSQL oraz SQLite. Całość prac dopełniono stworzeniem skryptów do masowego ładowania danych, a także warstwą dostępu (Data Access Layer) napisaną w Pythonie, za pośrednictwem której realizowano zaawansowane analityczne zapytania SQL.

Podsumowanie i wnioski
======================

Przeprowadzone eksperymenty i realizacja zadań laboratoryjnych pozwoliły na sformułowanie następujących wniosków:

* **Znaczenie normalizacji:** Prawidłowe znormalizowanie struktury (do postaci 3NF) w fazie projektowania logicznego jest niezbędne do wyeliminowania redundancji i zapobiegania anomaliom przy modyfikacji danych.
* **Specyfika silników bazodanowych:** Stworzenie dwóch oddzielnych modeli fizycznych uwydatniło różnice między technologiami. PostgreSQL wykazał się dużą rygorystycznością w typowaniu i obsłudze kluczy obcych, podczas gdy SQLite zaoferował większą elastyczność kosztem uboższego wsparcia dla natywnych typów danych (np. brak wbudowanego typu DATE).
* **Optymalizacja ładowania danych:** Wykorzystanie wstawek wielowartościowych (takich jak metoda ``executemany()`` w języku Python) ma kluczowe znaczenie dla wydajności. Pozwala to na drastyczne skrócenie czasu zasilania bazy poprzez redukcję narzutu komunikacyjnego.
* **Przeniesienie logiki do bazy:** Realizacja złożonych operacji (JOIN, UNION, INTERSECT, podzapytania) bezpośrednio w silniku bazy danych pozwala odciążyć aplikację po stronie klienta, co przekłada się na znacznie mniejsze zużycie zasobów pamięci operacyjnej.

Odnośniki do repozytoriów
=========================

Całość projektu została rozdzielona na dedykowane repozytoria w systemie Git, co ułatwiło zarządzanie wersjami i oddzielenie dokumentacji od plików konfiguracyjnych.

1. Repozytorium dokumentacji (Temat / Sphinx)
---------------------------------------------
W tym miejscu znajduje się struktura dokumentacji projektowej, historia zmian oraz pliki konfiguracyjne niezbędne do wygenerowania sprawozdania.

* **Link:** https://github.com/pawlos1337/Bazy-danych-temat

2. Repozytorium z plikami bazy danych
-------------------------------------
Repozytorium to zawiera kody źródłowe, skrypty DDL dla PostgreSQL i SQLite, wygenerowany plik bazy oraz dane w formacie CSV użyte do inicjalizacji.

* **Link WWW:** https://github.com/pawlos1337/Bazy-danych-pliki
* **Klonowanie SSH:** ``git@github.com:pawlos1337/Bazy-danych-pliki.git``

3. Badania literaturowe (Repozytoria grupy)
-------------------------------------------
Poniższe odnośniki prowadzą do opracowań przygotowanych przez pozostałych członków zespołu (zintegrowanych jako submoduły w odpowiednich rozdziałach):

* **Grupa 1:** https://github.com/karaskamil/Sprzet-dla-bazy-danych.git
* **Grupa 2:** https://github.com/Youarecheck/Bazy_Danych_Tematyczne_Repo_MK.git
* **Grupa 4:** https://github.com/OskarProgrammer/monitorowanie_i_diagnostyka.git
* **Grupa 5:** https://github.com/KMachoK/Tematyczne.git
* **Grupa 6:** https://github.com/domino0472/Partycjonowani-Danych
* **Grupa 7:** https://github.com/oski486/BazyDanych-Subject.git
* **Grupa 8:** https://github.com/Koko9077/Kopie-zapasowe-i-odzyskiwanie-danych.git
