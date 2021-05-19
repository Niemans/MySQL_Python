import budynek

#do pokazywania
def miesz_read(cursor):
    cursor.execute("SELECT dzielnica "
                   "FROM mieszkanie "
                   "GROUP BY dzielnica;")
    dzielnica = cursor.fetchall()
    for x in dzielnica:
        print("Mieszkania dzielnicy " + x[0] +":")

        cursor.execute("SELECT NRB, ulica, NRM, metraz, koszt, stan, liczba_rezydentow "
                       "FROM mieszkanie "
                       f"WHERE dzielnica = '{x[0]}' "
                       "ORDER BY NRB, ulica, NRM;")
        mieszkanie = cursor.fetchall()

        length = [len("Ulica"), len("koszt za m2"), len("stan")]
        for i in mieszkanie:
            if (length[0] < len(str(i[1]))):
                length[0] = len(str(i[1]))
            if (length[1] < len(str(i[4]))):
                length[1] = len(str(i[4]))
            if (length[2] < len(str(i[5]))):
                length[2] = len(str(i[5]))

        print("\t" +
              "Nr Budynku"      + " " * 2 +
              "Ulica"           + " " * (length[0] - len("Ulica") + 2) +
              "Nr mieszkania"   + " " * 2 +
              "Metraż"          + " " * 2 +
              "Koszt"           + " " * (length[1] - len("Koszt") + 2) +
              "Stan"            + " " * (length[2] - len("Stan")  + 2) +
              "Liczba rezyentów")

        for i in mieszkanie:
            print("\t" +
                  str(i[0]) + " " * (len("Nr Budynku")    - len(str(i[0])) + 2) +
                  str(i[1]) + " " * (length[0] - len(str(i[1])) + 2) +
                  str(i[2]) + " " * (len("Nr mieszkania") - len(str(i[2])) + 2) +
                  str(i[3]) + " " * (len("Metraż")        - len(str(i[3])) + 2) +
                  str(i[4]) + " " * (length[1] - len(str(i[4])) + 2) +
                  str(i[5]) + " " * (length[2] - len(str(i[5])) + 2) +
                  str(i[6]))

#do dodawania
def miesz_cr_metr_koszt(liczba):
    while True:
        metr_koszt = input()
        if(metr_koszt == 'exit'):
            return 0
        try:
            metr_koszt = int(metr_koszt)
        except:
            print("proszę podać liczbę całkowitą")
        else:
            if(metr_koszt < 1 or metr_koszt > liczba):
                print(f"Liczba nie musi byćw granicach o 1 do {liczba}")
            else:
                return metr_koszt

                                            #trzeba zmienić sposób podawania numeru mieszkania!!!!!!!!!!!!!!!!!!!!!!!

def miesz_cr_NRM(cursor, dzielnica, ulica, NRB):
    cursor.execute("SELECT MAX(NRM), dzielnica, ulica, NRB "
                   "FROM mieszkanie "
                   "GROUP BY Ulica, NRB "
                   f"HAVING dzielnica = '{dzielnica}' "
                   f"AND ulica = '{ulica}' "
                   f"AND NRB = {NRB};")
    dane = cursor.fetchall()
    return dane[0][0] + 1

def miesz_create(cursor):
    print("Wybór dzielnicy nowego mieszkania:")
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
    print("Jaki jest metraż tego mieszkania?")
    metraz = miesz_cr_metr_koszt(65535)
    if (metraz == 0):
        return 0
    print("Jaki jest koszt za zakup tego mieszkania?")
    koszt = miesz_cr_metr_koszt(16777215)
    if (koszt == 0):
        return 0
    nr_miesz = miesz_cr_NRM(cursor, dzielnica, ulica, numer)

    print("Dane nowego mieszkania:")
    print("Dzielnica:", dzielnica, " Ulica:", ulica, " Nr budynku:",numer)
    print("Nr mieszkania:", nr_miesz, " Metraż:", metraz, " koszt zakupu:", koszt)
    print("Mieszkanie na wstępie jest niezakupione i nie ma żadnych rezydentów")
    print("Czy chcesz dodać nowy r3cord? (y/n)")
    while True:
        pom = input()
        if (pom == 'n' or pom == 'exit'):
            return 0
        elif(pom == 'y'):
            try:
                cursor.callproc("insert_miesz",(dzielnica, ulica, numer, nr_miesz, metraz, koszt))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się dodać r3cord")
                return 1
        else:
            print("Proszę podać 'y' ()yes), 'n' (no) lub 'exit'")

#do updatowania
def miesz_up_dane(cursor, dzielnica, ulica, nrb):
    cursor.execute("SELECT NRM, metraz, koszt, stan, liczba_rezydentow, IDM "
                   "FROM mieszkanie "
                   f"WHERE dzielnica = '{dzielnica}' "
                   f"AND ulica = '{ulica}' "
                   f"AND NRB = {nrb} "
                   "ORDER BY NRM;")
    dane = cursor.fetchall()
    print("Lista mieszkań w budynku:",dzielnica + ", ", ulica, nrb)

    try:
        x=dane[0][0]
    except:
        print("Nie ma mieszkania w tym budynku")
    else:
        length = [5,6,8,8,3]

        print("Numer  Metraż  Koszt" +  " " * (length[2] - len("Koszt") + 2) +
              "Stan" + " " * (length[2] - len("Stan") + 2) + "Liczba mieszkańców")
        count = 0
        for i in dane:
            print(str(i[0]) + " " * (length[0] - len(str(i[0])) + 2) +
                  str(i[1]) + " " * (length[1] - len(str(i[1])) + 2) +
                  str(i[2]) + " " * (length[2] - len(str(i[2])) + 2) +
                  str(i[3]) + " " * (length[3] - len(str(i[3])) + 2) +
                  str(i[4]))
            count += 1

        print("Proszę podać numer mieszkania")
        while True:
            pom = input()
            if (pom == 'exit'):
                return 0
            try:
                pom = int(pom)
            except:
                print("Proszę podać liczbę")
            else:
                if(pom < 1 or pom > count):
                    print("Proszę podać numer jednego z mieszkań")
                else:
                    return dane[pom-1]

def miesz_update(cursor):
    """niemożliwa zmiana budynku (mieszkanie jest częścią budynku)
    i liczby rezydentów (ściśle powiązane z liczbą przypisanych osób),
    możliwa zmiana metraża, kosztu, stanu"""
    print("Możla zmieniać warości mieszkania, lecz nie można go przenosić.\n "
          "Nie można też zmieniać liczby mieszkańców ")
    print("Najpierw trzeba wybrać, które mieszknie którego budynku ma się zmienić.")
    print("Wybór dzielnicy mieszkania:")
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
    dane = miesz_up_dane(cursor,dzielnica,ulica,numer)
    if(dane == 0):
        return 0

    print("czy chcesz zmienić metraż mieszkania? (y/n)")
    metraz = ''
    while metraz == '':
        metraz = input()
        if(metraz == 'exit'):
            return 0
        elif(metraz == 'n'):
            metraz = dane[1]
        elif(metraz != 'y' and metraz != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
    if (metraz == 'y'):
        print("proszę więc podać nowy metraż:")
        metraz = miesz_cr_metr_koszt(65535)
        if (metraz == 0):
            return 0

    print("czy chcesz zmienić koszt zakupu mieszkania? (y/n)")
    koszt = ''
    while koszt == '':
        koszt = input()
        if(koszt == 'exit'):
            return 0
        elif(koszt == 'n'):
            koszt = dane[2]
        elif(koszt != 'y' and koszt != 'n'):
            print("Proszę podać 'y' ()yes), 'n' (no) lub 'exit'")
    if (koszt == 'y'):
        print("Proszę więc podać nowy koszt mieszkania:")
        koszt = miesz_cr_metr_koszt(16777215)
        if (koszt == 0):
            return 0

    print("czy chcesz zmienić stan zakupu mieszkania? (y/n)")
    stan = ''
    while stan == '':
        stan = input()
        if(stan == 'exit'):
            return 0
        elif(stan == 'n'):
            stan = dane[3]
        elif(stan != 'y'):
            print("Proszę podać 'y' ()yes), 'n' (no) lub 'exit'")
    if (stan == 'y'):
        if(dane[3] == 'puste'):
            print("Nie można zmienić stanu budynku, ponieważ jest on pusty, nikt go nie kupił bądź wynajął")
            stan = dane[3]
        else:
            choice = 0
            if(dane[3] == 'kupione'):
                choice = 1

            stan = "wynajęte" * (choice) + "kupione" * (1-choice)


    print("Nowe dane mieszkania to: ")
    print("dzielnica: " + dzielnica + "  ulica: " + ulica + "  nr budynku: " +str(numer))
    print("nr mieszkania: " + str(dane[0]) + "  metraż: " + str(metraz) + "  koszt zakupu: " + str(koszt))
    print("Stan: " + stan + "  liczba mieszkańców: " + str(dane[4]))

    if(metraz == dane[1] and koszt == dane[2] and  stan == dane[3]):
        print("NIc w tym r3cordzie nie zostaje mienione.")
        return 0

    print("czy na pewno chcesz dokonać zmian? (y/n)")
    while True:
        pom = input()
        if (pom == 'n' or pom == 'exit'):
            return 0
        elif (pom == 'y'):

            try:
                cursor.callproc("update_miesz", (dane[5], metraz, koszt, stan))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się edytować r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

#do usuwania
def miesz_delete(cursor):
    print("Najpierw trzeba wybrać, które mieszknie którego budynku ma zostać usunięte z listy.")
    print("Wybór dzielnicy mieszkania:")
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
    dane = miesz_up_dane(cursor, dzielnica, ulica, numer)
    if (dane == 0):
        return 0

    print("Dane mieszkania to: ")
    print("dzielnica: " + dzielnica + "  ulica: " + ulica + "  nr budynku: " + str(numer))
    print("nr mieszkania: " + str(dane[0]) + "  metraż: " + str(dane[1]) + "  koszt zakupu: " + str(dane[2]))
    print("Stan: " + dane[3] + "  liczba mieszkańców: " + str(dane[4]))

    print("czy na pewno chcesz usunąć r3cord? (y/n)")
    while True:
        pom = input()
        if (pom == 'n' or pom == 'exit'):
            return 0
        elif (pom == 'y'):

            try:
                cursor.callproc("delete_miesz", (dane[5],))
                cursor.callproc("update_bud_liczba", (dzielnica, ulica, numer, dane[4]))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się usunąć r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

def miesz_main(cnx,notcommited):
    cursor = cnx.cursor()

    show = True
    while True:
        if (show == 1):
            budynek.printf()
            print("Co wybierasz?")

        help = input()
        if (help == '1' or help == 'read'):
            miesz_read(cursor)
            show = 1
        elif (help == '2' or help == 'create'):
            pom = miesz_create(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '3' or help == 'update'):
            pom = miesz_update(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '4' or help == 'delete'):
            pom = miesz_delete(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '5' or help == 'rollback'):
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