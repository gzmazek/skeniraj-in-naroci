# Skeniraj in naroci

Projekt pri predmetu Osnove podatkovnih baz iz študijskega leta 2023/2024 na Fakulteti za matematiko in fiziko Univerze v Ljubljani.

Avtorja: Gal Zmazek in Vito Levstik

## ER Diagram
![ER diagram](https://github.com/gzmazek/skeniraj-in-naroci/blob/main/ER_diagram.png?raw=true)

## Opis Projekta

Projekt "Skeniraj in naroci" je sistem za upravljanje naročil v restavracijah. Glavni namen aplikacije je omogočiti preprosto oddajo naročil preko mobilne naprave s skeniranjem QR kode, upravljanje z meniji restavracij ter pridobivanje analitike o poslovanju restavracij.

## Navodila za Uporabo

### Namestitev

1. **Kloniranje repozitorija:**

   ```bash
   git clone https://github.com/gzmazek/skeniraj-in-naroci.git
   cd skeniraj-in-naroci
   ```

2. **Nastavitev virtualnega okolja:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Na Windows: venv\Scripts\activate
   ```

3. **Namestitev odvisnosti:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Migracija podatkovne baze:**

   ```bash
   python manage.py migrate
   ```

5. **Zagon razvojnega strežnika:**

   ```bash
   python manage.py runserver
   ```

### Uporaba Aplikacije

1. **Prijava:**
   Prijavite se z uporabniškim računom. Če račun še ne obstaja, ga lahko ustvarite prek administratorskega vmesnika ali pa dodate uporabnike neposredno v bazo.

2. **Dodajanje Restavracije:**
   V navigacijskem meniju izberite možnost za dodajanje nove restavracije. Po vnosu podatkov o restavraciji (ime, lokacija) lahko začnete upravljati z meniji, mizami in naročili.

3. **Upravljanje Menijev:**
   Po dodajanju restavracije lahko urejate meni restavracije in dodajate nove artikle. Vsak artikel ima določeno ceno in oznake (tags).

4. **Oddaja Naročil:**
   Uporabniki lahko skenirajo QR kodo, povezano z določeno mizo v restavraciji, in oddajo naročilo neposredno iz mobilne naprave.

5. **Analitika:**
   V zavihku "Analitika" lahko pregledate različne statistike o naročilih, kot so povprečna vrednost naročila, prihodek po urah, prihodek glede na vrsto strank (novi ali vračajoči se gostje) itd.

### Poudarek na Restavraciji Kavarna Rog

Za potrebe testiranja in demonstracije aplikacije je bila uporabljena restavracija *Kavarna Rog*. Podatki za to restavracijo so bili simulirani. Spodaj je prikazana koda, ki je bila uporabljena za simulacijo podatkov:

```sql
DO $$
DECLARE
    table_id INTEGER;
    user_id INTEGER;
    order_id INTEGER;
    order_date TIMESTAMP;
    item_id INTEGER;
    item_quantity INTEGER;
    order_status VARCHAR(50);
    item_status VARCHAR(50);
BEGIN
    FOR i IN 1..9000 LOOP  -- simulacija 9000 naročil
        SELECT id INTO table_id FROM DiningTable WHERE restaurant_id = (SELECT id FROM Restaurant WHERE name = 'Kavarna Rog') ORDER BY RANDOM() LIMIT 1;
        -- Izbere se naključna miza v restavraciji Kavarna Rog
        SELECT id INTO user_id FROM AppUser ORDER BY RANDOM() LIMIT 1;
        -- Izbere se naključni uporabnik
        SELECT NOW() - INTERVAL '5 months' * RANDOM() INTO order_date;
        -- Izbere se naključen datum v zadnjih 5 mesecih

        -- Določitev statusa naročila glede na datum naročila
        IF order_date >= NOW() - INTERVAL '10 hours' THEN
            order_status := 'IN PROGRESS';
            item_status := 'pending';
        ELSE
            order_status := 'FINISHED';
            item_status := 'prepared';
        END IF;

        -- Vstavi novo naročilo z določenim statusom
        INSERT INTO CustomerOrder (status, date, table_id, user_id)
        VALUES (order_status, order_date, table_id, user_id)
        RETURNING id INTO order_id;

        -- Vstavi od 1 do 5 artiklov za vsako naročilo v Kavarna Rog
        FOR j IN 1..(FLOOR(RANDOM() * 5 + 1))::INTEGER LOOP
            SELECT rm.item_id INTO item_id FROM RestaurantMenu rm
            WHERE rm.restaurant_id = (SELECT id FROM Restaurant WHERE name = 'Kavarna Rog')
            ORDER BY RANDOM() LIMIT 1;
            
            -- Naključna količina med 1 in 4
            SELECT FLOOR(RANDOM() * 4 + 1)::INTEGER INTO item_quantity;

            -- Vstavi artikle z določenim statusom
            INSERT INTO OrderItem (customer_order_id, item_id, quantity, status)
            VALUES (order_id, item_id, item_quantity, item_status);
        END LOOP;
    END LOOP;
END $$;
```

### Orodja in Tehnologije

- **Python & Django**: Backend razvoj in upravljanje podatkovne baze.
- **PostgreSQL**: Relacijska podatkovna baza.
- **HTML, CSS, Bootstrap**: Uporabniški vmesnik.
- **Chart.js**: Vizualizacija podatkov (grafi in analitika).

### Zaključek

Projekt "Skeniraj in naroci" je zasnovan kot celovita rešitev za upravljanje naročil v restavracijah z dodatnimi analitičnimi orodji za izboljšanje poslovanja. Simulacija podatkov za restavracijo *Kavarna Rog* omogoča testiranje funkcionalnosti aplikacije in demonstracijo naprednih SQL poizvedb, ki so uporabljene za analizo poslovnih podatkov.
```
