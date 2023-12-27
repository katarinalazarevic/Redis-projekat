import psycopg2
from config import Config



try:
    # Otvorite kursor za izvršavanje SQL upita
    cursor = Config.conn.cursor()

    # Primer SELECT upita
    cursor.execute("SELECT * FROM ime_tabele;")

    # Dobijanje rezultata SELECT upita
    records = cursor.fetchall()

    # Prikazivanje rezultata
    for row in records:
        print("ID =", row[0], "Ime =", row[1], "Prezime =", row[2])

except (Exception, psycopg2.Error) as error:
    print("Greška prilikom rada sa bazom podataka:", error)

finally:
    # Zatvaranje kursora i veze
    if Config.conn:
        cursor.close()
        Config.conn.close()
        print("Veza zatvorena.")