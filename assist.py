#Класс Ассистента
class Assistant:
    #Инициализирующий конструктор
    def __init__(self,numofpairs,name):
        self.pairs=[]
        self.numofpairs=numofpairs
        self.name=name.strip()
    #Метод, возвращающий пары, на которые нужно идти ассистенту
    def getPairs(self):
        return self.pairs
    def getNumOfPairs(self):
        return self.numofpairs
    def addPair(self,num):
        self.pairs.append(num)
        self.numofpairs=self.numofpairs-1
    def setNumOfPairs(self,num):
        self.numofpairs=num
    def getName(self):
        return self.name
    def removePair(self,num):
        self.pairs.pop(self.pairs.index(num))
#Класс Пары
class Pair:
    #Инициализирующий конструктор
    def __init__(self,numofstud,hourss,hoursf,info):
        self.students=[]
        self.numofstudents=numofstud
        self.start=hourss
        self.end=hoursf
        self.day=info
    #Метод, возвращающий студентов с этой пары
    def getStudents(self):
        return self.students
    #no comments
    def getNumOfStudents(self):
        return self.numofstudents
    def addStudent(self,num):
        self.students.append(num)
        self.numofstudents=self.numofstudents-1
    def setNumOfStudents(self,num):
        self.numofstudents=num
    #Метод, возвращающий информацию о паре
    def getHours(self):
        return self.start+'-'+self.end + ' on ' +self.day
    def removeStudent(self,num):
        self.students.pop(self.students.index(num))
#Тестовая дефолтная версия алгоритма
assistants_test=[]
assistants_test.append(Assistant(2,'Ivanov Sergey'))
assistants_test.append(Assistant(3,'Shamsutdinov Artemiy'))
pairs_test=[]
pairs_test.append(Pair(1,'12.10','13.30','2nd March'))
pairs_test.append(Pair(2,'13.40','15.00','2nd March'))
crossings_test=[(1,2),(1,1),(2,2),(2,1)]
#Проходимся по всем возможным сочетаниям пар и студентов, все совпадения заносим в соответствующие объекты классов Ассистента и Пары
for item in crossings_test:
    assistants_test[item[0]-1].addPair(item[1])
    pairs_test[item[1]-1].addStudent(item[0])
#Рабочий алгоритм.
for iterator_1 in range (len(pairs_test)):
    #Условие на то, что у нас переполнение пары (больше студентов, чем нужно)
    if pairs_test[iterator_1].getNumOfStudents()<0:
        #Список, хранящий для каждого студента из тех, кто может быть на паре, количество СВОБОДНЫХ пар у него
        rangeofpairs=[]
        for iterator_2 in pairs_test[iterator_1].getStudents():
            rangeofpairs.append(assistants_test[iterator_2-1].getNumOfPairs())
        rangeofpairs.sort()
        ind=0
        iterator_2 = 0
        #У нас появился список по рангу свободных пар. Убираем обрабатываемую пару у тех студентов, у кого свободных пар меньше всего (из списка)
        while pairs_test[iterator_1].getNumOfStudents()<0:
            #Нарыли ассистента, у которого столько же свободных пар, сколько у текущего элемента в списке свободных пар
            if assistants_test[iterator_2].getNumOfPairs()==rangeofpairs[ind]:
                    #Удалили у него пару
                    assistants_test[iterator_2].removePair(iterator_1+1)
                    assistants_test[iterator_2].setNumOfPairs(assistants_test[iterator_2].getNumOfPairs()+1)
                    pairs_test[iterator_1].setNumOfStudents(pairs_test[iterator_1].getNumOfStudents()+1)
                    pairs_test[iterator_1].removeStudent(iterator_2+1)
                    ind+=1
                    iterator_2+=1
            else:
                    iterator_2 += 1
#Вывод. Из каждой пары достаем информацию и список студентов, которые на ней работают
for iterator_1 in range (len(pairs_test)):
    print(pairs_test[iterator_1].getHours())
    for iterator_3 in pairs_test[iterator_1].getStudents():
        print(assistants_test[iterator_3-1].getName())
#Работа с данными. Спасибо Ерохиной за хороший файл (почти без ошибок)!
import pandas as pd
dataset=pd.read_excel('timetable.xlsx')
dataset[dataset['Дата ']!=None]
names_of_assistants=dataset.columns.values[8:]
print(dataset.shape)
dataset=dataset.drop(dataset.index[[72,73,74,75,76,77]])
#Удалили ненужные строки, начинаем клеить из данных столбец информации о паре
dataset['info']=dataset['Дата '].apply(lambda x: x.strftime('%Y-%m-%d'))+' '+dataset['День']+' '+dataset['Ауд']+' '+dataset['Преподаватель']+' '+dataset['Группа (подгруппа)']
del dataset['Дата '],dataset['День'],dataset['Ауд'],dataset['Преподаватель'],dataset['Группа (подгруппа)']
#Все столбцы с нужной информацией преобразовали в списки
beg=dataset['Начало'].tolist()
endings=dataset['Окончание'].tolist()
numofs=[int(x) for x in dataset['Число ассистентов'].tolist()]
infos=dataset['info'].tolist()
#Заталкиваем всю нужную информацию о парах в список пар
pairs_final=[]
for i in range(len(beg)):
    pairs_final.append(Pair(numofs[i],beg[i],endings[i],infos[i]))
del dataset['info'],dataset['Начало'],dataset['Окончание'],dataset['Число ассистентов']
#Собираем остальные данные в соответствующие списки
numofp=[]
assistants_final=[]
crossings_final=[]
available_pairs=[]
for item in names_of_assistants:
    #Заполнили пропуски
    dataset[item].fillna(value=0,inplace=True)
    #Для каждого студента нашли, сколько пар он может на себя взять. В нашем случае это все пары из таблицы Ерохиной.
    numofp.append(dataset[item].sum())
    #Выносим за алгоритм списки всех пар, на которые могут пойти студенты, в виде последовательности нулей и единиц
    massive=[float(x) for x in dataset[item].tolist()]
    available_pairs.append(massive)
for i in range (len(names_of_assistants)):
    assistants_final.append(Assistant(numofp[i],names_of_assistants[i]))
for i in range (len(available_pairs)):
    for j in range (len(available_pairs[i])):
        #Преобразуем эту последовательность в кортеж и отправляем в список сочетаний пар и студентов
        if available_pairs[i][j]==1:
            cross=(i+1,j+1)
            crossings_final.append(cross)
#Тот же алгоритм с доп. условиями прогнали по данным
for item in crossings_final:
    assistants_final[item[0]-1].addPair(item[1]-1)
    pairs_final[item[1]-1].addStudent(item[0]-1)
for i in range (len(pairs_final)):
    if pairs_final[i].getNumOfStudents()<0:
        rangeofpairs=[]
        for j in pairs_final[i].getStudents():
            rangeofpairs.append(assistants_final[j].getNumOfPairs())
        rangeofpairs.sort()
        ind=0
        t = 0
        while pairs_final[i].getNumOfStudents()<0 and t<len(assistants_final):
            if (assistants_final[t].getNumOfPairs()==rangeofpairs[ind]) and (i in assistants_final[t].getPairs()) and (t in pairs_final[i].getStudents()):
                    assistants_final[t].removePair(i)
                    assistants_final[t].setNumOfPairs(assistants_final[t].getNumOfPairs()+1)
                    pairs_final[i].setNumOfStudents(pairs_final[i].getNumOfStudents()+1)
                    pairs_final[i].removeStudent(t)
                    ind+=1
                    t+=1
            else:
                    t += 1
res={}
res["assists"] = []
#Радостно отправляем в словарь и в джейсон
for i in range (len(assistants_final)):
    assistant=assistants_final[i].getName()
    lessons=[]
    for t in assistants_final[i].getPairs():
        lessons.append(pairs_final[t].getHours())
    res["assists"].append({"assistant": assistant, "pairs": lessons})

import json
with open('data_file.json','w') as write_file:
    json.dump(res,write_file)
print('end')