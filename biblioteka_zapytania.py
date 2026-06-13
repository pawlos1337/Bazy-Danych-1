"""
Moduł biblioteka_zapytania
==========================

Moduł zawiera zestaw zaawansowanych zapytań SQL do obsługi systemu zarządzania biblioteką.
Obsługuje dwa silniki bazodanowe: PostgreSQL oraz SQLite.

Wymagania:
- psycopg2 (lub psycopg) dla PostgreSQL
- sqlite3 (wbudowany) dla SQLite
"""

import sqlite3
# import psycopg2 # Odkomentuj w środowisku docelowym


# =====================================================================
# SEKCJA POSTGRESQL
# =====================================================================

def get_aktywni_czytelnicy_powyzej_limitu(conn, limit_wypozyczen):
    """
    Pobiera listę czytelników, którzy w historii wypożyczyli więcej książek niż wynosi podany limit.
    Wykorzystuje funkcje agregujące, złączenia oraz klauzulę HAVING.

    :param conn: Obiekt aktywnego połączenia z bazą PostgreSQL (psycopg2).
    :type conn: psycopg2.extensions.connection
    :param limit_wypozyczen: Minimalna liczba wypożyczeń uprawniająca do znalezienia się na liście.
    :type limit_wypozyczen: int
    :return: Lista krotek zawierająca imię, nazwisko i sumę wypożyczeń czytelnika.
    :rtype: list[tuple]
    """
    sql = """
        SELECT c.Imie, c.Nazwisko, COUNT(w.ID_Wypozyczenia) as liczba_wypozyczen
        FROM Czytelnicy c
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika
        GROUP BY c.ID_Czytelnika, c.Imie, c.Nazwisko
        HAVING COUNT(w.ID_Wypozyczenia) > %s
        ORDER BY liczba_wypozyczen DESC;
    """
    with conn.cursor() as cursor:
        cursor.execute(sql, (limit_wypozyczen,))
        return cursor.fetchall()


def get_ksiazki_z_iloscia_wypozyczen(conn, rok_od):
    """
    Zwraca szczegółowe dane o książkach wydanych po zadanym roku wraz z ilością ich historycznych 
    wypożyczeń. Wykorzystuje funkcje wierszowe (UPPER) oraz podzapytanie w klauzuli SELECT.

    :param conn: Obiekt aktywnego połączenia z bazą PostgreSQL.
    :type conn: psycopg2.extensions.connection
    :param rok_od: Dolna granica roku wydania książki (wyłącznie).
    :type rok_od: int
    :return: Lista krotek (Tytuł, ZWielkiejLitery_NazwiskoAutora, Total_Wypozyczen).
    :rtype: list[tuple]
    """
    sql = """
        SELECT 
            k.Tytul, 
            UPPER(a.Nazwisko) AS Nazwisko_Autora_Caps,
            (SELECT COUNT(*) FROM Wypozyczenia w WHERE w.ID_Ksiazki = k.ID_Ksiazki) AS suma_wypozyczen
        FROM Ksiazki k
        JOIN Autorzy a ON k.ID_Autora = a.ID_Autora
        WHERE k.Rok_Wydania > %s;
    """
    with conn.cursor() as cursor:
        cursor.execute(sql, (rok_od,))
        return cursor.fetchall()


def get_czytelnicy_bez_wypozyczen(conn):
    """
    Pobiera dane czytelników, którzy zapisali się do biblioteki, ale nigdy nie wypożyczyli żadnej książki.
    Zastosowano tu operator zbiorowy EXCEPT w celu odjęcia zbioru aktywnych od wszystkich.

    :param conn: Obiekt aktywnego połączenia z bazą PostgreSQL.
    :type conn: psycopg2.extensions.connection
    :return: Lista krotek z danymi czytelników (ID, Imię, Nazwisko).
    :rtype: list[tuple]
    """
    sql = """
        SELECT ID_Czytelnika, Imie, Nazwisko FROM Czytelnicy
        EXCEPT
        SELECT c.ID_Czytelnika, c.Imie, c.Nazwisko 
        FROM Czytelnicy c
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika;
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def get_ksiazki_wypozyczone_w_miescie(conn, nazwa_miasta):
    """
    Wyszukuje tytuły książek, które kiedykolwiek zostały wypożyczone przez mieszkańców określonego miasta.
    Rozwiązanie bazuje na podzapytaniu skorelowanym w klauzuli WHERE.

    :param conn: Obiekt aktywnego połączenia z bazą PostgreSQL.
    :type conn: psycopg2.extensions.connection
    :param nazwa_miasta: Nazwa miasta do przefiltrowania czytelników.
    :type nazwa_miasta: str
    :return: Lista krotek zawierająca wyłącznie tytuły książek.
    :rtype: list[tuple]
    """
    sql = """
        SELECT Tytul 
        FROM Ksiazki 
        WHERE ID_Ksiazki IN (
            SELECT w.ID_Ksiazki 
            FROM Wypozyczenia w
            JOIN Czytelnicy c ON w.ID_Czytelnika = c.ID_Czytelnika
            WHERE c.Miasto = %s
        );
    """
    with conn.cursor() as cursor:
        cursor.execute(sql, (nazwa_miasta,))
        return cursor.fetchall()


def get_wszechstronni_czytelnicy(conn):
    """
    Zwraca czytelników (Imię i Nazwisko), którzy wypożyczali książki z kategorii 'Fantastyka'
    oraz jednocześnie z kategorii 'Kryminał'. Używa operatora zbiorowego INTERSECT.

    :param conn: Obiekt aktywnego połączenia z bazą PostgreSQL.
    :type conn: psycopg2.extensions.connection
    :return: Lista krotek z imionami i nazwiskami wszechstronnych czytelników.
    :rtype: list[tuple]
    """
    sql = """
        SELECT c.Imie, c.Nazwisko 
        FROM Czytelnicy c
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika
        JOIN Ksiazki k ON w.ID_Ksiazki = k.ID_Ksiazki
        JOIN Kategorie kat ON k.ID_Kategorii = kat.ID_Kategorii
        WHERE kat.Nazwa_Kategorii = 'Fantastyka'
        INTERSECT
        SELECT c.Imie, c.Nazwisko 
        FROM Czytelnicy c
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika
        JOIN Ksiazki k ON w.ID_Ksiazki = k.ID_Ksiazki
        JOIN Kategorie kat ON k.ID_Kategorii = kat.ID_Kategorii
        WHERE kat.Nazwa_Kategorii = 'Kryminał';
    """
    with conn.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


# =====================================================================
# SEKCJA SQLITE
# =====================================================================

def get_srednia_wypozyczen_na_czytelnika(conn):
    """
    Oblicza średnią liczbę wypożyczonych książek przypadającą na jednego aktywnego czytelnika.
    Wykorzystuje podzapytanie w klauzuli FROM do wcześniejszej agregacji danych.

    :param conn: Obiekt połączenia z bazą SQLite.
    :type conn: sqlite3.Connection
    :return: Zwraca jedną krotkę z pojedynczą wartością zmiennoprzecinkową (średnia).
    :rtype: list[tuple]
    """
    sql = """
        SELECT AVG(liczba_wypozyczen) 
        FROM (
            SELECT COUNT(ID_Wypozyczenia) as liczba_wypozyczen 
            FROM Wypozyczenia 
            GROUP BY ID_Czytelnika
        );
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def get_katalog_osob(conn):
    """
    Zwraca ujednoliconą listę wszystkich osób figurujących w systemie, przypisując im odpowiednią
    rolę. Używa operatora zbiorowego UNION w celu złączenia tabel Czytelnicy i Autorzy.

    :param conn: Obiekt połączenia z bazą SQLite.
    :type conn: sqlite3.Connection
    :return: Lista krotek postaci (Imię, Nazwisko, Rola).
    :rtype: list[tuple]
    """
    sql = """
        SELECT Imie, Nazwisko, 'Czytelnik' AS Rola FROM Czytelnicy
        UNION
        SELECT Imie, Nazwisko, 'Autor' AS Rola FROM Autorzy
        ORDER BY Nazwisko ASC;
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def get_puste_kategorie(conn):
    """
    Pobiera nazwy kategorii, do których aktualnie nie przypisano żadnych książek w inwentarzu.
    Demonstruje wykorzystanie LEFT JOIN w celu znalezienia brakujących relacji (NULL).

    :param conn: Obiekt połączenia z bazą SQLite.
    :type conn: sqlite3.Connection
    :return: Lista krotek z nazwami "pustych" kategorii.
    :rtype: list[tuple]
    """
    sql = """
        SELECT kat.Nazwa_Kategorii 
        FROM Kategorie kat 
        LEFT JOIN Ksiazki k ON kat.ID_Kategorii = k.ID_Kategorii 
        WHERE k.ID_Ksiazki IS NULL;
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def get_najdluzej_przetrzymywane(conn, limit_rekordow):
    """
    Wyszukuje wypożyczenia, które aktualnie trwają (brak daty zwrotu) i sortuje je rosnąco od 
    najstarszych. Wykorzystuje funkcję wierszową DATE() silnika SQLite działającą na ciągach TEXT.

    :param conn: Obiekt połączenia z bazą SQLite.
    :type conn: sqlite3.Connection
    :param limit_rekordow: Liczba rekordów do zwrócenia (LIMIT).
    :type limit_rekordow: int
    :return: Lista krotek (Tytuł, Imię, Nazwisko, Data wypożyczenia).
    :rtype: list[tuple]
    """
    sql = """
        SELECT k.Tytul, c.Imie, c.Nazwisko, w.Data_Wypozyczenia 
        FROM Wypozyczenia w 
        JOIN Ksiazki k ON w.ID_Ksiazki = k.ID_Ksiazki 
        JOIN Czytelnicy c ON w.ID_Czytelnika = c.ID_Czytelnika 
        WHERE w.Data_Zwrotu IS NULL OR w.Data_Zwrotu = '' 
        ORDER BY DATE(w.Data_Wypozyczenia) ASC 
        LIMIT ?;
    """
    cursor = conn.cursor()
    cursor.execute(sql, (limit_rekordow,))
    return cursor.fetchall()


def get_raport_autorow(conn):
    """
    Tworzy zaawansowany raport o autorach, zliczając ich wszystkie książki oraz wskazując 
    tytuł chronologicznie najnowszego dzieła za pomocą podzapytania w SELECT.

    :param conn: Obiekt połączenia z bazą SQLite.
    :type conn: sqlite3.Connection
    :return: Lista krotek (Imię autora, Nazwisko, Suma dzieł, Tytuł najnowszej książki).
    :rtype: list[tuple]
    """
    sql = """
        SELECT 
            a.Imie, 
            a.Nazwisko, 
            COUNT(k.ID_Ksiazki) as ilosc_ksiazek,
            (
                SELECT Tytul 
                FROM Ksiazki k2 
                WHERE k2.ID_Autora = a.ID_Autora 
                ORDER BY Rok_Wydania DESC 
                LIMIT 1
            ) as najnowsza_ksiazka
        FROM Autorzy a 
        LEFT JOIN Ksiazki k ON a.ID_Autora = k.ID_Autora 
        GROUP BY a.ID_Autora;
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()
