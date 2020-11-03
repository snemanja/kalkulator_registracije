from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class KalkulatorRegistracije:

    def __init__(self, root):
        #Definisanje tipa podataka koja se unose u polja
        self.unos_snage_motora_entry = StringVar(root, value='')
        self.unos_zapremine_motora_entry = StringVar(root, value='')
        self.unos_godista_entry = StringVar(root, value='')

        #Definisanje izgleda glavnog prozora, naziva polja, polja za unos, dugmadi i padajućih menija
        root.title("Kalkulator registracije")
        root.geometry("525x550")
        root.resizable(width=False, height=False)
        izgled = ttk.Style()
        izgled.configure("TButton", font="Arial 12", padding=3)
        izgled.configure("TEntry", font="Arial 12", padding=3)
        unos_snage_motora_label = ttk.Label(root, text="Snaga motora:")
        unos_snage_motora_label.grid(column=1, row=0, sticky=W)
        self.broj_snage_motora_entry = ttk.Entry(root, textvariable=self.unos_snage_motora_entry, width=20)
        self.broj_snage_motora_entry.grid(row=0, column=2, sticky=(W, E))
        self.broj_snage_motora_entry.focus()
        unos_zapremine_motora_label = ttk.Label(root, text='Zapremina motora:')
        unos_zapremine_motora_label.grid(column=1, row=1, sticky=W)
        self.broj_zapremine_motora_entry = ttk.Entry(root, textvariable=self.unos_zapremine_motora_entry, width=20)
        self.broj_zapremine_motora_entry.grid(row=1, column=2, sticky=(W, E))
        unos_godista_label = Label(root, text="Godište vozila:")
        unos_godista_label.grid(column=1, row=2, sticky=W)
        self.broj_godista_entry = ttk.Entry(root, textvariable=self.unos_godista_entry, width=20)
        self.broj_godista_entry.grid(row=2, column=2, sticky=(W, E))
        unos_premijskog_stepena_label = ttk.Label(root, text="Koji je Vaš trenutni\n premijski stepen?")
        unos_premijskog_stepena_label.grid(column=1, row=3, sticky=W)
        self.unos_premijskog_stepena_combobox = ttk.Combobox(root, state="readonly", width=2, textvariable=None,
                                                             values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        self.unos_premijskog_stepena_combobox.grid(column=2, row=3, sticky=W)
        self.unos_premijskog_stepena_combobox.current(3)
        broj_steta_label = ttk.Label(root, text="Koliko ste šteta imali\n u proteklih godinu dana?")
        broj_steta_label.grid(column=1, row=4, sticky=W)
        self.broj_steta_combobox = ttk.Combobox(root, state="readonly", width=2, textvariable=None,
                                                values=[0, 1, 2, 3])
        self.broj_steta_combobox.grid(column=2, row=4, sticky=W)
        self.broj_steta_combobox.current(0)
        nova_saobr_label = ttk.Label(root, text="Da li treba da napravite\n novu saobraćajnu dozvolu?")
        nova_saobr_label.grid(column=1, row=5, sticky=W)
        self.nova_saobr_combobox = ttk.Combobox(root, state="readonly", width=5, textvariable=None, values=["Da", "Ne"])
        self.nova_saobr_combobox.grid(column=2, row=5, sticky=W)
        self.nova_saobr_combobox.current(1)
        nove_tablice_label = ttk.Label(root, text="Da li Vam trebaju nove tablice?")
        nove_tablice_label.grid(column=1, row=6, sticky=W)
        self.nove_tablice_combobox = ttk.Combobox(root, width=5, textvariable=None, values=["Da", "Ne"])
        self.nove_tablice_combobox.grid(column=2, row=6, sticky=W)
        self.nove_tablice_combobox.current(1)
        unos_opstine_label = ttk.Label(root, text="Kojoj opštini pripadate:")
        unos_opstine_label.grid(column=1, row=7, sticky=W)
        self.unos_opstine_combobox = ttk.Combobox(root, state="readonly", width=12, textvariable=None,
                                                  values=["Novi Sad", "Beograd", "Sombor"])
        self.unos_opstine_combobox.grid(column=2, row=7, sticky=W)
        self.unos_opstine_combobox.current(0)
        self.izracunaj_button = ttk.Button(root, text="Izračunaj", command=self.ispis_rezultata)
        self.izracunaj_button.grid(column=1, row=8, sticky=(W, E))
        self.izracunaj_button.bind("<Return>", self.ispis_rezultata)
        self.izbrisi_button = ttk.Button(root, text="Izbriši", command=self.brisanje_polja)
        self.izbrisi_button.grid(column=2, row=8, sticky=(W, E))
        self.izbrisi_button.bind("<Return>", self.brisanje_polja)
        self.izadji_button = ttk.Button(root, text="Izađi", command=self.izlazak)
        self.izadji_button.grid(column=3, row=8, sticky=(W, E))
        self.izadji_button.bind("<Return>", self.izlazak)

    def uporedjivanje_brojeva(self, unos, prvi_broj: int, drugi_broj: int):
        if prvi_broj < unos <= drugi_broj:
            return True
        else:
            return False

    def uzimanje_podataka_snaga_motora(self):
        try:
            snaga_motora = int(self.unos_snage_motora_entry.get())
            return snaga_motora
        except(ValueError, AssertionError):
            self.greska()

    def uzimanje_podataka_zapremina_motora(self):
        try:
            zapremina_motora = int(self.unos_zapremine_motora_entry.get())
            return zapremina_motora
        except(ValueError, AssertionError):
            self.greska()

    def uzimanje_podataka_godiste_vozila(self):
        try:
            godiste_vozila = int(self.unos_godista_entry.get())
            return godiste_vozila
        except(ValueError, AssertionError):
            self.greska()

    def nova_saobracajna(self):
        saobracajna_dozvola = self.nova_saobr_combobox.get()
        if saobracajna_dozvola == "Da":
            saobracajna_dozvola = 1320.00
        else:
            saobracajna_dozvola = 0
        return saobracajna_dozvola

    def nove_tablice(self):
        tablice = self.nove_tablice_combobox.get()
        if tablice == "Da":
            iznos_tablice = 2203.00
        else:
            iznos_tablice = 0

        return iznos_tablice

    def premija(self):
        global iznos_premije
        if self.uporedjivanje_brojeva(self.uzimanje_podataka_snaga_motora(), 1, 22):
            iznos_premije = 7844
        elif self.uporedjivanje_brojeva(self.uzimanje_podataka_snaga_motora(), 22, 33):
            iznos_premije = 9370
        elif self.uporedjivanje_brojeva(self.uzimanje_podataka_snaga_motora(), 33, 44):
            iznos_premije = 10908
        elif self.uporedjivanje_brojeva(self.uzimanje_podataka_snaga_motora(), 44, 55):
            iznos_premije = 12447
        elif self.uporedjivanje_brojeva(self.uzimanje_podataka_snaga_motora(), 55, 66):
            iznos_premije = 13974
        elif self.uporedjivanje_brojeva(self.uzimanje_podataka_snaga_motora(), 66, 84):
            iznos_premije = 16025
        elif self.uporedjivanje_brojeva(self.uzimanje_podataka_snaga_motora(), 84, 110):
            iznos_premije = 19090
        elif self.uzimanje_podataka_snaga_motora() > 110:
            iznos_premije = 22666
        else:
            self.greska()
        return iznos_premije

    def unos_broja_steta(self):
        global premijski_stepen
        premijski_stepen = int(self.unos_premijskog_stepena_combobox.get())
        broj_steta = int(self.broj_steta_combobox.get())
        if broj_steta == 0:
            premijski_stepen += 0
        elif broj_steta == 1:
            premijski_stepen += 4
        elif broj_steta == 2:
            premijski_stepen += 7
        elif broj_steta == 3:
            premijski_stepen += 10
        return premijski_stepen

    def premijski_stepen(self):
        global novi_premijski_stepen
        prem_step = self.unos_broja_steta()
        if prem_step == 1:
            novi_premijski_stepen = prem_step
        elif prem_step in range(2, 13):
            novi_premijski_stepen = prem_step - 1
        elif prem_step > 12:
            novi_premijski_stepen = 12
        return novi_premijski_stepen

    def racunanje_premije(self):
        global novi_iznos_premije
        novi_iznos_premije = self.premija()
        novi_premijski_stepen_1 = self.premijski_stepen()
        prem_stepen_racunanje = {1: 0.75, 2: 0.85, 3: 0.95, 4: 1, 5: 1.15, 6: 1.3,
                                 7: 1.5, 8: 1.7, 9: 1.9, 10: 2.1, 11: 2.3, 12: 2.5}
        for k, v in prem_stepen_racunanje.items():
            if novi_premijski_stepen_1 == k:
                novi_iznos_premije *= v
        return novi_iznos_premije

    def porez(self):
        global porez
        if self.uporedjivanje_brojeva(self.uzimanje_podataka_godiste_vozila(), 1950, 1999):
            if self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 0, 1150):
                porez = 258
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora, 1150, 1300):
                porez = 506
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora, 1300, 1600):
                porez = 1114
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora, 1600, 2000):
                porez = 2284
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora, 2000, 2500):
                porez = 11286
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 2500, 3000):
                porez = 22870
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 3000, 10000):
                porez = 47268
            else:
                self.greska()
        if self.uporedjivanje_brojeva(self.uzimanje_podataka_godiste_vozila(), 1999, 2008):
            if self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 0, 1150):
                porez = 774
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1150, 1300):
                porez = 1518
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1300, 1600):
                porez = 3342
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1600, 2000):
                porez = 6852
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 2000, 2500):
                porez = 33858
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 2500, 3000):
                porez = 68610
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 3000, 10000):
                porez = 141804
            else:
                self.greska()
        if self.uporedjivanje_brojeva(self.uzimanje_podataka_godiste_vozila(), 2008, 2010):
            if self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 0, 1150):
                porez = 967
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1150, 1300):
                porez = 1897
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1300, 1600):
                porez = 4177
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1600, 2000):
                porez = 8565
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 2000, 2500):
                porez = 42322
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 2500, 3000):
                porez = 85762
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 3000, 10000):
                porez = 177255
            else:
                self.greska()
        if self.uporedjivanje_brojeva(self.uzimanje_podataka_godiste_vozila(), 2010, 2013):
            if self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1, 1150):
                porez = 1096
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1150, 1300):
                porez = 2150
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1300, 1600):
                porez = 4734
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1600, 2000):
                porez = 9707
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 2000, 2500):
                porez = 47965
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 2500, 3000):
                porez = 97197
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 3000, 10000):
                porez = 200889
            else:
                self.greska()
        if self.uporedjivanje_brojeva(self.uzimanje_podataka_godiste_vozila(), 2013, 2019):
            if self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1, 1150):
                porez = 1290
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1150, 1300):
                porez = 2530
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1300, 1600):
                porez = 5570
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 1600, 2000):
                porez = 11420
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 2000, 2500):
                porez = 56430
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 2500, 3000):
                porez = 114350
            elif self.uporedjivanje_brojeva(self.uzimanje_podataka_zapremina_motora(), 3000, 10000):
                porez = 236340
            else:
                self.greska()
        if self.uzimanje_podataka_godiste_vozila() < 1950:
            self.greska()

        return porez

    def nalepnica(self):
        global iznos_nalepnice
        iznos_nalepnice = 440
        return iznos_nalepnice

    def zahtev(self):
        global iznos_zahteva
        iznos_zahteva = 320
        return iznos_zahteva

    def unos_opstine(self):
        global komunalna_taksa
        db_conn = sqlite3.connect('opstine_db.db')
        cursor = db_conn.cursor()
        try:
            unos_opstine_value = self.unos_opstine_combobox.get().lower()
            if " " in unos_opstine_value:
                unos_opstine_value = unos_opstine_value.replace(" ", "_")
                cursor.execute(
                    'SELECT iznos_kom_takse FROM {} WHERE zapremina_vozila = (SELECT MAX(zapremina_vozila) '
                    'FROM {} WHERE zapremina_vozila <= {});'.format(unos_opstine_value, unos_opstine_value,
                                                                self.uzimanje_podataka_zapremina_motora()))
            else:
                cursor.execute(
                    'SELECT iznos_kom_takse FROM {} WHERE zapremina_vozila = (SELECT MAX(zapremina_vozila) '
                    'FROM {} WHERE zapremina_vozila <= {});'.format(unos_opstine_value, unos_opstine_value,
                                                                self.uzimanje_podataka_zapremina_motora()))

            komunalna_taksa_2 = cursor.fetchone()
            komunalna_taksa_3 = [int(''.join(map(str, number))) for number in (komunalna_taksa_2,)]
            komunalna_taksa_4 = [str(i) for i in komunalna_taksa_3]
            komunalna_taksa = int("".join(komunalna_taksa_4))
            return komunalna_taksa

        except sqlite3.OperationalError as e:
            print("Error: ", str(e))

        db_conn.close()

    def greska(self):
        messagebox.showinfo("Pogresan unos",
                            "Nepravilan unos podataka.\n Forma ne prihvata negativne brojeve, \n "
                            "alfanumericke karatkere kao i specijalne karaktere.\n"
                            " Molimo Vas, pokusajte ponovo.")

    def izracunaj(self, *args):
        global ukupno
        ukupno = self.racunanje_premije() + self.unos_opstine() + self.nova_saobracajna() + self.nove_tablice() + self.porez() + self.nalepnica() + self.zahtev()
        return ukupno

    def ispis_rezultata(self, *args):
        global ispis_premije, ispis_komunalne_takse, ispis_poreza, ispis_nalepnice, ispis_zahteva, iznos_nove_saobracajne_dozvole,\
            iznos_novih_tablica, prazno_polje, ukupan_iznos_registracije
        ispis_premije = Label(root, text='Vaš novi premijski stepen je {}, a polisa za Vaš auto iznosi %10.2f din'
                              .format(self.premijski_stepen()) % round(self.racunanje_premije()))
        ispis_premije.grid(column=1, row=10, columnspan=4, sticky=W)
        ispis_komunalne_takse = Label(root, text='Iznos komunalne takse je: %10.2f din' % self.unos_opstine())
        ispis_komunalne_takse.grid(column=1, row=11, columnspan=4, sticky=W)
        ispis_poreza = Label(root, text='Iznos poreza za vozilo je: %10.2f din' % self.porez())
        ispis_poreza.grid(column=1, row=12, columnspan=4,  sticky=W)
        ispis_nalepnice = Label(root, text='Iznos za nalepnicu je: %10.2f din' % self.nalepnica())
        ispis_nalepnice.grid(column=1, row=13, columnspan=4, sticky=W)
        ispis_zahteva = Label(root, text='Iznos zahteva za registraciju je: %10.2f din' % self.zahtev())
        ispis_zahteva.grid(column=1, row=14, columnspan=4, sticky=W)
        nova_saob = self.nova_saobr_combobox.get()
        if nova_saob == "Da":
            iznos_nove_saobracajne_dozvole = Label(root, text='Iznos za novu saobraćajnu dozvolu je: %10.2f din'
                                                              % self.nova_saobracajna())
            iznos_nove_saobracajne_dozvole.grid(column=1, row=15, sticky=W, columnspan=4)
        nove_tab = self.nove_tablice_combobox.get()
        if nove_tab == "Da":
            iznos_novih_tablica = Label(root, text='Iznos za nove tablice je: %10.2f din' % self.nove_tablice())
            iznos_novih_tablica.grid(column=1, row=16, sticky=W, columnspan=4)
        prazno_polje = Label(root, text="-"*100)
        prazno_polje.grid(column=1, row=17, columnspan=4, sticky=W)
        ukupan_iznos_registracije = Label(root, text='Ukupan iznos registracije je: %10.2f din' % round(self.izracunaj()))
        ukupan_iznos_registracije.grid(column=1, row=18, columnspan=4, sticky=W)

    def izlazak(*args):
        root.destroy()

    def brisanje_polja(self):
        ispis_premije.destroy()
        ispis_komunalne_takse.destroy()
        ispis_poreza.destroy()
        ispis_nalepnice.destroy()
        ispis_zahteva.destroy()
        nova_saob = self.nova_saobr_combobox.get()
        if nova_saob == "Da":
            iznos_nove_saobracajne_dozvole.destroy()
        nove_tab = self.nove_tablice_combobox.get()
        if nove_tab == "Da":
            iznos_novih_tablica.destroy()
        prazno_polje.destroy()
        ukupan_iznos_registracije.destroy()
        self.broj_snage_motora_entry.delete(0, END)
        self.broj_snage_motora_entry.focus_set()
        self.broj_zapremine_motora_entry.delete(0, END)
        self.broj_godista_entry.delete(0, END)
        self.unos_premijskog_stepena_combobox.current(3)
        self.broj_steta_combobox.current(0)
        self.unos_opstine_combobox.current(0)
        self.nova_saobr_combobox.current(1)
        self.nove_tablice_combobox.current(1)


root = Tk()
kalkulator = KalkulatorRegistracije(root)
root.mainloop()
