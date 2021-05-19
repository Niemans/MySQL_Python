import budynek
import mieszkanie

#do wypisywania
def os_len(cursor, ulica_nr):
    length = [len("Imię"),len("Nazwisko")]
    for y in ulica_nr:
        cursor.execute("SELECT osoba.nazwisko, osoba.nazwisko2, imie "
                       "FROM osoba;")
        osoba = cursor.fetchall()

        for i in osoba:
            if (length[0] < len(str(i[2]))):
                length[0] = len(str(i[2]))

        for i in osoba:
            if (i[1] is None):
                help = 0
            else:
                help = 1

            if (length[1] < len(str(i[0]) + '-' * help + help * str(i[1]))):
                length[1] = len(str(i[0]) + '-' * help + help * str(i[1]))

    return length

def os_print(cursor, ulica_nr, length, dzielnica):
    for y in ulica_nr:
        print("\t W budynku " + str(y[1]) + " " + str(y[0]) + ":")

        cursor.execute("SELECT osoba.imie, osoba.nazwisko, osoba.nazwisko2, osoba.telefon, mieszkanie.NRM, osoba.owner "
                       "FROM osoba "
                       "INNER JOIN mieszkanie ON mieszkanie.IDM = osoba.IDM "
                       f"WHERE mieszkanie.NRB = {y[0]} "
                       f"AND mieszkanie.ulica = '{y[1]}' "
                       f"AND mieszkanie.dzielnica = '{dzielnica}' "
                       "ORDER BY mieszkanie.NRM, osoba.owner DESC;")
        osoba = cursor.fetchall()

        print("\t\t" +
              "Imię" + " " * (length[0] - len("Imię") + 2) +
              "Nazwisko" + " " * (length[1] - len("Nazwisko") + 2) +
              "telefon" + " " * 4 +
              "Nr mieszkania" + " " * 2 +
              "Czy właściciel")

        for i in osoba:
            if (i[2] is None):
                help = 0
            else:
                help = 1

            print("\t\t" +
                  str(i[0]) + " " * (length[0] - len(str(i[0])) + 2) +
                  str(i[1]) + "-" * help + str(i[2]) * help + " " * (length[1] - len(str(i[1]) + '-' * help + str(i[2]) * help) + 2) +
                  str(i[3]) + " " * 2 +
                  str(i[4]) + " " * (len("Nr mieszkania") - len(str(i[4])) + 2) +
                  str(i[5]))

def os_read(cursor):
    cursor.execute("SELECT dzielnica "
                   "FROM budynek "
                   "GROUP BY dzielnica;")
    dzielnica = cursor.fetchall()
    for x in dzielnica:
        print("Osoby w dzielnicy " + str(x[0]) + ":")

        cursor.execute("SELECT NRB, ulica "
                       "FROM mieszkanie "
                       f"WHERE dzielnica = '{x[0]}' "
                       "AND liczba_rezydentow <> 0 "
                       "GROUP BY NRB, ulica;")
        ulica_nr = cursor.fetchall()

        length = os_len(cursor, ulica_nr)
        os_print(cursor, ulica_nr, length, x[0])

#do tworzenia
def os_cr_im_naz():
    while True:
        r3cord = input()
        if(r3cord == 'exit'):
            return 0
        elif(r3cord.isalpha() != True):
            print("Proszę wpisać same litery")
        elif(len(r3cord) > 30):
            print("Maksymalna liczba liter to 30")
        else:
            return r3cord

def os_cr_tel():
    while True:
        tel = input()
        if(tel == 'exit'):
            return 0
        elif(tel.isdigit() != True):
            print("Proszę wpisać same cyfry (bez odnościka krajowego)")
        elif(len(tel) != 9):
            print("Proszę podać dokładnie 9 cyfr")
        else:
            return tel

def os_cr_check(cursor,IDM,imie, naz, naz2):
    if(naz2 == 'n'):
        cursor.execute("SELECT IDO "
                       "FROM osoba "
                       f"WHERE IDM = {IDM} "
                       f"AND imie = '{imie}' "
                       f"AND nazwisko = '{naz}' "
                       f"AND nazwisko2 IS NULL;")
    else:
        cursor.execute("SELECT IDO "
                       "FROM osoba "
                       f"WHERE IDM = {IDM} "
                       f"AND imie = '{imie}' "
                       f"AND nazwisko = '{naz}' "
                       f"AND nazwisko2 = '{naz2}';")

    check = cursor.fetchall()
    try:
        x = check[0][0]
    except:
        return 1
    else:
        print("Taka osoba już istnieje w tym mieszkaniu")
        return 0

def os_create(cursor):
    print("W którym budynku nowa osoba ma mieszkać?")
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
    dane = mieszkanie.miesz_up_dane(cursor,dzielnica,ulica,numer)
    if(dane == 0):
        return 0

    print("Czy chcesz, by ta osoba była właścicielem mieszkania? (y/n)")
    owner = ''
    while owner == '':
        owner = input()
        if(owner == 'exit'):
            return 0
        elif(owner == 'y'):
            owner = 1
        elif(owner == 'n'):
            owner = 0
        else:
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            owner = ''

    print("Proszę podać imię osoby")
    imie = os_cr_im_naz()
    if (imie == 0):
        return 0
    print("Proszę podać nazwisko osoby")
    naz = os_cr_im_naz()
    if (naz == 0):
        return 0
    print("czy dana osoba ma drugie nazwisko? (y/n)")

    naz2 = ''
    while naz2 == '':
        naz2 = input()
        if(naz2 == 'exit'):
            return 0
        elif(naz2 == 'y'):
            print("Proszę podać drugie nazwisko osoby")
            naz2 = os_cr_im_naz()
            if (naz2 == 0):
                return 0
        elif(naz2 !='n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            naz2 = ''
    help = 1
    if(naz2 == 'n'):
        help = 0

    print("Proszę podać numer telefonu:")
    tel = os_cr_tel()
    if(tel == 0):
        return 0

    print("Dane nowej osoby:")
    print("Będzie w budynku:", dzielnica, ulica, numer)
    print("W mieszkaniu nr:",dane[0], " o metrażu:", dane[1], " i koszcie:", dane[2])
    print("A jej dane to:", imie, naz + '-'*help + naz2*help, tel)
    print("Osoba " + "nie "*(1-owner) + "będzie właściielem/właścicielką mieszkania\n")

    print("Czy chcesz stworzyć taką osobę? (y/n)")
    while True:
        pom = input()
        if(pom == 'exit' or pom == 'n'):
            return 0
        elif(pom == 'y'):
            pom = os_cr_check(cursor, dane[5], imie, naz, naz2)
            if(pom == 0):
                return 0
            else:
                try:
                    cursor.callproc("insert_os", (dane[5], imie, naz, naz2, tel, owner))
                except:
                    print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                    return 0
                else:
                    print("udało się dodać r3cord")
                    return 1
        else:
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")

#do update'owanie
def os_up_dane(cursor, IDM):
    cursor.execute("SELECT imie, nazwisko, nazwisko2, telefon, owner, IDO "
                   "FROM osoba "
                   f"WHERE IDM = {IDM} "
                   "ORDER BY imie;")
    dane = cursor.fetchall()

    try:
        x = dane[0][0]
    except:
        print("Nie ma osób w tym mieszkaniu")
        return 0
    else:
        length = [len("Imie"), len("Nazwisko"), 9]
        for i in dane:
            if(length[0] < len(i[0])):
                length[0] = len(i[0])

            if (i[2] is None):
                help = 0
            else:
                help = 1

            if (length[1] < len(str(i[1]) + help * '-' + help * str(i[2]))):
                length[1] = len(str(i[1]) + help * '-' + help * str(i[2]))

        print(" " * 5 +
              "Imię" + " " * (length[0] - len("Imię") + 2) +
              "Nazwisko" + " " * (length[1] - len("nazwisko") + 2) +
              "telefon" + " " * (length[2] - len("telefon") + 2) +
              "Czy właściciel")

        count = 0
        for i in dane:
            count += 1
            if (i[2] is None):
                help = 0
            else:
                help = 1


            print(str(count) + "." + " " * (4 -len(str(count))) +
                  str(i[0]) + " " * (length[0] - len(str(i[0])) + 2) +
                  str(i[1]) + "-" * help + str(i[2]) * help + " " * (length[1] - len(str(i[1]) + '-' * help + str(i[2]) * help) + 2) +
                  str(i[3]) + " " * (length[2] - len(str(i[3])) + 2) +
                  str(i[4]))


        print("Proszę podać numer przy osobie")
        while True:
            pom = input()
            if (pom == 'exit'):
                return 0
            try:
                pom = int(pom)
            except:
                print("Proszę podać liczbę")
            else:
                if (pom < 1 or pom > count):
                    print("Proszę podać numer przy jednej z osób")
                else:
                    return dane[pom - 1]

def os_up_miesz(cursor):
    print("Trzeba wybrać, do kórego mieszkania chce się przenieść")
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
    dane = mieszkanie.miesz_up_dane(cursor, dzielnica, ulica, numer)
    if (dane == 0):
        return 0
    pom = list(dane)
    pom.append(dzielnica)
    pom.append(ulica)
    pom.append(numer)
    dane = tuple(pom)
    return dane

def os_up_search_dziel_ul_nr(cursor, IDM):
    cursor.execute("SELECT dzielnica, ulica, NRB "
                   "FROM mieszkanie "
                   f"WHERE NRM = {IDM};")
    dane = cursor.fetchall()
    return dane[0]

def os_update(cursor):
    #można zmieniać wszystko poza IDO
    print("Praktycznie każda dana może zostać u osoby zmieniona u osoby")
    print("Lecz najpierw trzeba wybrać osobę")
    print("W którym budynku nowa osoba ma mieszkać?")
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
    dane_miesz = mieszkanie.miesz_up_dane(cursor, dzielnica, ulica, numer)
    if (dane_miesz == 0):
        return 0
    dane_os = os_up_dane(cursor, dane_miesz[5])
    if (dane_os == 0):
        return 0

    print("Czy dana osoba będzie się przenosić do innego mieszkania? (y/n)")
    new_dane_miesz = ''
    while new_dane_miesz == '':
        new_dane_miesz = input()
        if (new_dane_miesz == 'exit'):
            return 0
        elif (new_dane_miesz == 'y'):
            new_dane_miesz = os_up_miesz(cursor)
            if(new_dane_miesz == 0):
                return 0
        elif(new_dane_miesz != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            new_dane_miesz = ''

    print("Czy zostaje zmienione imie? (y/n)")
    new_imie = ''
    while new_imie == '':
        new_imie = input()
        if (new_imie == 'exit'):
            return 0
        elif (new_imie == 'y'):
            print("Proszę podać nowe imię:")
            new_imie = os_cr_im_naz()
            if(new_imie == 0):
                return 0
        elif(new_imie != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            new_imie = ''

    print("Czy zostaje zmienione nazwisko? (y/n)")
    new_naz = ''
    while new_naz == '':
        new_naz = input()
        if (new_naz == 'exit'):
            return 0
        elif (new_naz == 'y'):
            print("Proszę podać nowe nazwisko:")
            new_naz = os_cr_im_naz()
            if(new_naz == 0):
                return 0
        elif(new_naz != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            new_naz = ''

    print("Czy zostaje zmienione lub dodane drugie nazwisko? (y/n)")
    new_naz2 = ''
    while new_naz2 == '':
        new_naz2 = input()
        if (new_naz2 == 'exit'):
            return 0
        elif (new_naz2 == 'y'):
            print("Proszę podać nowe drugie nazwisko:")
            new_naz2 = os_cr_im_naz()
            if(new_naz2 == 0):
                return 0
        elif(new_naz2 != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            new_naz2 = ''

    print("Czy zostaje zmieniony telefon? (y/n)")
    new_tel = ''
    while new_tel == '':
        new_tel = input()
        if (new_tel == 'exit'):
            return 0
        elif (new_tel == 'y'):
            print("Proszę podać nowy numer telefonu:")
            new_tel = os_cr_tel()
            if(new_tel == 0):
                return 0
        elif(new_tel != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            new_tel = ''

    print("Czy zmienić wartość przy tym, czy dana osoba jest właścicielem mieszkania? (y/n)")
    new_owner = ''
    while new_owner == '':
        new_owner = input()
        if (new_owner == 'exit'):
            return 0
        elif (new_owner == 'y'):
            if (dane_os[4] == 1):
                new_owner = 0
            else:
                new_owner = 1
        elif(new_owner != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            new_owner = ''

    if(new_dane_miesz == 'n' and new_imie == 'n' and new_naz == 'n' and new_naz2 == 'n' and new_tel == 'n' and new_owner == 'n'):
        print("Żadna dana w r3cordzie tej osoby nie zostaje zmieniona")
        return 0

    if(new_dane_miesz == 'n'): new_dane_miesz = dane_miesz
    if(new_imie == 'n'): new_imie = dane_os[0]
    if(new_naz == 'n'): new_naz = dane_os[1]
    if(new_naz2 == 'n'): new_naz2 = dane_os[2]
    if(new_tel == 'n'): new_tel = dane_os[3]
    if(new_owner == 'n'): new_owner = dane_os[4]

    help = 0
    if (dane_os[2] is None):
        help = 0
    else:
        help = 1
    print("Stare dane: budynek:", dzielnica, ulica, numer)
    print("mieszkanie nr:", dane_miesz[0])
    print("Dane osoby:", dane_os[0], dane_os[1] + "-" * help +
          str(dane_os[2]) * help, dane_os[3], "Czy jest właścicielem mieszkania: " + str(dane_os[4]), end = "\n\n")

    if (new_naz2 is None):
        help = 0
    else:
        help = 1
    if(new_dane_miesz != dane_miesz):
        print("Nowe dane: budynek:", new_dane_miesz[6], new_dane_miesz[7], new_dane_miesz[8])
    else:
        print("Nowe dane: budynek:", dzielnica, ulica, numer)
    print("mieszkanie nr:", new_dane_miesz[0])
    print("Dane osoby:", new_imie, new_naz + "-" * help +
          str(new_naz2) * help, new_tel, "Czy jest właścicielem mieszkania: " + str(new_owner), end = "\n\n")

    print("Czy chcesz zaktualizować te dane? (y/n)")
    while True:
        pom = input()
        if (pom == 'n' or pom == 'exit'):
            return 0
        elif (pom == 'y'):
            if(new_naz2 is None):
                new_naz2 = 'n'

            if(os_cr_check(cursor, new_dane_miesz[5], new_imie, new_naz, new_naz2) == 0):
                return 0

            try:
                cursor.callproc("update_os", (dane_os[5], new_dane_miesz[5], new_imie, new_naz, new_naz2,new_tel,new_owner))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się edytować r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

#do usuwania
def os_del_rezydenci(cursor, IDM):
    cursor.execute("UPDATE mieszkanie "
                   "SET liczba_rezydentow = liczba_rezydentow - 1 "
                   f"WHERE IDM = {IDM};")

    cursor.execute("SELECT liczba_rezydentow, dzielnica, ulica, NRB "
                   "FROM mieszkanie "
                   f"WHERE IDM = {IDM};")
    liczba = cursor.fetchall()

    if(liczba[0][0] == 0):
        cursor.execute("UPDATE budynek "
                       "SET l_wolnych = l_wolnych + 1 "
                       f"WHERE dzielnica = '{liczba[0][1]}' "
                       f"AND ulica = '{liczba[0][2]}' "
                       f"AND NRB = {liczba[0][3]};")

def os_delete(cursor):
    #zmiana wartości z mieszkaniach i budynkach
    print("Najpierw trzeba ustalić, o którą osobę w którym mieszkaniu chodzi.")
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
    dane_miesz = mieszkanie.miesz_up_dane(cursor, dzielnica, ulica, numer)
    if (dane_miesz == 0):
        return 0
    dane_os = os_up_dane(cursor, dane_miesz[5])
    if (dane_os == 0):
        return 0


    print("Dane osoby do usunięcia:")
    print("dane budynku:", dzielnica, ulica, numer)
    print("Numer mieszkania:",dane_miesz[0])
    help = 1
    if(dane_os[2] is None): help = 0
    print("Dane osoby:", dane_os[0], dane_os[1] + ("-" + str(dane_os[2])) * help, dane_os[3], "Czy właściciel : " + str(dane_os[4]))

    print("Czy na pewno chcesz usunąć dany r3ord? (y/n)")
    while True:
        pom = input()
        if(pom == 'y'):
            os_del_rezydenci(cursor,dane_miesz[5])

            try:
                cursor.callproc("delete_os", (dane_os[5],))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się usunąć r3cord")
                return 1
        if(pom == 'n' or pom == 'exit'):
            return 0
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

def os_main (cnx,notcommited):
    cursor = cnx.cursor()

    show = True
    while True:
        if (show == 1):
            budynek.printf()
            print("Co wybierasz?")


        help = input()
        if (help == '1' or help == 'read'):
            os_read(cursor)
            show = 1
        elif (help == '2' or help == 'create'):
            pom = os_create(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '3' or help == 'update'):
            pom = os_update(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '4' or help == 'delete'):
            pom = os_delete(cursor)
            if(notcommited == 0 and pom == 1):
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