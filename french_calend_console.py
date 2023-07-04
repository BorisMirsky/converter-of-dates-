# Консольная версия


import datetime, calendar


# словарь сопоставлений: французские республиканские (революционные) месяцы, декады, дни и 'санкюлотиды'
dict_month = {1:'Vendemiaire', 2:'Brumaire', 3:'Frimaire',
              4:'Nivose', 5:'Pluviose', 6:'Ventose',
              7:'Germinal', 8:'Floreal', 9:'Prairial',
              10:'Messidor', 11:'Thermidor', 12:'Fructidor'}

# декады вместо недель
dict_decade = {1:'I', 2:'II', 3:'III'}

# свои названия дней
dict_day = {1:'Primidi', 2:'Duodi', 3:'Tridi', 4:'Quartidi', 5:'Quintidi',
           6:'Sextidi', 7:'Septidi', 8:'Octidi', 9:'Nonidi', 10:'Décadi'}

# специальные дни 'санкюлотиды'
dict_sancs = {1:'La Fête de la Vertu', 2:'La Fête du Génie',
             3:'La Fête du Travail', 4:'La Fête de le Opinion',
             5:'La Fête des Récompenses', 6:' La Fête de la Révolution'}


# Класс  переводит дату по текущему (григорианскому) календарю во французский революционный (республиканский)
class Fr_date():
   def __init__(self, y, m, d):
      self.y = y
      self.m = m
      self.d = d


   # индекс сегодняшней даты
   def get_index(self, y, m, d):
      today = datetime.date(y, m, d)
      today_ind = today.timetuple().tm_yday
      return today_ind


   # Вычисление индекса дня Осеннего Равноденствия (далее ОР) - фр.респ. Нового года
   # В високосный и следующий годы ОР приходится на  22.09
   def eq(self, y):                                    # 'eq' сокращённо от 'equinox'
      eq_day = None
      if calendar.isleap(y) == True:
         eq_day = datetime.date(y, 9, 22)             # в високосный год ...
      elif calendar.isleap(y - 1) == True:
         eq_day = datetime.date(y, 9, 22)             # ... и следующий год ОР приходится на 22.09 ...
      else:
         eq_day = datetime.date(y, 9, 23)             # ... в два других года на 23.09
      return eq_day.timetuple().tm_yday


   # Получение индекса дня по фр. календарю
   def fr_index(self):
      pred_y = self.y - 1
      if self.get_index(self.y, self.m, self.d) >= self.eq(self.y):            # если день после ОР
         day_ind = self.get_index(self.y, self.m, self.d) - self.eq(self.y) + 1
      else:                                                                    # если день до ОР
         day_ind = self.get_index(self.y, self.m, self.d) + self.get_index(pred_y, 12, 31) - self.eq(pred_y)
      return day_ind


   # Получение всех параметров дня по фр. календарю
   def fr_date(self):
      fr_year = self.y - 1792 + 1
      fr_ind = int(self.fr_index())
      if fr_ind > 359:         # 'Cанкюлотиды' - cпец. дни в конце года. В високосный год их 6, в другие 5.
         sanc = fr_ind - 359
         return('%d год, санкюлотиды %d день %s' % (fr_year, sanc, dict_sancs[sanc]))
      else:
         fr_month = (fr_ind // 30) + 1
         fr_dec = ((fr_ind % 30) // 10) + 1
         if fr_ind % 10 == 0:
            fr_day = 10
         else:
            fr_day = str(fr_ind)[-1]
         fr_day = int(fr_day)
         return('Сегодня по французскому революционному календарю: \n %d год Республики, %s месяц, %s декада, %s день' %
                (fr_year, dict_month[fr_month], dict_decade[fr_dec], dict_day[fr_day]))




# aujourd'hui == сегодня
aujourdhui_arg = datetime.datetime.today().strftime('%Y-%m-%d').split('-')


# форматирование 'сегодня'
def aujourdhui_func(aujourdhui):
    res = '%s год, %s месяц, %s день' % (aujourdhui[0], aujourdhui[1], aujourdhui[2])
    print('Сегодня по григорианскому календарю: \n',res)


# 'сегодня' во фр. рев. кал.
instance = Fr_date(int(aujourdhui_arg[0]), int(aujourdhui_arg[1]), int(aujourdhui_arg[2]))


#вывод двух 'сегодня' - обычного и 'французского революционного'
aujourdhui_func(aujourdhui_arg)
print('')
print(instance.fr_date())



