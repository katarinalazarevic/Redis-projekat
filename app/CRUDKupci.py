from app.routesKupac import Kupac

def azuriraj_kupca():
    id_za_azuriranje = input("Unesite ID kupca za ažuriranje: ")
    kupac_za_azuriranje = Kupac.get_by_id(id_za_azuriranje)

    if kupac_za_azuriranje:
        novo_ime = input("Unesite novo ime kupca: ")
        novi_email = input("Unesite novi email kupca: ")

        kupac_za_azuriranje.update(name=novo_ime, email=novi_email)
        print(f'Informacije o {kupac_za_azuriranje.name} su uspešno ažurirane.')
    else:
        print('Kupac nije pronađen!')

def obrisi_kupca():
    id_za_brisanje = input("Unesite ID kupca za brisanje: ")
    kupac_za_brisanje = Kupac.get_by_id(id_za_brisanje)

    if kupac_za_brisanje:
        kupac_za_brisanje.delete()
        print(f'Kupac {kupac_za_brisanje.name} je uspešno obrisan.')
    else:
        print('Kupac nije pronađen!')
