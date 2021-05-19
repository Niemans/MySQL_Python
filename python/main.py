import mysql.connector
from mysql.connector import errorcode

import budynek
import pracownik
import zawod
import mieszkanie
import miejsce_pracy
import osoba


user = ''
password = ''
print("Witaj!")
print("Którego urzytkownika chciałyś urzyć?")
while user == '':
    user = input()
    if(user != 'adm' and user != 'user'):
        print("Nie ma takiego urzytkownika")
        user = ''
    else:
        print("Proszę podać hasło:")
        while password == '':
            password = input()
            if(password != 'asdf'):
                print("błędne hasło")
                password = ''

try:
    cnx = mysql.connector.connect(user = f"{user}", password = f"{password}", host = '127.0.0.1', database = 'dzielnica', autocommit = 0)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Brak dostępu, może wprowadzono złe hasło')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Brak danej bazy danych')
    else:
        print(err)
else:
    cnx._open_connection()
    cnx.start_transaction()
    cnx.autocommit = 0 #na wszelki wypadek

    show = True
    notcommited = 0
    while True:

        if(show == 1):
            print("Lista tabel:\n"
                  "1. budynek\n"
                  "2. pracownik\n"
                  "3. zawód\n"
                  "4. miejsce pracy\n"
                  "5. mieszkanie\n"
                  "6. osoba\n"
                  "7. rollback\n"
                  "8. commit\n"
                  "0. exit")
            print("Na której tabeli chcesz się skupić:")

        help = input()
        if  (help == '1' or help == 'budynek'):
            notcommited = budynek.bud_main(cnx,notcommited)
            show = 1
        elif (help == '2' or help == 'pracownik'):
            notcommited = pracownik.prac_main(cnx,notcommited)
            show = 1
        elif (help == '3' or help == 'zawód' or help == 'zawod'):
            notcommited = zawod.zaw_main(cnx,notcommited)
            show = 1
        elif (help == '4' or help == 'miejsce' or help == 'miejsce pracy'):
            notcommited = miejsce_pracy.miej_main(cnx,notcommited)
            show = 1
        elif (help == '5' or help == 'mieszkanie'):
            notcommited = mieszkanie.miesz_main(cnx,notcommited)
            show = 1
        elif (help == '6' or help == 'osoba'):
            notcommited = osoba.os_main(cnx,notcommited)
            show = 1
        elif (help == '7' or help == 'rollback'):
            cnx.rollback()
            notcommited = 0
            print("dokonano rollback")
            show = 0
        elif (help == '8' or help == 'commit'):
            cnx.commit()
            notcommited = 0
            print("dokonano commit")
            show = 0
        elif (help == '0' or help == 'exit'):
            if(notcommited == 1):
                print("Przed wyjściem proszę dokonać rollback (7) lub commit (8)")
                show = 0
            else:
                cnx.close()
                exit()
        else:
            print("Proszę wybrać numer lub mapisać nazwę z listy")
            show = 0