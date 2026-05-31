#!/bin/bash

# Ustawienie ścieżki do Twojego projektu
PROJEKT_DIR="/home/student15/gitstuiff/Bazy-Danych-1"
cd "$PROJEKT_DIR" || exit

# 0. ZABEZPIECZENIE: Pobranie najnowszych zmian z GitHuba przed pracą
echo ">>> Synchronizacja lokalnego repozytorium z GitHubem..."
git pull --rebase --no-recurse-submodules origin main

# Twój sprawdzony link do surowych danych CSV z Arkusza
LINK_CSV="https://docs.google.com/spreadsheets/d/e/2PACX-1vTq8qlrUea8l8lVkCEzqDy45oepDUm8kmL7hrploPt_suOFkJAK8uwGfodrXKy1XLm1kRHD9UflCw1Z/pub?gid=0&single=true&output=csv"

# 1. Pobieramy aktualną listę od chłopaków
curl -s -L "$LINK_CSV" | sed 's/\r$//' > linki.csv

# 2. Szukamy nowych ziomków w Arkuszu
tail -n +2 linki.csv | while IFS=, read -r NUMER LINK; do
    NUMER_CZYSTY=$(echo "$NUMER" | tr -d ' ' | sed 's/^2\.//')
    LINK_CZYSTY=$(echo "$LINK" | tr -d ' ' | sed 's/\/$//')

    if [ -n "$NUMER_CZYSTY" ] && [ -n "$LINK_CZYSTY" ]; then
        FOLDER="rozdzial_2${NUMER_CZYSTY}"
        SCIEZKA_SUBMODULU="source/rozdzial_2/${FOLDER}"

        if [ ! -d "$SCIEZKA_SUBMODULU" ]; then
            echo ">>> Wykryto nową osobę! Temat 2.$NUMER_CZYSTY: $LINK_CZYSTY"
            git submodule add "$LINK_CZYSTY" "$SCIEZKA_SUBMODULU"
        fi
    fi
done

# 3. AKTUALIZACJA WSZYSTKICH ISTNIEJĄCYCH (Dociąganie poprawek od kumpli)
echo ">>> Sprawdzam aktualizacje u wszystkich ziomków..."
# Usunięto flagę --recursive, aby ignorować zepsute, zagnieżdżone submoduły u innych
git submodule update --remote

# 4. DECYZJA O WYSYŁCE: Jeśli są nowe osoby LUB ktoś coś zmienił w tekście
if [ -n "$(git status --porcelain)" ]; then
    echo ">>> Wykryto nowości. Aktualizuję spis treści i wysyłam na GitHuba..."
    
    # Budowanie spisu treści index.rst
    cat << 'EOF' > source/rozdzial_2/index.rst
Badania literaturowe
====================

.. toctree::
   :maxdepth: 1

EOF
    
    for dir in $(ls -d source/rozdzial_2/rozdzial_2*/ | sort -V); do
        nazwa_folderu=$(basename "$dir")
        if [ -f "$dir/source/index.rst" ]; then
            echo "   $nazwa_folderu/source/index" >> source/rozdzial_2/index.rst
        else
            echo "   $nazwa_folderu/index" >> source/rozdzial_2/index.rst
        fi
    done
    
    # Wysyłka na GitHuba
    git add .
    git commit -m "Terminator: Globalna aktualizacja treści i submodułów"
    # Ostatnia deska ratunku przed pushem, gdyby ktoś wypchnął coś dosłownie w tej samej sekundzie
    git pull --rebase --no-recurse-submodules origin main
    git push
    echo ">>> Wszystko zsynchronizowane!"
else
    echo ">>> Brak zmian. Wszyscy są aktualni."
fi
