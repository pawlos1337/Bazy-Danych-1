"""
Moduł realizujący warstwę dostępu do danych (Data Access Layer) dla systemu bibliotecznego.
Zawiera zaawansowane zapytania SQL obsługujące bazy PostgreSQL oraz SQLite.
"""

# ==============================================================================
# SEKCJA 1: ZAPYTANIA DLA POSTGRESQL (Wymaga psycopg)
# ==============================================================================

def get_aktywni_czytelnicy_powyzej_limitu(conn, limit_wypozyczen):
    """
    Pobiera listę czytelników, którzy w historii wypożyczyli więcej książek niż wynosi podany limit.
    Wykorzystuje funkcje agregujące, złączenia (JOIN) oraz klauzulę HAVING.

    **Zapytanie SQL:**::

        SELECT c.Imie, c.Nazwisko, COUNT(w.ID_Wypozyczenia) as suma 
        FROM Czytelnicy c 
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika 
        GROUP BY c.ID_Czytelnika 
        HAVING COUNT(w.ID_Wypozyczenia) > %s;

    :param conn: Obiekt aktywnego połączenia z bazą PostgreSQL.
    :param limit_wypozyczen: Minimalna liczba wypożyczeń.
    :return: Lista krotek (Imie, Nazwisko, Suma wypozyczen).
    """
    sql = """
        SELECT c.Imie, c.Nazwisko, COUNT(w.ID_Wypozyczenia) as suma 
        FROM Czytelnicy c 
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika 
        GROUP BY c.ID_Czytelnika 
        HAVING COUNT(w.ID_Wypozyczenia) > %s;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (limit_wypozyczen,))
        return cur.fetchall()

def get_czytelnicy_bez_wypozyczen(conn):
    """
    Pobiera dane czytelników, którzy zapisali się do biblioteki, ale nigdy nie wypożyczyli książki.
    Zastosowano operator zbiorowy EXCEPT (odjęcie zbioru aktywnych od wszystkich).

    **Zapytanie SQL:**::

        SELECT ID_Czytelnika, Imie, Nazwisko FROM Czytelnicy
        EXCEPT
        SELECT c.ID_Czytelnika, c.Imie, c.Nazwisko 
        FROM Czytelnicy c 
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika;

    :param conn: Obiekt aktywnego połączenia z bazą PostgreSQL.
    :return: Lista krotek z danymi biernych czytelników.
    """
    sql = """
        SELECT ID_Czytelnika, Imie, Nazwisko FROM Czytelnicy
        EXCEPT
        SELECT c.ID_Czytelnika, c.Imie, c.Nazwisko 
        FROM Czytelnicy c 
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()

def get_ksiazki_wypozyczone_w_miescie(conn, nazwa_miasta):
    """
    Wyszukuje tytuły książek, które kiedykolwiek zostały wypożyczone przez mieszkańców określonego miasta.
    Wykorzystuje podzapytanie skorelowane z operatorem EXISTS w klauzuli WHERE.

    **Zapytanie SQL:**::

        SELECT Tytul FROM Ksiazki k 
        WHERE EXISTS (
            SELECT 1 FROM Wypozyczenia w 
            JOIN Czytelnicy c ON w.ID_Czytelnika = c.ID_Czytelnika 
            WHERE w.ID_Ksiazki = k.ID_Ksiazki AND c.Miasto = %s
        );

    :param conn: Obiekt aktywnego połączenia z bazą PostgreSQL.
    :param nazwa_miasta: Ciąg znaków oznaczający miasto.
    :return: Lista krotek z tytułami książek.
    """
    sql = """
        SELECT Tytul FROM Ksiazki k 
        WHERE EXISTS (
            SELECT 1 FROM Wypozyczenia w 
            JOIN Czytelnicy c ON w.ID_Czytelnika = c.ID_Czytelnika 
            WHERE w.ID_Ksiazki = k.ID_Ksiazki AND c.Miasto = %s
        );
    """
    with conn.cursor() as cur:
        cur.execute(sql, (nazwa_miasta,))
        return cur.fetchall()

def get_ksiazki_z_iloscia_wypozyczen(conn, rok_od):
    """
    Zwraca szczegółowe dane o książkach wydanych po zadanym roku wraz z ilością ich historycznych wypożyczeń.
    Używa podzapytania w klauzuli SELECT oraz funkcji wierszowej UPPER().

    **Zapytanie SQL:**::

        SELECT k.Tytul, UPPER(a.Nazwisko) AS Autor, 
            (SELECT COUNT(*) FROM Wypozyczenia w WHERE w.ID_Ksiazki = k.ID_Ksiazki) AS Total 
        FROM Ksiazki k 
        JOIN Autorzy a ON k.ID_Autora = a.ID_Autora 
        WHERE k.Rok_Wydania > %s;

    :param conn: Obiekt aktywnego połączenia z bazą PostgreSQL.
    :param rok_od: Dolna granica roku wydania.
    :return: Lista krotek z tytułem, nazwiskiem autora i liczbą wypożyczeń.
    """
    sql = """
        SELECT k.Tytul, UPPER(a.Nazwisko) AS Autor, 
            (SELECT COUNT(*) FROM Wypozyczenia w WHERE w.ID_Ksiazki = k.ID_Ksiazki) AS Total 
        FROM Ksiazki k 
        JOIN Autorzy a ON k.ID_Autora = a.ID_Autora 
        WHERE k.Rok_Wydania > %s;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (rok_od,))
        return cur.fetchall()

def get_wszechstronni_czytelnicy(conn):
    """
    Zwraca czytelników, którzy wypożyczali książki z kategorii 'Fantastyka' oraz z 'Kryminał'.
    Używa operatora zbiorowego INTERSECT (część wspólna zbiorów).

    **Zapytanie SQL:**::

        SELECT c.Imie, c.Nazwisko FROM Czytelnicy c 
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika 
        JOIN Ksiazki k ON w.ID_Ksiazki = k.ID_Ksiazki 
        JOIN Kategorie kat ON k.ID_Kategorii = kat.ID_Kategorii 
        WHERE kat.Nazwa_Kategorii = 'Fantastyka'
        INTERSECT
        SELECT c.Imie, c.Nazwisko FROM Czytelnicy c 
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika 
        JOIN Ksiazki k ON w.ID_Ksiazki = k.ID_Ksiazki 
        JOIN Kategorie kat ON k.ID_Kategorii = kat.ID_Kategorii 
        WHERE kat.Nazwa_Kategorii = 'Kryminał';

    :param conn: Obiekt aktywnego połączenia z bazą PostgreSQL.
    :return: Lista krotek z imionami i nazwiskami czytelników.
    """
    sql = """
        SELECT c.Imie, c.Nazwisko FROM Czytelnicy c 
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika 
        JOIN Ksiazki k ON w.ID_Ksiazki = k.ID_Ksiazki 
        JOIN Kategorie kat ON k.ID_Kategorii = kat.ID_Kategorii 
        WHERE kat.Nazwa_Kategorii = 'Fantastyka'
        INTERSECT
        SELECT c.Imie, c.Nazwisko FROM Czytelnicy c 
        JOIN Wypozyczenia w ON c.ID_Czytelnika = w.ID_Czytelnika 
        JOIN Ksiazki k ON w.ID_Ksiazki = k.ID_Ksiazki 
        JOIN Kategorie kat ON k.ID_Kategorii = kat.ID_Kategorii 
        WHERE kat.Nazwa_Kategorii = 'Kryminał';
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()

# ==============================================================================
# SEKCJA 2: ZAPYTANIA DLA SQLITE (Wymaga sqlite3)
# ==============================================================================

def get_katalog_osob(conn):
    """
    Zwraca ujednoliconą listę wszystkich osób figurujących w systemie (polimorfizm encji).
    Używa operatora zbiorowego UNION.

    **Zapytanie SQL:**::

        SELECT Imie, Nazwisko, 'Czytelnik' as Rola FROM Czytelnicy 
        UNION 
        SELECT Imie, Nazwisko, 'Autor' as Rola FROM Autorzy;

    :param conn: Obiekt połączenia z bazą SQLite.
    :return: Lista krotek (Imie, Nazwisko, Rola).
    """
    sql = """
        SELECT Imie, Nazwisko, 'Czytelnik' as Rola FROM Czytelnicy 
        UNION 
        SELECT Imie, Nazwisko, 'Autor' as Rola FROM Autorzy;
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def get_najdluzej_przetrzymywane(conn, limit_rekordow):
    """
    Wyszukuje aktualnie trwające wypożyczenia (brak zwrotu) posortowane od najstarszych.
    Wykorzystuje funkcję wierszową DATE().

    **Zapytanie SQL:**::

        SELECT k.Tytul, c.Imie, c.Nazwisko, DATE(w.Data_Wypozyczenia) as Data 
        FROM Wypozyczenia w 
        JOIN Czytelnicy c ON w.ID_Czytelnika = c.ID_Czytelnika 
        JOIN Ksiazki k ON w.ID_Ksiazki = k.ID_Ksiazki 
        WHERE w.Data_Zwrotu IS NULL 
        ORDER BY w.Data_Wypozyczenia ASC 
        LIMIT ?;

    :param conn: Obiekt połączenia z bazą SQLite.
    :param limit_rekordow: Liczba zwracanych wyników.
    :return: Lista niezakończonych wypożyczeń.
    """
    sql = """
        SELECT k.Tytul, c.Imie, c.Nazwisko, DATE(w.Data_Wypozyczenia) as Data 
        FROM Wypozyczenia w 
        JOIN Czytelnicy c ON w.ID_Czytelnika = c.ID_Czytelnika 
        JOIN Ksiazki k ON w.ID_Ksiazki = k.ID_Ksiazki 
        WHERE w.Data_Zwrotu IS NULL 
        ORDER BY w.Data_Wypozyczenia ASC 
        LIMIT ?;
    """
    cur = conn.cursor()
    cur.execute(sql, (limit_rekordow,))
    return cur.fetchall()

def get_puste_kategorie(conn):
    """
    Pobiera nazwy kategorii bez przypisanych książek.
    Demonstruje wykorzystanie LEFT JOIN w celu znalezienia brakujących relacji (IS NULL).

    **Zapytanie SQL:**::

        SELECT kat.Nazwa_Kategorii FROM Kategorie kat 
        LEFT JOIN Ksiazki k ON kat.ID_Kategorii = k.ID_Kategorii 
        WHERE k.ID_Ksiazki IS NULL;

    :param conn: Obiekt połączenia z bazą SQLite.
    :return: Lista pustych kategorii.
    """
    sql = """
        SELECT kat.Nazwa_Kategorii FROM Kategorie kat 
        LEFT JOIN Ksiazki k ON kat.ID_Kategorii = k.ID_Kategorii 
        WHERE k.ID_Ksiazki IS NULL;
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def get_raport_autorow(conn):
    """
    Tworzy zaawansowany raport o autorach, zliczając ich dzieła oraz wskazując tytuł chronologicznie najnowszego dzieła.
    Używa podzapytania nieskorelowanego w klauzuli SELECT.

    **Zapytanie SQL:**::

        SELECT a.Imie, a.Nazwisko, COUNT(k.ID_Ksiazki) as Suma_dziel, 
            (SELECT Tytul FROM Ksiazki WHERE ID_Autora = a.ID_Autora ORDER BY Rok_Wydania DESC LIMIT 1) as Najnowsza 
        FROM Autorzy a 
        LEFT JOIN Ksiazki k ON a.ID_Autora = k.ID_Autora 
        GROUP BY a.ID_Autora;

    :param conn: Obiekt połączenia z bazą SQLite.
    :return: Zestawienie analityczne dorobku autorów.
    """
    sql = """
        SELECT a.Imie, a.Nazwisko, COUNT(k.ID_Ksiazki) as Suma_dziel, 
            (SELECT Tytul FROM Ksiazki WHERE ID_Autora = a.ID_Autora ORDER BY Rok_Wydania DESC LIMIT 1) as Najnowsza 
        FROM Autorzy a 
        LEFT JOIN Ksiazki k ON a.ID_Autora = k.ID_Autora 
        GROUP BY a.ID_Autora;
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def get_srednia_wypozyczen_na_czytelnika(conn):
    """
    Oblicza średnią liczbę wypożyczonych książek na aktywnego czytelnika.
    Wykorzystuje podzapytanie w klauzuli FROM do zagnieżdżonej agregacji danych.

    **Zapytanie SQL:**::

        SELECT AVG(suma) FROM (
            SELECT COUNT(ID_Wypozyczenia) as suma 
            FROM Wypozyczenia GROUP BY ID_Czytelnika
        );

    :param conn: Obiekt połączenia z bazą SQLite.
    :return: Średnia wartość zmiennoprzecinkowa.
    """
    sql = """
        SELECT AVG(suma) FROM (
            SELECT COUNT(ID_Wypozyczenia) as suma 
            FROM Wypozyczenia GROUP BY ID_Czytelnika
        );
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()
