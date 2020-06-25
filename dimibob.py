from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import untitled
import curses
import urllib.request, json 
import datetime
import os.path

def right () :
    ui.dateEdit.setDate(ui.dateEdit.date().addDays(1))

def left () :
    ui.dateEdit.setDate(ui.dateEdit.date().addDays(-1))


def changed() :
    ui.textBrowser.clear()
    display_bob(ui.dateEdit.date())

max_day = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

bob_data = {}
raw_data = {}
eng2kor = {'breakfast': '아침', 'lunch': '점심', 'dinner': '저녁'}

def init():
    if not os.path.isfile('tmp/bob.db'):
        f = open('tmp/bob.db', 'w')
        f.close()
    ui.textBrowser.clear()
    ui.dateEdit.setCalendarPopup(True)

def fetch_bob(month):
    with open('tmp/bob.db', 'r') as f:
        for tmp in f.readlines():
            date = int(tmp.split('%')[0])
            meal = {
                'breakfast': tmp.split('%')[1],
                'lunch': tmp.split('%')[2],
                'dinner': tmp.split('%')[3].replace('\n', ''),
            }
            # print(date, meal
            raw_data[date] = tmp.split('%', 1)[1]
            bob_data[date] = meal
    for i in range(20200000 + month * 100 + 1, 20200000 + month * 100+ max_day[month] + 1):
        if i not in bob_data:
            # print("https://api.dimigo.in/dimibobs/" + str(i) + '/')
            try:
                with urllib.request.urlopen("https://api.dimigo.in/dimibobs/" + str(i) + '/') as url:
                    bob_data[i] = json.loads(url.read().decode())
                    # print("fetch %d:" % i, bob_data[i])
            except:
                # print('failed to fetch %d' % i)
                break
    # print(bob_data)
    with open('tmp/bob.db', 'w') as f:
        for i in bob_data:
            f.write("%d%%%s%%%s%%%s\n" % (i, bob_data[i]['breakfast'], \
                            bob_data[i]['lunch'], bob_data[i]['dinner']))


def bob_time(ban, date):
    time = {
        'lunch': [47400, 47580, 47760, 47940, 48120, 48300],
        'dinner': [69300, 69480, 69660, 69840, 70020, 70200]
    }
    date2 = datetime.date(int(date.toString('yyyy')), int(date.toString('MM')), int(date.toString('dd')))
    w = date2.isocalendar()[1]
    d = date2.isocalendar()[2]

    # print('w', w, 'd', d)

    p = 0
    if w < 35:
        p = w - 22
        if d < 3:
            p -= 1
    else:
        p = w - 33
    p = p % 6
    # print('p', p)

    lunch_time = time['lunch'][(ban - p) % 6]
    dinner_time = time['dinner'][5 - (ban - p) % 6]
    if d == 3:
        dinner_time -= 1500

    return (datetime.timedelta(seconds=lunch_time),
            datetime.timedelta(seconds=dinner_time))

def display_bob(date):
    # print(date, type(date))

    #stdscr.addstr(0, 0, "Press ';' for help.", curses.color_pair(3))
    #stdscr.addstr(1, 0, "Press 'q' to quit.", curses.color_pair(3))
    #ui.textBrowser.setPlainText("Press ';' for help.")
    #ui.textBrowser.append("Press 'q' to quit.")

    #date_str = date.year * 10000 + date.month * 100 + date.day
    date_str = int(date.toString('yyyyMMdd'))
    #print(date_str)
    #stdscr.addstr(1, 30, '{}년 {:0>2}월 {:0>2}일'.format(date.year, date.month, date.day))
    ui.textBrowser.append("{}년 {:0>2}월 {:0>2}일".format(date.toString('yyyy'), date.toString('MM'), date.toString('dd')))
    
    if date_str in bob_data:
        col = -24
        for k in eng2kor:
            line = 3
            col += 25
            #stdscr.addstr(line, col, eng2kor[k] + ' ', curses.color_pair(1))
            ui.textBrowser.append(eng2kor[k] + ' ')
            time = bob_time(6, date)
            if k == 'lunch':
                #stdscr.addstr(line, col + 5, str(time[0]), curses.color_pair(1))
                ui.textBrowser.append(str(time[0]))
            elif k == 'dinner':
                #stdscr.addstr(line, col + 5, str(time[1]), curses.color_pair(1))
                ui.textBrowser.append(str(time[1]))
            for j in bob_data[date_str][k].split('/'):
                line += 1
                if line < 40:
                    #stdscr.addstr(line, col + 1, j + '\n')
                    ui.textBrowser.append(j + '\n')
    else:
        #stdscr.addstr(4, 28, '급식 정보가 없습니다')
        ui.textBrowser.append('급식 정보가 없습니다.')
    cursor = ui.textBrowser.textCursor()
    cursor.setPosition(0)
    ui.textBrowser.setTextCursor(cursor)

    #stdscr.move(0, 0)
    #stdscr.refresh()

# CLI Based Help Script Starting From Here :
"""
def display_help(stdscr):
    stdscr.clear()

    #stdscr.addstr(0, 0, "Press ';' for bob.", curses.color_pair(3))
    #stdscr.addstr(1, 0, "Press 'q' to quit.", curses.color_pair(3))
    ui.textBrowser.setPlainText("Press ';' for bob.")
    ui.textBrowser.append("Press 'q' to quit.")

    #stdscr.addstr(3, 1, "H - 1주 전으로 이동")
    #stdscr.addstr(4, 1, "h - 1일 전으로 이동")
    ui.textBrowser.append("H - Move to One week earlier.")
    ui.textBrowser.append("h - Move to One day earlier.")


    #stdscr.addstr(6, 1, "L - 1주 후로 이동")
    #stdscr.addstr(7, 1, "l - 1일 후로 이동")
    ui.textBrowser.append("L - Move to One week forward.")
    ui.textBrowser.append("l - Move to One day forward.")


    #stdscr.addstr(9, 1, "t - 오늘로 이동")
    ui.textBroser.append("t - Move to today.")
"""

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = untitled.Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.dateEdit.setDate(QDate.currentDate())
    ui.dateEdit.setMinimumDate(QDate(2000, 1, 1))
    ui.dateEdit.setMaximumDate(QDate(2050, 12, 31))
    ui.pushButton.clicked.connect(right)
    ui.pushButton_2.clicked.connect(left)
    ui.dateEdit.dateChanged.connect(changed)
    MainWindow.show()
    init()
    fetch_bob(6)
    now = QtCore.QDate.currentDate()
    display_bob(now)
    is_searching = False
    #curses.wrapper(main)
    sys.exit(app.exec_())

