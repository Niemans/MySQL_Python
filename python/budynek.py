#funkcje wykorzystywane przez inne pliki main
def printf():
    print("Możliwe opcje:\n"
          "1. Zobaczenie tabeli (read)\n"
          "2. Dodanie r3kordu (create)\n"
          "3. Zmienienie r3cordu (update)\n"
          "4. Usunięcie r3cordu (delete)\n"
          "5. zaniechanie wprowadzonych w sesji aktualizacji bazy danych (rollback)\n"
          "6. zaktualizowanie głównej bazy danych (commit)\n"
          "0. powrót do głównego menu (exit)")

#do czytania
def bud_read(cursor):
    cursor.execute("SELECT dzielnica "
                   "FROM budynek "
                   "GROUP BY dzielnica;")
    result = cursor.fetchall()
    for x in result:
        print("Budynki w dizelnicy "+ str(x[0]) +":")

        cursor.execute("SELECT NRB, ulica, kod_pocztowy, l_mieszkan, l_wolnych "
                       "FROM budynek "
                       f"WHERE dzielnica = '{x[0]}';")

        myresult = cursor.fetchall()
        length = [len("Numer"),len("Ulica")]
        for i in myresult:
            if (length[0] < len(str(i[0]))):
                length[0] = len(str(i[0]))
            if (length[1] < len(str(i[1]))):
                length[1] = len(str(i[1]))

        print("Numer"           + " " * (length[0] - len("Numer") + 2)+
              "Ulica"           + " " * (length[1] - len("Ulica") + 2)+
              "Kod pocztowy"    + " " * 2 +
              "Liczba mieszk."  + " " * 2 +
              "Wolne mieszk.")
        for i in myresult:
            print(str(i[0]) + " " * (length[0] - len(str(i[0]))+2)+
                  str(i[1]) + " " * (length[1] - len(str(i[1]))+2)+
                  str(i[2]) + " " * (len("Kod pocztowy")    - len(str(i[2])) + 2) +
                  str(i[3]) + " " * (len("Liczba mieszk.")  - len(str(i[3])) + 2) +
                  str(i[4]))

#do dodawania
def bud_search(cursor, column):
    r3cord=''
    while r3cord == '':
        r3cord = input()
        if(r3cord == 'exit'):
            return 1
        elif(r3cord != 'y' and r3cord != 'n'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit' (wyjście z funkcji tworzenia)")
            r3cord = ''
    kolumna = [[]]
    if (r3cord == 'y'):
        cursor.execute(f"SELECT {column} FROM budynek GROUP BY {column};")
        kolumna = cursor.fetchall()

        count = 0
        print("Lista:")
        for i in kolumna:
            count += 1
            print(str(count) + ". " + i[0])

        print("proszę podać numer lub dać 'n', by móc wprowadzić dowolny nowy:")
        while r3cord == 'y':
            r3cord = input()
            if (r3cord != 'n'):
                try:
                    r3cord = int(r3cord)
                except:
                    if (r3cord == 'exit'):
                        return 0
                    print("Proszę podać liczbę lub 'n'")
                    r3cord = 'y'
                else:
                    if (r3cord < 1 or r3cord > count):
                        print("Proszę podać liczbę z listy")
                        r3cord = 'y'
                    else:
                        r3cord = kolumna[r3cord - 1][0]

    if (r3cord == 'n'):
        while len(r3cord) < 2 or len(r3cord) > 50:
            r3cord = input("Proszę podać nazwę: ")
            if (r3cord == 'exit'):
                return 0
            elif (len(r3cord) < 2):
                print("Nie kojarzę czegoś takiego z mniej niż 2 zmakami...")
            elif (len(r3cord) > 50):
                print("Za długa nazwa (maks 50 znaków) i nie da się jej przechować w bazie.")
    return r3cord

def bud_no(cursor, dzielnica, ulica):
    nr = 0
    while nr == 0:
        nr = input()
        try:
            nr = int(nr)
        except:
            if(nr == 'exit'):
                return 0
            print("Proszę podać liczbę naturalną")
            nr = 0
        else:
            if(nr < 1 or nr > 65535):
                print("Proszę podać liczbę z przedziału od 1 do 65535.")
                nr = 0
            else:
                cursor.execute("SELECT NRB FROM budynek "
                               f"WHERE dzielnica = '{dzielnica}' "
                               f"AND ulica = '{ulica}' "
                               f"AND NRB = {nr};")
                check = cursor.fetchall()
                try:
                    if(nr == check[0][0]):
                        print("budynek już istnieje, proszę podać inny numer")
                        nr = 0
                except:
                    nr = nr

    return nr

def bud_code():
    poczta = ''
    while poczta == '':
        poczta = input()
        if (poczta == 'exit'):
            return 0
        elif(len(poczta) != 6):
            print("To powinno zawierać 6 znaków: 'XX-XXX', gdzie X to cyfry")
            poczta = ''
        elif(poczta.find('-') != 2):
            print("Trzecim znakiem musi być '-'")
            poczta = ''
        else:
            try:
                x = int(poczta[0])
                x = int(poczta[1])
                x = int(poczta[3])
                x = int(poczta[4])
                x = int(poczta[5])
            except:
                print("Któryś ze znaków poza '-' nie jest cyfrą. Proszę spóbować jeszcze raz:")
                poczta = ''
    return poczta

def bud_create(cursor):
    print("Czy nowy r3cord będzie w jednej z już stworzonych dzielnic? (y/n/exit)")
    dzielnica = bud_search(cursor,'dzielnica')
    if(dzielnica == 0):
        return 0
    print("Czy nowy r3cord będzie w jednej z już stworzonych ulic? (y/n/exit)")
    ulica = bud_search(cursor, 'ulica')
    if(ulica == 0):
        return 0
    print("Jaki numer ma mieć budynek?")
    numer = bud_no(cursor, dzielnica, ulica)
    if (numer == 0):
        return 0

    print("Proszę podać kod pocztowy, pod który jest przypisany budynek (kod pocztowy wygląda mniej więcej tak: 'XX-XXX')")
    kod_pocztowy = bud_code()
    if(kod_pocztowy == 0):
        return 0

    print("Ile będzie w budynku mieszkań do kupienia lub wynajęcia?")
    liczba = -1
    while liczba == -1:
        liczba = input()
        try:
            liczba = int(liczba)
        except:
            if(liczba == 'exit'):
                return 0
            print("Proszę podać liczbę całkowitą od 0 do 255")
            liczba = -1
        else:
            if(liczba < 0 or liczba > 255):
                print("Proszę podać liczbę całkowitą od 0 do 255")
                liczba = -1

    print("Czy dane nowego budynku mają wyglądać następująco (y/n):\n dzielnica:", dzielnica, " ulica:", ulica," numer budynku:", numer," kod pocztowy:", kod_pocztowy," liczba mieszkań:", liczba)
    while True:
        choice = input()
        if(choice == 'n' or choice == 'exit'):
            return 0
        elif(choice == 'y'):
            try:
                cursor.callproc("insert_bud",(dzielnica,ulica,numer, kod_pocztowy,liczba))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się dodać r3cord")
                return 1
        else:
            print("wybierz 'y' (yes), 'n' (no) lub 'exit'")

#do usuwania
def bud_del_dziel(cursor):
    r3cord = 'y'

    cursor.execute(f"SELECT dzielnica FROM budynek GROUP BY dzielnica;")
    kolumna = cursor.fetchall()

    count = 0
    print("Lista:")
    for i in kolumna:
        count += 1
        print(str(count) + ". " + i[0])

    print("proszę podać numer podany koło nazwy:")
    while r3cord == 'y':
        r3cord = input()
        if (r3cord == 'exit'):
            return 0

        try:
            r3cord = int(r3cord)
        except:
            print("Proszę podać liczbę")
            r3cord = 'y'
        else:
            if (r3cord < 1 or r3cord > count):
                print("Proszę podać liczbę z listy")
                r3cord = 'y'
            else:
                r3cord = kolumna[r3cord - 1][0]
    return r3cord

def bud_del_ul(cursor, dzielnica):
    r3cord = 'y'

    cursor.execute(f"SELECT ulica FROM budynek "
                   f"WHERE dzielnica = '{dzielnica}' "
                   f"GROUP BY ulica;")
    kolumna = cursor.fetchall()

    count = 0
    print("Lista:")
    for i in kolumna:
        count += 1
        print(str(count) + ". " + i[0])

    print("proszę podać numer podany koło nazwy:")
    while r3cord == 'y':
        r3cord = input()
        if (r3cord == 'exit'):
            return 0

        try:
            r3cord = int(r3cord)
        except:
            print("Proszę podać liczbę")
            r3cord = 'y'
        else:
            if (r3cord < 1 or r3cord > count):
                print("Proszę podać liczbę z listy")
                r3cord = 'y'
            else:
                r3cord = kolumna[r3cord - 1][0]
    return r3cord

def bud_del_no(cursor, dzielnica, ulica):
    r3cord = 'y'

    cursor.execute("SELECT NRB FROM budynek "
                   f"WHERE dzielnica = '{dzielnica}' "
                   f"AND ulica = '{ulica}';")
    kolumna = cursor.fetchall()

    count = 0
    print("Lista:")
    for i in kolumna:
        count += 1
        print(str(count) + ". " + str(i[0]))

    print("proszę podać numer podany koło nazwy:")
    while r3cord == 'y':
        r3cord = input()
        if (r3cord == 'exit'):
            return 0

        try:
            r3cord = int(r3cord)
        except:
            print("Proszę podać liczbę")
            r3cord = 'y'
        else:
            if (r3cord < 1 or r3cord > count):
                print("Proszę podać liczbę z listy")
                r3cord = 'y'
            else:
                r3cord = kolumna[r3cord - 1][0]
    return r3cord

def bud_delete(cursor):
    print("Wybór dzielnicy:")
    dzielnica = bud_del_dziel(cursor)
    if(dzielnica == 0):
        return 0
    print("Wybór ulicy:")
    ulica = bud_del_ul(cursor, dzielnica)
    if(ulica == 0):
        return 0
    print("Wybór numeru budynku:")
    numer = bud_del_no(cursor, dzielnica, ulica)
    if(numer == 0):
        return 0

    cursor.execute("SELECT kod_pocztowy, l_mieszkan, l_wolnych "
                   "FROM budynek "
                   f"WHERE dzielnica = '{dzielnica}' "
                   f"AND ulica = '{ulica}' "
                   f"AND NRB = {numer};")
    dane = cursor.fetchall()
    print("Czy na pewno chcesz usunąć na stałe r3cordy powiązane oraz sam r3cor budynku (y/n): ")
    print(dzielnica + ",", ulica, str(numer) + ", ", dane[0][0] + ";  mieszkania:", dane[0][1], "liczba zajętych mieszkań:", dane[0][1]-dane[0][2])

    while True:
        pom = input()
        if(pom == 'n' or pom == 'exit'):
            return 0
        elif(pom == 'y'):

            try:
                cursor.callproc("delete_bud", (dzielnica, ulica, numer))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się usunąć r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit':")

#do update'owania'
def bud_update(cursor):
    """Niemożliwa jest zmiana położenia budynku, więc możliwa jest tylko zmiana numeru budynku i kodu pocztowego"""
    print("Update konkretnego budynku nie jest zmianą miejsca mudynku,\n"
          "więc nie ma możliwości zmiany dzielnicy czy ulicy.\n"
          "Nie ma też ustalania liczby mieszkań, "
          "gdyż jest ona uzależniona od liczby mieszkań wprowadzonych do bazy danych.")
    print("Proszę wybrać dzielnicę budynku:")
    dzielnica = bud_del_dziel(cursor)
    if (dzielnica == 0):
        return 0
    print("Proszę wybrać ulicę budynku:")
    ulica = bud_del_ul(cursor, dzielnica)
    if (ulica == 0):
        return 0
    print("Proszę wybrać numer budynku:")
    numer = bud_del_no(cursor, dzielnica, ulica)
    if (numer == 0):
        return 0

    cursor.execute("SELECT kod_pocztowy, l_mieszkan, l_wolnych "
                   "FROM budynek "
                   f"WHERE dzielnica = '{dzielnica}' "
                   f"AND ulica = '{ulica}' "
                   f"AND NRB = {numer};")
    dane = cursor.fetchall()
    print("Dane budynku:")
    print(dzielnica + ", " + ulica + " " + str(numer) +";  " + dane[0][0] + "  liczba mieszkań: " +
          str(dane[0][1]) + ", liczba wolnych mieszkań:" + str(dane[0][2]))

    print("czy zostaje zmieniany numer budynku? (y/n)")
    numer2 = ''
    while numer2 == '':
        numer2 = input()
        if (numer2 == 'exit'):
            return 0
        elif (numer2 == 'y'):
            print("Jaki ma być nowy numer?")
            numer2 = bud_no(cursor, dzielnica, ulica)
            if (numer2 == 'exit'):
                return 0
        elif (numer2 != 'n'):
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")
            numer2 = ''
    if(numer2 == 'n'):
        numer2 = numer

    print("czy zostaje zmieniany kod pocztowy? (y/n)")
    kod = ''
    while kod == '':
        kod = input()
        if(kod == 'exit'):
            return 0
        elif(kod == 'y'):
            print("Jaki ma być nowy kod pocztowy?")
            kod = bud_code()
            if (numer2 == 'exit'):
                return 0
        elif(kod != 'n'):
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")
            kod = ''
    if(kod == 'n'):
        kod = dane[0][0]

    print("Nowe dane budynku:")
    print(dzielnica + ", " + ulica + " " + str(numer2) + ";  " + kod + "  liczba mieszkań: " +
          str(dane[0][1]) + ", liczba wolnych mieszkań:" + str(dane[0][2]))

    if(numer2 == numer and kod == dane[0][0]):
        print("NIc w tym r3cordzie nie zostaje mienione.")
        return 0

    print("Czy chcesz zmienić dane budynku? (y/n)")
    while True:
        pom = input()
        if(pom ==  'n' or pom == 'exit'):
            return 0
        elif(pom == 'y'):

            try:
                cursor.callproc("update_bud", (dzielnica, ulica, numer, numer2, kod))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji\n")
                return 0
            else:
                print("udało się edytować r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

#funkcja główna
def bud_main(cnx,notcommited):
    cursor = cnx.cursor()

    show = True
    while True:
        if (show == 1):
            printf()
        print("Co wybierasz?")

        help = input()
        if (help == '1' or help == 'read'):
            bud_read(cursor)
            show = 1
        elif (help == '2' or help == 'create'):
            pom = bud_create(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '3' or help == 'update'):
            pom = bud_update(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '4' or help == 'delete'):
            pom = bud_delete(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '5' or help == 'rollback'):
            cnx.rollback()
            notcommited = 0
            show = 0
        elif (help == '6' or help == 'commit'):
            cnx.commit()
            notcommited = 0
            show = 0
        elif ((help == '0' or help == 'exit')):
            cursor.close()
            return notcommited
        else:
            print("Proszę wybrać numer lub mapisać nazwę z listy")
            show = 0

