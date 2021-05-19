import budynek
import pracownik
from datetime import date

#do czytania
def miej_read(cursor):
    cursor.execute("SELECT dzielnica "
                   "FROM mieszkanie "
                   "GROUP BY dzielnica;")
    dzielnica = cursor.fetchall()
    for x in dzielnica:
        print("Pracownicy budynków " + x[0] + ":")

        cursor.execute("SELECT miejsce_pracy.NRB, miejsce_pracy.ulica, zawod.nazwa, pracownik.Imie, pracownik.Nazwisko, pracownik.Nazwisko2, miejsce_pracy.data_zatrudnienia, miejsce_pracy.data_zwolnienia "
                       "FROM miejsce_pracy "
                       "INNER JOIN pracownik ON pracownik.IDP = miejsce_pracy.IDP "
                       "INNER JOIN zawod ON zawod.IDZ = pracownik.IDZ "
                       f"WHERE miejsce_pracy.dzielnica = '{x[0]}' "
                       "ORDER BY miejsce_pracy.ulica, miejsce_pracy.NRB, zawod.IDZ;")

        mp = cursor.fetchall()
        length = [len("Ulica"),len("Zawód"), len("Imię"), len("Nazwisko")]
        help = ''
        print("Czy wyświetlić pracowników, którzy zostali już zwolnieni? (y/n/exit)")
        while help == '':
            help = input()
            if (help == 'exit'):
                return 0
            elif (help == 'y'):
                help = 1
            elif (help == 'n'):
                help = 0
            else:
                help = ''
                print("proszę poszę napisać 'y', 'n' lub 'exit'")


        for i in mp:
            if (i[5] is None):
                help2 = 0
            else:
                help2 = 1

            if (length[0] < len(str(i[1]))):
                length[0] = len(str(i[1]))
            if (length[1] < len(str(i[2]))):
                length[1] = len(str(i[2]))
            if (length[2] < len(str(i[3]))):
                length[2] = len(str(i[3]))
            if (length[3] < len(str(i[4]) + '-' * help2 + help2 * str(i[5]))):
                length[3] = len(str(i[4]) + '-' * help2 + help2 * str(i[5]))

        print("Nr budynku"  + " " * 2 +
              "Ulica"       + " " * (length[0] - len("Ulica") + 2) +
              "Zawód"       + " " * (length[1] - len("Zawód") + 2) +
              "Imię"        + " " * (length[2] - len("Imię")  + 2) +
              "Nazwisko"    + " " * (length[3] - len("Nazwisko") + 2) +
              "Zatrudnienie"+ " " * 2 +
              "Zwolnienie" * int(help))

        for i in mp:
            if (i[5] is None):
                help2 = 0
            else:
                help2 = 1

            if((help == 0 and i[7] is None) or help == 1):
                print(str(i[0]) + " " * (len("Nr budynku")-len(str(i[0])) + 2) +
                      str(i[1]) + " " * (length[0] - len(str(i[1])) + 2) +
                      str(i[2]) + " " * (length[1] - len(str(i[2])) + 2) +
                      str(i[3]) + " " * (length[2] - len(str(i[3])) + 2) +
                      str(i[4]) + "-" * help2 + str(i[5]) * help2 + " " * ( length[3] - len(str(i[4]) + '-' * help2 + str(i[5]) * help2) + 2) +
                      str(i[6]), end = '' * help + '\n' * (1-help))
            if (help == 1):
                print(" " * (len("Zatrudnienie")-len(str(i[6])) + 2) + str(i[7]))

#do tworzenia
def miej_cr_date():
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")

    rok = ''
    print("Proszę podać rok:")
    while rok == '':
        rok = input()
        if(rok == 'exit'):
            return 0
        elif(len(rok) != 4):
            print("Proszę podać rok jako 4 liczby")
            rok = ''
        else:
            try:
                rok = int(rok)
            except:
                print("proszę wpisać tylko liczby")
                rok = ''
            else:
                if(rok > int(year) or rok < int(year) - 150):
                    print("nie można zatrudnić osoby w przyszłości lub mającej ponad 150 lat,"
                          " umowa nie miała jak zostać podpisana")
                    rok = ''

    miesiac = ''
    print("Proszę podać miesiąc:")
    while miesiac == '':
        miesiac = input()
        if(miesiac == 'exit'):
            return 0
        elif(len(miesiac) != 1 and len(miesiac) != 2):
            print("Proszę podać rok jako 1 lub 2 liczby")
            miesiac = ''
        else:
            try:
                miesiac = int(miesiac)
            except:
                print("proszę wpisać tylko liczby")
                miesiac = ''
            else:
                if(miesiac < 1 or miesiac > 12):
                    print("nie ma takiego miesiąca (liczba od 1 do 12)")
                    miesiac = ''
                elif(rok == int(year) and miesiac > int(month)):
                    print("nie można zatrudnić osoby w przyszłości, umowa nie miała jak zostać podpisana")
                    miesiac = ''

    dzien = ''
    print("Proszę podać dzień:")
    while dzien == '':
        dzien = input()
        if(dzien == 'exit'):
            return 0
        elif(len(dzien) != 1 and len(dzien) != 2):
            print("Proszę podać rok jako 1 lub 2 liczby")
            dzien = ''
        else:
            try:
                dzien = int(dzien)
            except:
                print("proszę wpisać tylko liczby")
                dzien = ''
            else:
                if(miesiac == 1 or miesiac == 3 or miesiac == 5 or miesiac == 7 or miesiac == 8 or miesiac == 10 or miesiac == 12):
                    if(dzien < 1 or dzien > 31):
                        print("Nie ma takiego dnia w tym miesiącu")
                        dzien = ''
                elif(miesiac == 4 or miesiac == 6 or miesiac == 9 or miesiac == 11):
                    if (dzien < 1 or dzien > 30):
                        print("Nie ma takiego dnia w tym miesiącu")
                        dzien = ''
                elif(miesiac == 2 and rok % 4 == 0):
                    if (dzien < 1 or dzien > 29):
                        print("Nie ma takiego dnia w tym miesiącu")
                        dzien = ''
                elif(miesiac == 2 and rok % 4 != 0):
                    if (dzien < 1 or dzien > 28):
                        print("Nie ma takiego dnia w tym miesiącu")
                        dzien = ''

                if(int(rok) == int(year) and int(miesiac) == int(month) and int(dzien) > int(day)):
                    print("nie można zatrudnić osoby w przyszłości, umowa nie miała jak zostać podpisana")
                    dzien = ''

    return [str(rok),str(miesiac),str(dzien)]

def miej_cr_check(cursor, IDP, dzielnica, ulica, numer):
    cursor.execute("SELECT data_zatrudnienia "
                   "FROM miejsce_pracy "
                   f"WHERE IDP = {IDP} "
                   f"AND dzielnica = '{dzielnica}' "
                   f"AND ulica = '{ulica}' "
                   f"AND NRB = {numer} "
                   f"AND data_zwolnienia IS NULL;")

    check = cursor.fetchall()
    try:
        x = check[0][0]
    except:
        return 1
    else:
        return 0

def miej_create(cursor):
    pracownik.prac_read(cursor)
    print("Który pracownik ma nowwą pracę?")
    dane = ''
    nr = ''
    while nr == '':
        nr = input()
        if (nr == 'exit'):
            return 0
        try:
            nr = int(nr)
        except:
            print("Proszę podać liczbę")
            nr = ''
        else:
            dane = pracownik.prac_up_info(cursor, nr)
            if (dane == -1):
                print("Proszę wybrać numer z listy")
                nr = ''
    help = 1
    if(dane[3] is None):
        help = 0
    print("W której dzielnicy ma to mieszkanie:")
    dzielnica = budynek.bud_del_dziel(cursor)
    if (dzielnica == 0):
        return 0
    print("Wybór ulicy:")
    ulica = budynek.bud_del_ul(cursor, dzielnica)
    if (ulica == 0):
        return 0
    print("Wybór numeru budynku:")
    numer = budynek.bud_del_no(cursor, dzielnica, ulica)
    if (numer == 0):
        return 0

    data = miej_cr_date()
    print("Nowo dodanej osoby nie można od razu zwolnić, jeśli jednak jest taka przeba, proszę udać się pod 'update'")
    print("Nowe zatrudnienie osoby w budynku:", dzielnica, ulica, numer)
    print("Pracownik:", dane[1],dane[2] + '-' * help + str(dane[3]) * help,dane[0])
    print("Zatrudniony w dniu:", data[0]+ '-' + data[1] + '-' + data[2])

    print("Czy chcesz zapisać nowy r3cord? (y/n)")
    while True:
        pom = input()
        if(pom == 'exit' or pom == 'n'):
            return 0
        elif(pom == 'y'):
            data_zat = data[0]+ '-' + data[1] + '-' + data[2]
            if(miej_cr_check(cursor,dane[5],dzielnica,ulica,numer) == 0):
                print("ta osoba już tam pracuje")
                return 0

            try:
                cursor.callproc("insert_miej", (dzielnica, ulica, numer, dane[5], data_zat))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się dodać r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

#do update'owania
def miej_up_read(cursor):
    cursor.execute(
        "SELECT miejsce_pracy.dzielnica, miejsce_pracy.ulica, miejsce_pracy.NRB, zawod.nazwa, pracownik.Imie, pracownik.Nazwisko, pracownik.Nazwisko2, miejsce_pracy.data_zatrudnienia, miejsce_pracy.IDP "
        "FROM miejsce_pracy "
        "INNER JOIN pracownik ON pracownik.IDP = miejsce_pracy.IDP "
        "INNER JOIN zawod ON zawod.IDZ = pracownik.IDZ "
        "WHERE miejsce_pracy.data_zwolnienia IS NULL "
        "ORDER BY miejsce_pracy.dzielnica, miejsce_pracy.ulica, miejsce_pracy.NRB, zawod.IDZ;")

    dane = cursor.fetchall()
    length = [len("dzielnica"),len("Ulica"), len("Zawód"), len("Imię"), len("Nazwisko")]

    for i in dane:
        if (i[5] is None):
            help2 = 0
        else:
            help2 = 1

        if (length[0] < len(str(i[0]))):
            length[0] = len(str(i[0]))
        if (length[1] < len(str(i[1]))):
            length[1] = len(str(i[1]))
        if (length[2] < len(str(i[3]))):
            length[2] = len(str(i[3]))
        if (length[3] < len(str(i[4]))):
            length[3] = len(str(i[4]))
        if (length[4] < len(str(i[5]) + '-' * help2 + help2 * str(i[6]))):
            length[4] = len(str(i[5]) + '-' * help2 + help2 * str(i[6]))

    print(" " * 7 +
          "Dzielnica" + " " * (length[0] - len("Dzielnica") + 2) +
          "Ulica" + " " * (length[1] - len("Ulica") + 2) +
          "Nr budynku" + " " * 2 +
          "Zawód" + " " * (length[2] - len("Zawód") + 2) +
          "Imię" + " " * (length[3] - len("Imię") + 2) +
          "Nazwisko" + " " * (length[4] - len("Nazwisko") + 2) +
          "Zatrudnienie")


    count = 0
    for i in dane:
        help = 1
        if(i[6] is None):
            help = 0
        count += 1

        print(str(count)    + "." + " " * (6 - len(str(count))) +
              i[0]          + " " * (length[0] - len(i[0]) + 2) +
              i[1]          + " " * (length[1] - len(i[1]) + 2) +
              str(i[2])     + " " * (len("Nr budynku") - len(str(i[2])) + 2) +
              i[3]          + " " * (length[2] - len(i[3]) + 2) +
              i[4]          + " " * (length[3] - len(i[4]) + 2) +
              str(i[5])     + "-" * help + str(i[6]) * help + " " * ( length[4] - len(str(i[5]) + '-' * help + str(i[6]) * help) + 2) +
              str(i[7]))

    print("Który r3cord zatrudnienia wybierasz?")
    while True:
        pom = input()
        if (pom == 'exit'):
            return 0
        try:
            pom = int(pom)
        except:
            print("proszę podać liczbę")
        else:
            if (pom < 1 or pom > len(dane)):
                print("proszę podać liczbę obok konkretnego r3cordu")
            else:
                return dane[pom - 1]

def miej_update(cursor):
    dane = miej_up_read(cursor)
    if(dane == 0):
        return 0
    help = 1
    if (dane[6] is None):
        help = 0

    print("Czy chcesz zmienić budynek? (y/n)")
    bud = ''
    while bud == '':
        bud = input()
        if (bud == 'exit'):
            return 0
        elif (bud == 'y'):
            dzielnica = budynek.bud_del_dziel(cursor)
            if (dzielnica == 0):
                return 0
            print("Wybór ulicy:")
            ulica = budynek.bud_del_ul(cursor, dzielnica)
            if (ulica == 0):
                return 0
            print("Wybór numeru budynku:")
            numer = budynek.bud_del_no(cursor, dzielnica, ulica)
            if (numer == 0):
                return 0
            bud = [dzielnica, ulica, numer]
        elif (bud != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            bud = ''

    print("Czy chcesz zmienić datę zatrudnienia tego pracownika? (y/n)")
    zatr = ''
    while zatr == '':
        zatr = input()
        if (zatr == 'exit'):
            return 0
        elif (zatr == 'y'):
            zatr = miej_cr_date()
            zatr = zatr[0] + '-' + zatr[1] + '-' + zatr[2]
            if(zatr == 0):
                return 0
        elif (zatr != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            zatr = ''



    if (bud == 'n'): bud = [dane[0],dane[1],dane[2]]
    if (zatr == 'n'): zatr = dane[7]
    if (bud == [dane[0],dane[1],dane[2]] and zatr == dane[7]):
        print("nic nie zostało zmienione")
        return 0

    print("Pracownik:", dane[4], dane[5]+ "-" * help + str(dane[6]) * help + " " + str(dane[3]))

    print("Stare dane:")
    print("Budynek:", dane[0],dane[1],dane[2])
    print("Data zatrudnienia:",dane[7])

    print("Nowe dane:")
    print("Budynek:", bud[0],bud[1],bud[2])
    print("Data zatrudnienia:",zatr)

    print("Czy chcesz zaktualizować te dane r3cordu? (y/n)")
    while True:
        pom = input()
        if (pom == 'n' or pom == 'exit'):
            return 0
        elif (pom == 'y'):
            if(bud != [dane[0],dane[1],dane[2]]):
                if(miej_cr_check(cursor,dane[8],bud[0],bud[1],bud[2]) == 0):
                    print("Ten pracownik już pracuje w tym budynku i jest to zapisane w osobnym r3cordzie")
                    return 0

            try:
                cursor.callproc("update_miej", (dane[0], dane[1], dane[2], bud[0], bud[1], bud[2], dane[8], zatr))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się edytować r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

#do usuwania
def miej_delete(cursor):
    dane = miej_up_read(cursor)
    if (dane == 0):
        return 0
    help = 1
    if (dane[6] is None):
        help = 0

    print("Dane r3cordu:")
    print("Budynek:", dane[0],dane[1],dane[2])
    print("Pracownik:", dane[4], dane[5] + "-" * help + str(dane[6]) * help + dane[3])
    print("Data zatrudnienia:",dane[7])

    print("Chcesz całkowicie usunąć rekord (y) czy tylko zwolnić pracownika (n)?")
    pom = ''
    while pom == '':
        pom = input()
        if (pom == 'exit'):
            return 0
        elif (pom == 'y'):

            try:
                cursor.callproc("delete_miej",(dane[0],dane[1],dane[2],dane[8]))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się usunąć r3cord")
                return 1
        elif(pom != 'n'):
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")
            pom = ''

    print("Czy na pewno chcesz zwolnić tego pracownika? (y/n)")
    zwol = ''
    while zwol == '':
        zwol = input()
        if (zwol == 'exit'):
            return 0
        elif(zwol == 'n'):
            print("Nie zmieni się więc kompletnie nic")
            return 0
        elif (zwol != 'n' and zwol != 'y'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            zwol = ''

    if (zwol == 'y'):
        print("Czy chcesz dać dzisiejszą datę jako datę zwolnienia? (y/n)")
        zwol = ''
        while zwol == '':
            zwol = input()
            if (zwol == 'exit'):
                return 0
            elif(zwol == 'y'):
                zwol = str(date.today())
            elif(zwol == 'n'):
                zwol = miej_cr_date()
                if (zwol == 0):
                    return 0
                zwol = date(int(zwol[0]), int(zwol[1]), int(zwol[2]))
                if(zwol < dane[7]):
                    print("Podano datę wcześniejszą niż data zatrudnienia")
                    zwol = ''
            else:
                print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
                zwol = ''

    try:
        cursor.callproc("update_miej_zwolnienie", (dane[0], dane[1], dane[2], dane[8], zwol))
    except:
        print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
        return 0
    else:
        print("udało się zwolnić daną osobę w tym miejscu pracy")
        return 1

def miej_main(cnx,notcommited):
    cursor = cnx.cursor()

    show = True
    while True:
        if (show == 1):
            budynek.printf()
            print("Co wybierasz?")

        help = input()
        if (help == '1' or help == 'read'):
            miej_read(cursor)
            show = 1
        elif (help == '2' or help == 'create'):
            pom = miej_create(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '3' or help == 'update'):
            pom = miej_update(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '4' or help == 'delete'):
            pom = miej_delete(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '5' or help == 'reollback'):
            cnx.rollback()
            notcommited = 0
            show = 1
        elif (help == '6' or help == 'commit'):
            cnx.commit()
            notcommited = 0
            show = 1
        elif ((help == '0' or help == 'exit')):
            cursor.close()
            return notcommited
        else:
            print("Proszę wybrać numer lub mapisać nazwę z listy")
            show = 0