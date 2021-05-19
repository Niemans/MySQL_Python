import budynek
import osoba
import zawod

#do wyświetlania
def prac_read(cursor):
    cursor.execute("SELECT zawod.nazwa, pracownik.Imie, pracownik.Nazwisko, pracownik.Nazwisko2, pracownik.placa "
                   "FROM pracownik "
                   "INNER JOIN zawod ON pracownik.IDZ = zawod.IDZ;")
    pracownik = cursor.fetchall()

    length = [len("Zawód"), len("Imie"), len("Nazwisko"), len("Płaca")]
    for i in pracownik:
        if (i[1] is None):
            help = 0
        else:
            help = 1

        if (length[0] < len(str(i[0]))):
            length[0] = len(str(i[0]))
        if (length[1] < len(str(i[1]))):
            length[1] = len(str(i[1]))
        if (length[2] < len(str(i[2]) + '-' * help + str(i[3]) * help)):
            length[2] = len(str(i[2]) + '-' * help + str(i[3]) * help)
        if (length[3] < len(str(i[4]))):
            length[3] = len(str(i[4]))

    print(" " * 7 +
          "Zawód"           + " " * (length[0] - len("Zawód") + 2) +
          "Imię"            + " " * (length[1] - len("Imię") + 2) +
          "Nazwisko"        + " " * (length[2] - len("Nazwisko") + 2) +
          "Płaca")

    count = 0
    for i in pracownik:
        count += 1
        if (i[3] is None):
            help = 0
        else:
            help = 1

        print(str(count)+ "." + " " * (6 - len(str(count))) +
              str(i[0]) + " " * (length[0] - len(str(i[0])) + 2) +
              str(i[1]) + " " * (length[1] - len(str(i[1])) + 2) +
              str(i[2]) + "-" * help + str(i[3]) * help + " " * (length[2] - len(str(i[2]) + '-' * help + str(i[3]) * help) + 2) +
              str(i[4]))

#do tworzenia
def prac_cr_check(cursor, im, naz, naz2, IDZ, zarobek):
    cursor.execute("SELECT IDP "
                   "FROM pracownik "
                   f"WHERE imie = '{im}' AND nazwisko = '{naz}' "
                   f"AND nazwisko2 = '{naz2}' AND IDZ = {IDZ} "
                   f"AND placa = {zarobek};")
    dane = cursor.fetchall()
    if(dane is None):
        return 0
    return 1

def prac_cr_zar(min, maks):
    while True:
        zarobek = input()
        if (zarobek == 'exit'):
            return 0
        try:
            zarobek = round(float(zarobek),2)
        except:
            print("Proszę podać liczbę")
        else:
            if(zarobek < float(min) or zarobek > float(maks)):
                print("Proszę podać zarobek między granicami")
            else:
                return zarobek

def prac_create(cursor):
    print("Proszę podać imię pracownika")
    imie = osoba.os_cr_im_naz()
    if (imie == 0):
        return 0
    print("Proszę podać nazwisko pracownika")
    naz = osoba.os_cr_im_naz()
    if (naz == 0):
        return 0

    print("czy dana osoba ma drugie nazwisko? (y/n)")
    naz2 = ''
    while naz2 == '':
        naz2 = input()
        if (naz2 == 'exit'):
            return 0
        elif (naz2 == 'y'):
            print("Proszę podać drugie nazwisko osoby")
            naz2 = osoba.os_cr_im_naz()
            if (naz2 == 0):
                return 0
        elif (naz2 != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            naz2 = ''
    help = 1
    if (naz2 == 'n'):
        help = 0

    pom = zawod.zaw_search(cursor)
    zawod.zaw_read(cursor)
    print("Prosże wybrać jeden z zawodów:")

    praca = ''
    while praca == '':
        praca = input()
        if (praca == 'exit'):
            return 0
        try:
            praca = int(praca)
        except:
            print("Proszę podać numer przy zawodzie")
            praca = ''
        else:
            if(praca < 1 or praca > len(pom)):
                print("Proszę podać jeden z numerów przy zawodach")
                praca = ''
            else:
                praca = pom[praca-1]

    print("Jakie zarobki będzie mieć dany pracownik w każdej ze swych przyszłych prac?")
    print("Minimalne zarobki:", praca[1], " Maksymalne zarobki:", praca[2])

    zarobek = prac_cr_zar(praca[1], praca[2])

    print("Dane nowego pracownika:")
    print(imie, naz + ('-' + naz2) * help)
    print("Zawód:", praca[0], " Zarobek:", round(zarobek,2))

    print("czy na pewno chcesz stworzyć takiego pracownika? (y/n)")
    while True:
        pom = input()
        if (pom == 'n' or pom == 'exit'):
            return 0
        elif (pom == 'y'):

            try:
                cursor.callproc("insert_prac", (imie, naz, naz2, round(zarobek, 2), praca[3]))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się dodać r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

#do update'owania
def prac_up_info(cursor, nr):
    cursor.execute("SELECT zawod.nazwa, pracownik.Imie, pracownik.Nazwisko, pracownik.Nazwisko2, pracownik.placa, IDP, pracownik.IDZ "
                   "FROM pracownik "
                   "INNER JOIN zawod ON pracownik.IDZ = zawod.IDZ;")
    data = cursor.fetchall()
    if(nr > len(data) or nr < 1):
        return -1
    return data[nr-1]

def prac_update(cursor):

    prac_read(cursor)
    print("Proszę podać nr przy pracowniku, którego dane chciałbyś zmienić")
    dane = ''
    nr = ''
    while nr == '':
        nr = input()
        if(nr == 'exit'):
            return 0
        try:
            nr = int(nr)
        except:
            print("Proszę podać liczbę")
            nr = ''
        else:
            dane = prac_up_info(cursor, nr)
            if(dane == -1):
                print("Proszę wybrać numer z listy")
                nr = ''

    print("Czy zostaje zmienione imie? (y/n)")
    new_imie = ''
    while new_imie == '':
        new_imie = input()
        if (new_imie == 'exit'):
            return 0
        elif (new_imie == 'y'):
            print("Proszę podać więc nowe imię:")
            new_imie = osoba.os_cr_im_naz()
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
            print("Proszę podać więc nowe nazwisko:")
            new_naz = osoba.os_cr_im_naz()
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
            new_naz2 = osoba.os_cr_im_naz()
            if(new_naz2 == 0):
                return 0
        elif(new_naz2 != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            new_naz2 = ''

    print("Czy zostaje zmieniona praca? (y/n)")
    new_prac = ''
    while new_prac == '':
        new_prac = input()
        if (new_prac == 'exit'):
            return 0
        elif (new_prac != 'n' and new_prac != 'y'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            new_prac = ''

    if(new_prac == 'y'):
        pom = zawod.zaw_search(cursor)
        zawod.zaw_read(cursor)
        print("Prosże wybrać jeden z zawodów:")
        while new_prac == 'y':
            new_prac = input()
            if (new_prac == 'exit'):
                return 0
            try:
                new_prac = int(new_prac)
            except:
                print("Proszę podać numer przy zawodzie")
                new_prac = 'y'
            else:
                if (new_prac < 1 or new_prac > len(pom)):
                    print("Proszę podać jeden z numerów przy zawodach")
                    new_prac = 'y'
                else:
                    new_prac = pom[new_prac - 1]
    if(new_prac == 'n'):
        pom = zawod.zaw_search(cursor,dane[6])
        new_prac = [pom[0], pom[1], pom[2], pom[3]]

    pom = ''
    new_zarobki = 0
    if(new_prac[0] == 'n' or (dane[4] > new_prac[1] and dane[4] < new_prac[2])):
        print("Czy chcesz zmieniać płacę pracownika? (y/n)")
        while pom == '':
            pom = input()
            if(pom == 'exit'):
                return 0
            elif(pom == 'n'):
                new_zarobki = pom
            elif(pom != 'y'):
                print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
                pom = ''

    if(pom == 'y' or (dane[4] < new_prac[1] or dane[4] > new_prac[2])):
        print("Proszę podać nowe zarobki tego pracownika:")
        print("Minimalna płaca tego zawodu:", new_prac[1], " Maksymalna płaca:", new_prac[2])
        new_zarobki = prac_cr_zar(new_prac[1], new_prac[2])

    if(new_naz == 'n' and new_imie == 'n' and new_naz2 == 'n' and new_prac[0] == dane[0] and new_zarobki == 'n'):
        print("Żadna dana w r3cordzie tego pracownika nie zostaje zmieniona")
        return 0
    if(new_imie == 'n'): new_imie = dane[1]
    if(new_naz == 'n'): new_naz = dane[2]
    if(new_naz2 == 'n'): new_naz2 = dane[3]
    if(new_zarobki == 'n'): new_zarobki = dane[4]

    help = 1
    if(new_naz2 is None):
        help = 0
    help2 = 1
    if(dane[3] is None):
        help2 = 0

    print("Stare dane pracownika:")
    print(dane[1], dane[2] + help2 * '-' + help2 * str(dane [3]))
    print("Zawód:", dane[0], "Zarobki:", dane[4], end = '\n\n')

    print("Nowe dane pracownika:")
    print(new_imie, new_naz + '-' * help + str(new_naz2) * help)
    print("Zawód:", new_prac[0], "Zarobki:", new_zarobki, end = '\n\n')

    print("Czy chcesz zaktualizować te dane? (y/n)")
    while True:
        pom = input()
        if (pom == 'n' or pom == 'exit'):
            return 0
        elif (pom == 'y'):

            if(prac_cr_check(cursor,new_imie,new_naz,new_naz2,new_prac[3],new_zarobki) == 0):
                print("Jest już taki pracownik z dokładnie takimi samymi danymi")
                return 0

            if (new_naz2 is None):
                new_naz2 = 'n'

            try:
                cursor.callproc("update_prac", (dane[5], new_prac[3], new_imie, new_naz, new_naz2, new_zarobki))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się edytować r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

#do usuwania
def prac_delete(cursor):
    prac_read(cursor)
    print("Proszę podać nr przy pracowniku, którego dane chciałbyś zmienić")
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
            dane = prac_up_info(cursor, nr)
            if (dane == -1):
                print("Proszę wybrać numer z listy")
                nr = ''

    help = 1
    if(dane[3] is None):
        help = 0
    print("Dane pracownika do wyrzucenia:")
    print(dane[1], dane[2] + help * '-' + help * str(dane[3]))
    print("Zawód:", dane[0], "Zarobki:", dane[4], end = '\n\n')

    print("Czy na pewno chcesz usunąć dany r3ord? (y/x)")
    while True:
        pom = input()
        if (pom == 'n' or pom == 'exit'):
            return 0
        elif (pom == 'y'):

            try:
                cursor.callproc("delete_prac", (dane[5],))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się usunąć r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

def prac_main(cnx,notcommited):
    cursor = cnx.cursor()

    show = True
    while True:
        if (show == 1):
            budynek.printf()
            print("Co wybierasz?")

        help = input()
        if (help == '1' or help == 'read'):
            prac_read(cursor)
            show = 1
        elif (help == '2' or help == 'create'):
            pom = prac_create(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '3' or help == 'update'):
            pom = prac_update(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '4' or help == 'delete'):
            pom = prac_delete(cursor)
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