import budynek

#do pokazania
def zaw_search(cursor, IDZ = -1):
    if(IDZ == -1):
        cursor.execute("SELECT nazwa, min_placa, max_placa, IDZ "
                       "FROM zawod;")
        return cursor.fetchall()
    else:
        cursor.execute("SELECT nazwa, min_placa, max_placa, IDZ "
                       "FROM zawod "
                       f"WHERE IDZ = {IDZ};")
        dane = cursor.fetchall()
        return dane[0]

def zaw_read(cursor):
    zawod =  zaw_search(cursor)
    print("Zawody pracowników budynków:")
    length = [len("zawód"), len("min. płaca")]
    for i in zawod:

        if (length[0] < len(str(i[0]))):
            length[0] = len(str(i[0]))
        if (length[1] < len(str(i[1]))):
            length[1] = len(str(i[1]))

    print(" " * 7 +
          "Nazwa"        + " " * (length[0] - len("Nazwa") + 2) +
          "Min. płaca"   + " " * (length[1] - len("Min. płaca") + 2) +
          "Maks. płaca")
    count = 0
    for i in zawod:
        count += 1
        print(str(count)+ "." + " " * (6 - len(str(count))) +
              str(i[0]) + " " * (length[0] - len(str(i[0])) + 2) +
              str(i[1]) + " " * (length[1] - len(str(i[1])) + 2) +
              str(i[2]))

#do dodania
def zaw_cr_check(cursor, nazwa):

    cursor.execute("SELECT nazwa "
                   "FROM zawod "
                   f"WHERE nazwa = '{nazwa}';")
    check = cursor.fetchall()

    try:
        x = check[0][0]
    except:
        return 1
    else:
        return 0

def zaw_cr_nazwa():
    nazwa = ''
    while nazwa == '':
        nazwa = input()
        if(nazwa == 'exit'):
            return 0
        elif(len(nazwa) < 2):
            print("Jeden znak to troszkę za mało")
            nazwa = ''
        elif(len(nazwa) > 30):
            print("Maksymalna liczba znaków to 30")
            nazwa = ''
        else:
            return nazwa

def zaw_cr_min_max(min = 0):
    min_max = ''
    while min_max == '':
        min_max = input()
        if(min_max == 'exit'):
            return 0

        try:
            min_max = int(min_max)
        except:
            print("Proszę pisać same liczby")
            min_max = ''
        else:
            if(min_max < 0):
                print("Minimalna wartość to 0 (praca charytatywna)")
                min_max = ''
            elif(min_max > 8388607):
                print("Za duża liczba, nie mieści się w bazie")
                min_max = ''
            elif(min_max < min):
                print("Maksymalna płaca nie może być niższa od minimalnej")
                min_max = ''
            else:
                return min_max

def zaw_create(cursor):
    print("Proszę podać nazwę zawodu (maksymalnie 30 znaków)")
    nazwa = zaw_cr_nazwa()

    print("proszę podać minimalną płacę za ten zawód (maksymalnie 8388607)")
    min = zaw_cr_min_max()

    print("proszę podać maksymalną płacę za ten zawód (maksymalnie 8388607)")
    max = zaw_cr_min_max(min)

    print("Dane nowego zawodu:")
    print("nazwa:",nazwa," min. płaca:",min," maks. płaca:",max)
    print("czy chcesz dodać taki r3cord do bazy? (y/n)")
    while True:
        pom = input()
        if(pom == 'n' or pom == 'exit'):
            return 0
        elif(pom == 'y'):
            if(zaw_cr_check(cursor,nazwa) == 0):
                print("zawód o takiej nazwie już istnieje")
                return 0

            try:
                cursor.callproc("insert_zaw", (nazwa, min, max))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się dodać r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

#do update'owania
def zaw_update(cursor):
    zaw_read(cursor)
    dane = zaw_search(cursor)

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
            if (nr < 1 or nr > len(dane)):
                print("Proszę wybrać numer z listy")
                nr = ''
            else:
                dane = dane[nr-1]

    print("Czy chcesz zmienić nazwę? (y/n)")
    nazwa = ''
    while nazwa == '':
        nazwa = input()
        if (nazwa == 'exit'):
            return 0
        elif (nazwa != 'n' and nazwa != 'y'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            nazwa = ''
    if (nazwa == 'y'):
        print("Proszę więc podać  nowąnazwę:")
        nazwa = zaw_cr_nazwa()

    print("Czy chcesz zmienić wartość minimalnej płacy? (y/n)")
    min = ''
    while min == '':
        min = input()
        if (min == 'exit'):
            return 0
        elif (min != 'n' and min != 'y'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            min = ''
    if (min == 'y'):
        print("Proszę więc podać nową wartość minimalną:")
        min = zaw_cr_min_max()

    print("Czy chcesz zmienić wartość maksymalnej płacy? (y/n)")
    max = ''
    while max == '':
        max = input()
        if (max == 'exit'):
            return 0
        elif (max != 'n' and max != 'y'):
            print("Proszę podać 'y' (yes), 'n' (no) lub 'exit'")
            max = ''
    if (max == 'y'):
        print("Proszę więc podać nową wartość maksymalną:")
        max = zaw_cr_min_max(min)

    if(nazwa == 'n'): nazwa = dane[0]
    if(min == 'n'): min = dane[1]
    if(max == 'n'): max = dane[2]
    if(nazwa == dane[0] and min == dane[1] and max == dane[2]):
        print("Nic się w tym r3cordzie nie zmieniło")
        return 0

    print("Stare dane:",dane[0],"minmimalna płaca:",dane[1]," maksymalna płaca:",dane[2])
    print("nowe dane:" ,nazwa,"minmimalna płaca:",min," maksymalna płaca:",max)

    print("Czy chcesz zaktualizować te dane? (y/n)")
    while True:
        pom = input()
        if (pom == 'n' or pom == 'exit'):
            return 0
        elif (pom == 'y'):
            if (zaw_cr_check(cursor, nazwa) == 0):
                print("zawód o takiej nazwie już istnieje")
                return 0

            try:
                cursor.callproc("update_zaw", (nazwa, min, max, dane[3]))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się edytować r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")


#do usuwania
def zaw_delete(cursor):
    zaw_read(cursor)
    dane = zaw_search(cursor)

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
            if (nr < 1 or nr > len(dane)):
                print("Proszę wybrać numer z listy")
                nr = ''
            else:
                dane = dane[nr - 1]

    print("Dane:", dane[0], "minmimalna płaca:", dane[1], " maksymalna płaca:", dane[2])

    print("Czy chcesz usunąć ten r3cord? (y/n)")
    while True:
        pom = input()
        if (pom == 'n' or pom == 'exit'):
            return 0
        elif (pom == 'y'):

            try:
                cursor.callproc("delete_zaw", (dane[3],))
            except:
                print("Najprawdopodobniej nie masz uprawnień do wykonywania tej operacji")
                return 0
            else:
                print("udało się usunąć r3cord")
                return 1
        else:
            print("Proszę wybrać 'y' (yes) lub 'n' (no), lub 'exit'")

def zaw_main(cnx, notcommited):
    cursor = cnx.cursor()

    show = True
    while True:
        if (show == 1):
            budynek.printf()
            print("Co wybierasz?")

        help = input()
        if (help == '1' or help == 'read'):
            zaw_read(cursor)
            show = 1
        elif (help == '2' or help == 'create'):
            pom = zaw_create(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '3' or help == 'update'):
            pom = zaw_update(cursor)
            if (notcommited == 0 and pom == 1):
                notcommited = pom
            show = 1
        elif (help == '4' or help == 'delete'):
            pom = zaw_delete(cursor)
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