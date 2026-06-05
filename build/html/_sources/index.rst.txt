================================================
Sprawozdanie z Laboratorium: Bazy Danych
================================================

**Autorzy projektu:** Paweł Łoćwin, Paweł Łosowski

Wprowadzenie
============

Niniejsza dokumentacja stanowi kompletne sprawozdanie z laboratorium przedmiotu Bazy Danych. Projekt obejmuje całościową analizę procesów związanych z administracją i projektowaniem relacyjnych systemów baz danych, od teoretycznych aspektów konserwacji i optymalizacji, poprzez badania literaturowe, aż po praktyczną implementację systemu zarządzania biblioteką.

Struktura dokumentacji
======================

Dokumentacja została podzielona na cztery główne sekcje:

1. **Rozdział 1: Kontrola i konserwacja** – Analiza fundamentalnych procesów administracyjnych niezbędnych do utrzymania wysokiej dostępności i wydajności systemu bazodanowego. Obejmuje VACUUM, optymalizację planisty zapytań, bezpieczeństwo oraz strategie zabezpieczania przed utratą danych.

2. **Rozdział 2: Badania literaturowe** – Przegląd źródeł akademickich i naukowo-technicznych dotyczących baz danych, ich architektury, optymalizacji i bezpieczeństwa.

3. **Rozdział 3: Projektowanie bazy danych** – Praktyczne modelowanie systemu zarządzania bibliotecznym katalogiem wypożyczeń. Sekcja obejmuje analizę wymagań, model konceptualny (notacja Chena), proces normalizacji (1NF, 2NF, 3NF) oraz diagram ERD dla dwóch środowisk (SQLite i PostgreSQL).

4. **Rozdział 4: Implementacja fizyczna i zasilanie bazy** – Realizacja fizycznego schematu bazy danych poprzez skrypty DDL, mechanizmy importu danych oraz automatyzacja zasilania bazy przy użyciu Python i plików CSV.

.. toctree::
   :maxdepth: 1
   :numbered:

   rozdzial_1/index
   rozdzial_2/index
   rozdzial_3/index
   rozdzial_4/index
