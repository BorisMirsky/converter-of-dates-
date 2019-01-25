#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Конвертер дат. Переводит текущую либо выбранную дату в формат французского
республиканского календаря.

Сделано в Linux, переносимость не проверял. Не тестировал.

Скачет размер окна, надо доделать!
"""



import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import datetime, calendar


# словарь сопоставлений: французские республиканские месяцы, декады, дни и 'санкюлотиды'. 
dict_month = {1:'Vendemiaire', 2:'Brumaire', 3:'Frimaire',
              4:'Nivose', 5:'Pluviose', 6:'Ventose',
              7:'Germinal', 8:'Floreal', 9:'Prairial',
              10:'Messidor', 11:'Thermidor', 12:'Fructidor'}    
dict_decade = {1:'I', 2:'II', 3:'III'}
dict_day = {1:'Primidi', 2:'Duodi', 3:'Tridi', 4:'Quartidi', 5:'Quintidi',
           6:'Sextidi', 7:'Septidi', 8:'Octidi', 9:'Nonidi', 10:'Décadi'}
dict_sancs = {1:'La Fête de la Vertu', 2:'La Fête du Génie',
             3:'La Fête du Travail', 4:'La Fête de le Opinion',
             5:'La Fête des Récompenses', 6:' La Fête de la Révolution'}

# текущая дата
a = datetime.date.today()   


# Класс  переводит дату по юлианскому календарю во фр. респ. календарь
class Fr_date():
   def __init__(self, y, m, d):
      self.y = y                      
      self.m = m                      
      self.d = d                      
     
   # индекс сегодняшней даты
   def get_index(self, y, m, d):
      x = datetime.date(y, m, d)
      i = x.timetuple().tm_yday
      return i                           

   # Вычисление индекса дня Осеннего Равноденствия (далее ОР) - фр.респ. Нового года
   # В високосный и следующий годы ОР приходится на  22.09
   def eq(self, y):                                    # 'eq' сокращённо от 'equinox'
      if calendar.isleap(self.y) == True:
         d_ = datetime.date(self.y, 9, 22)             # в високосный год ...
         i1 = d_.timetuple().tm_yday
         return i1
      elif calendar.isleap(self.y) == True:
         d_ = datetime.date(self.y + 1, 9, 22)         # ... и следующий год ОР приходится на 22.09 ...
         i1 = d_.timetuple().tm_yday
         return i1
      else:                                    
         d_ = datetime.date(self.y, 9, 23)             # ... в два других года на 23.09    
         i1 = d_.timetuple().tm_yday
         return i1

   # Получение индекса дня по фр. календарю
   def fr_index(self):
      w = self.y - 1
      if self.get_index(self.y, self.m, self.d) >= self.eq(self.y):                       # если день после ОР
         z = self.get_index(self.y, self.m, self.d) - self.eq(self.y) + 1
         return z
      else:                                                                               # если день до ОР
        z = self.get_index(self.y, self.m, self.d) + self.get_index(w, 12, 31) - self.eq(w)
        return z

   # Получение всех параметров дня по фр. календарю
   def fr_date(self):
      fr_year = self.y - 1792 + 1
      fr_i = int(self.fr_index())
      if fr_i > 359:                     # Т.н. 'cанкюлотиды', спецю дни в конце года. В високосный год их 6, в другие 5.
         sanc = fr_i - 359
         return('%d год, санкюлотиды %d день %s' % (fr_year, sanc, dict_sancs[sanc]))
      else:
         fr_month = (fr_i // 30) + 1
         fr_dec = ((fr_i % 30) // 10) + 1
         if fr_i % 10 == 0:
            fr_day = 10
         else:
            fr_day = str(fr_i)[-1]
         fr_day = int(fr_day)
         return('%d год Республики, %s месяц, %s декада, %s день' %
                (fr_year, dict_month[fr_month], dict_decade[fr_dec], dict_day[fr_day]))
      

# Класс строит виджет
class Example(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        grid = QGridLayout()
        grid.setSpacing(10)        
        grid.addWidget(self.FirstGroup(), 1, 0)
        grid.addWidget(self.SecondGroup(), 2, 0, 6, 1)    
        self.setLayout(grid)
        self.setGeometry(100, 100, 400, 100)
        self.setWindowTitle('Vive la République!')
        self.q = Fr_date(a.year, a.month, a.day)              

    def FirstGroup(self):
        groupBox = QGroupBox("Конвертировать текущую дату")
        lbl1 = QLabel('Сегодня')
        today_ = QLineEdit()
        today_.setText(a.strftime("%d %B %Y")) 
        today_.setReadOnly(True)
        btn1 = QPushButton('allez')
        btn1.clicked.connect(self.on_clicked_btn1)
        global today_fr                                      
        today_fr = QLabel('   ') 
        hbox = QHBoxLayout()
        hbox.addWidget(lbl1)
        hbox.addWidget(today_)
        hbox.addWidget(btn1)
        hbox.addWidget(today_fr)
        hbox.addStretch(1)          
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        groupBox.setLayout(vbox)
        return groupBox

    def on_clicked_btn1(self):
        self.q = Fr_date(a.year, a.month, a.day)
        today_fr.setText(self.q.fr_date())                     

    def SecondGroup(self):    
        groupBox = QGroupBox("Выбрать и конвертировать дату с 22.9.1792 по текущий день")
        lbl2 = QLabel('Выбрать дату')
        global date_edit
        date_edit = QDateEdit(a)                                            
        date_edit.setDisplayFormat("yyyy-MM-dd")
        date_edit.setDateRange(QDate(1792, 9, 22), QDate(a))                 
        btn2 = QPushButton('allez')                                         
        btn2.clicked.connect(self.on_clicked_btn2) 
        global get_date
        get_date = QLabel('  ')                                              
        hbox = QHBoxLayout()
        hbox.addWidget(lbl2)
        hbox.addWidget(date_edit)
        hbox.addWidget(btn2)
        hbox.addWidget(get_date)
        hbox.addStretch(1)              
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)   
        groupBox.setLayout(vbox)
        return groupBox

    def on_clicked_btn2(self):
       self.q = Fr_date(int(date_edit.date().year()), int(date_edit.date().month()), int(date_edit.date().day())) 
       get_date.setText(self.q.fr_date())

     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
