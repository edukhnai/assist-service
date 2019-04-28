class Lesson:
    lesson_counter_ = 0

    def __init__(self, teacher, available_assistants, have_consultation, time, additional_info, is_deadline,
                 intersecting_lessons):
        self.id_ = Lesson.lesson_counter_
        Lesson.lesson_counter_ += 1
        self.teacher_ = teacher
        #self.teacher_ = Teacher('fake teacher', [], 'none', [])
        self.assistants_ = []
        self.available_assistants_ = available_assistants
        self.time_ = time
        self.additional_info_ = additional_info
        self.is_deadline_ = is_deadline
        self.intersecting_lessons_ = intersecting_lessons

class Teacher:
    teacher_counter_ = 0

    def __init__(self, name, lessons, info, prefering_assistants):
        self.id_ = Teacher.teacher_counter_
        Teacher.teacher_counter_ += 1
        self.name_ = name
        self.lessons_ = lessons
        self.info_ = info
        self.prefering_assistants_ = prefering_assistants


class Assistant:
    assistant_counter_ = 0

    def __init__(self, name, available_lessons, prefered_teachers):
        self.id_ = Assistant.assistant_counter_
        Assistant.assistant_counter_ += 1
        self.name_ = name
        self.lessons_ = []
        self.available_lessons_ = available_lessons
        self.score_ = 0
        self.potential_score_ = 0
        self.tasks_ = []
        self.prefered_teachers_ = prefered_teachers

class Task:
    task_counter_ = 0

    def __init__(self, name, additional_info, amount, score):
        self.id_ = Task.task_counter_
        Task.task_counter_ += 1
        self.name_ = name
        self.additional_info_ = additional_info
        self.amount_ = amount
        self.score_ = score
        # TODO assignations contains student, number of first and last task for him.
        self.assignations_ = []


class SchelduleManager:
    # def __init__(self, lessons=None, teachers=None, assistants=None, tasks=None, score_per_lesson=None, assistant_for_deadline=None,
    #              assistant_for_usual_lesson=None):
    #     self.lessons_ = lessons
    #     self.teachers_ = teachers
    #     self.assistants_ = assistants
    #     self.tasks_ = tasks
    #     self.score_per_lesson_ = score_per_lesson
    #     self.assistant_for_deadline_ = assistant_for_deadline
    #     self.assistant_for_usual_lesson_ = assistant_for_usual_lesson

    def __init__(self,open_file):
        self.lessons_ = []
        self.teachers_ = []
        self.assistants_ = []
        self.tasks_ = []
        self.score_per_lesson_ = 20
        self.assistant_for_deadline_ = 4
        self.assistant_for_usual_lesson_ = 2
        self.ParseData(open_file)

    def ParseData(self, open_file):
        import pandas as pd
        dataset = pd.read_excel(open_file,'Лист1')
        list_of_names_of_assistants = dataset.columns.values[9:]
        dataset['Дата '].fillna(value='итого', inplace=True)
        indices_of_bad_data = dataset[dataset['Дата '] == 'итого'].index
        dataset = dataset.drop(indices_of_bad_data)
        deadlines = dataset['Дедлайн'].tolist()
        list_of_deadline = []
        for i in range(len(deadlines)):
            if deadlines[i] == 1:
                list_of_deadline.append(True)
            else:
                list_of_deadline.append(False)
        teachers = dataset['Преподаватель'].tolist()
        distinct_teachers = list(set(teachers))
        list_of_distinct_teacher_names = []
        list_of_teacher_info = []
        for i in range(len(distinct_teachers)):
            needed_list = distinct_teachers[i].split()
            list_of_teacher_info.append(needed_list[0])
            list_of_distinct_teacher_names.append(needed_list[1] + ' ' + needed_list[2] + ' ' + needed_list[3])
        dataset['date'] = dataset['Дата '].apply(lambda x: x.strftime('%Y-%m-%d'))+ ' ' + dataset['Начало'] + ' ' + dataset['Окончание']
        list_of_times = dataset['date'].tolist()
        dataset['addinfo'] = dataset['День']+' '+ dataset['Ауд'] + ' ' + dataset['Группа (подгруппа)']
        list_of_add_info = dataset['addinfo'].tolist()
        self.lessons_.clear()
        self.teachers_.clear()
        self.assistants_.clear()
        self.tasks_.clear()
        for i in range(len(list_of_deadline)):
            self.lessons_.append(Lesson(Teacher('fake teacher', [], 'none', []), [], [], list_of_times[i], list_of_add_info[i], list_of_deadline[i], []))
        for i in range(len(list_of_teacher_info)):
            self.teachers_.append(Teacher(list_of_distinct_teacher_names[i], [], list_of_teacher_info[i], []))
        for i in range(len(list_of_names_of_assistants)):
            self.assistants_.append(Assistant(list_of_names_of_assistants[i], [], []))
        available_pairs = []
        for item in list_of_names_of_assistants:
            dataset[item].fillna(value=0, inplace=True)
            massive = [float(x) for x in dataset[item].tolist()]
            available_pairs.append(massive)
        # Мы же вносили ассистентов и пары по порядку в соответствующие списки. Воспользуемся этим.
        for i in range(len(list_of_names_of_assistants)):
            for j in range(dataset.shape[0]):
                if available_pairs[i][j] == 1:

                    self.assistants_[i].available_lessons_.append(self.lessons_[j])
                    self.lessons_[j].available_assistants_.append(self.assistants_[i])
        del dataset
        # А вот с учителями будет чуть сложнее.
        for i in range(len(teachers)):
            for j in range(len(self.teachers_)):
                if teachers[i] == self.teachers_[j].info_ + ' ' + self.teachers_[j].name_:
                    self.lessons_[i].teacher_ = self.teachers_[j]
                    self.teachers_[j].lessons_.append(self.lessons_[i])
        # Пересечения уроков тоже учтем.
        for i in range(len(self.lessons_) - 1):
            for j in range(i + 1, len(self.lessons_), 1):
                if self.lessons_[i].time_ == self.lessons_[j].time_ and i != j:
                    self.lessons_[i].intersecting_lessons_.append(self.lessons_[j])
                    for assistant in self.lessons_[i].available_assistants_:
                        if assistant not in self.lessons_[j].available_assistants_:
                            self.lessons_[j].available_assistants_.append(assistant)
                            if self.lessons_[j] not in assistant.available_lessons_:
                                assistant.available_lessons_.append(self.lessons_[j])
                    self.lessons_[j].intersecting_lessons_.append(self.lessons_[i])
                    for assistant in self.lessons_[j].available_assistants_:
                        if assistant not in self.lessons_[i].available_assistants_:
                            self.lessons_[i].available_assistants_.append(assistant)
                            if self.lessons_[i] not in assistant.available_lessons_:
                                assistant.available_lessons_.append(self.lessons_[i])
        #Парсим задания
        dataset=pd.read_excel(open_file,'Лист2')
        names_of_tasks=dataset['Название'].tolist()
        amounts_of_tasks=dataset['Число работ'].tolist()
        dataset['information']=dataset['Группа или вариант']+' '+str(dataset['Выдано'])+' '+str(dataset['Получено'])+' '+dataset['Время проверки']
        information=dataset['information'].tolist()
        scores_of_tasks=dataset['Вес'].tolist()
        for i in range(len(names_of_tasks)):
            self.tasks_.append(Task(names_of_tasks[i],information[i],amounts_of_tasks[i],scores_of_tasks[i]))
        self.AssignAssistants()

    def DumpToJson(self):
        import json as js
        res = {}
        for i in range(len(self.assistants_)):
            key = self.assistants_[i].name_
            value = []
            for j in range(len(self.assistants_[i].lessons_)):
                value.append(self.assistants_[i].lessons_[j].teacher_.info_ + ' ' + self.assistants_[i].lessons_[
                    j].teacher_.name_ + ' ' + self.assistants_[i].lessons_[j].time_ + ' ' +
                             self.assistants_[i].lessons_[j].additional_info_)
            inner = {key: value}
            res.update(inner)
        with open('data_file.json', 'w') as write_file:
            js.dump(res, write_file)
        self.DumpToXlsx()

    def DumpToXlsx(self):
        import pandas as pd
        list_of_dates=[]
        list_of_days=[]
        list_of_beg=[]
        list_of_end=[]
        list_of_rooms=[]
        list_of_teachers=[]
        list_of_groups=[]
        list_of_deadline=[]
        list_of_numbers=[]
        import datetime
        for i in range(len(self.lessons_)):
            date=self.lessons_[i].time_.split()
            add_infos=self.lessons_[i].additional_info_.split()
            date_split=date[0].split('-')
            date_split=list(map(int,date_split))
            exact_date=datetime.date(date_split[0],date_split[1],date_split[2])
            list_of_dates.append(exact_date)
            list_of_days.append(add_infos[0])
            list_of_beg.append(date[1])
            list_of_end.append(date[2])
            list_of_rooms.append(add_infos[1])
            list_of_teachers.append(self.lessons_[i].teacher_.info_+' '+self.lessons_[i].teacher_.name_)
            list_of_groups.append(add_infos[2])
            if self.lessons_[i].is_deadline_==True:
                list_of_deadline.append(1)
            else:
                list_of_deadline.append(0)
            list_of_numbers.append(len(self.lessons_[i].assistants_))
        crossings_dict=[]
        for i in range(len(self.assistants_)):
            key=self.assistants_[i].name_
            value=[]
            for t in range(len(self.lessons_)):
                flag=False
                for j in range(len(self.assistants_[i].lessons_)):
                    if self.lessons_[t].time_==self.assistants_[i].lessons_[j].time_ and self.lessons_[t].teacher_.name_==self.assistants_[i].lessons_[j].teacher_.name_:
                        flag=True
                if flag==False:
                    value.append(None)
                else:
                    value.append(1)
            crossings_dict.append(pd.DataFrame({key:value},index=None))
        def excel_date(date_input):
            temp=datetime.date(1899,12,31)
            delta=date_input-temp
            return float(delta.days)+1
        list_of_dates=list(map(excel_date,list_of_dates))
        dates=pd.DataFrame({'Дата':list_of_dates})
        days=pd.DataFrame({'День':list_of_days})
        beginnings=pd.DataFrame({'Начало':list_of_beg})
        endings=pd.DataFrame({'Окончание':list_of_end},index=None)
        rooms=pd.DataFrame({'Ауд':list_of_rooms},index=None)
        prepods=pd.DataFrame({'Преподаватель':list_of_teachers},index=None)
        groups=pd.DataFrame({'Группа(подгруппа)':list_of_groups},index=None)
        deadlines=pd.DataFrame({'Дедлайн':list_of_deadline},index=None)
        numbers=pd.DataFrame({'Число ассистентов':list_of_numbers},index=None)
        dataset=pd.concat([dates,days,beginnings,endings,rooms,prepods,groups,deadlines,numbers],axis=1)
        assistants_dataset=pd.DataFrame()
        for i in range(len(crossings_dict)):
            assistants_dataset=pd.concat([assistants_dataset,crossings_dict[i]],axis=1)
        dataset=pd.concat([dataset,assistants_dataset],axis=1)
        writer=pd.ExcelWriter('new_timetable.xlsx',engine='xlsxwriter')
        dataset.to_excel(writer,sheet_name='Лист1',index=False)
        workbook=writer.book
        worksheet=writer.sheets['Лист1']
        format1=workbook.add_format({'num_format':'ddmmyyyy'})
        worksheet.set_column('A:A',None,format1)
        writer.save()

    def AssignAssistants(self):
        lessons_with_no_students = []
        for lesson in self.lessons_:
            if len(lesson.assistants_) == 0 and len(lesson.available_assistants_) != 0:
                lessons_with_no_students.append(lesson)
        self.FillLayer(lessons_with_no_students, 1)
        for i in range(1, self.assistant_for_deadline_):
            lessons_with_deadline = []
            for lesson in self.lessons_:
                if len(lesson.assistants_) == i and len(lesson.available_assistants_) != 0 and lesson.is_deadline_:
                    lessons_with_deadline.append(lesson)
            self.FillLayer(lessons_with_deadline, i+1)
        for i in range(1, self.assistant_for_usual_lesson_):
            lessons_with_no_deadline = []
            for lesson in self.lessons_:
                if len(lesson.assistants_) == i and len(lesson.available_assistants_) != 0 and not lesson.is_deadline_:
                    lessons_with_no_deadline.append(lesson)
            self.FillLayer(lessons_with_no_deadline, i+1)
        self.DumpToJson()

    def FillLayer(self, lessons, number_of_needed_students):
        for lesson in lessons:
            if len(lesson.assistants_) < number_of_needed_students:
                if len(lesson.intersecting_lessons_) == 0:
                    self.ChooseAssistant(lesson)
                    continue
                if len(lesson.intersecting_lessons_) > 0:
                    # копирует хранилище, а не сами объекты
                    lessons_at_the_same_time = []
                    for buffer in lesson.intersecting_lessons_:
                        if buffer in lessons:
                            lessons_at_the_same_time.append(buffer)
                    lessons_at_the_same_time.append(lesson)
                    assistants = lesson.available_assistants_
                    for assistant in assistants:
                        if len(lessons_at_the_same_time) == 0:
                            continue
                        chosen_lesson = self.ChooseLesson(assistant, lessons_at_the_same_time)
                        lessons_at_the_same_time.remove(chosen_lesson)

    def ChooseLesson(self, assistant, lessons):
        have_deadline = []
        for lesson in lessons:
            if lesson.is_deadline_:
                have_deadline.append(lesson)
        if len(have_deadline) == 1:
            self.AddStudentToPair(assistant, have_deadline[0])
            return have_deadline[0]
        if len(have_deadline) > 1:
            teachers_preferences = []
            for lesson_with_deadline in have_deadline:
                if lesson_with_deadline.teacher_.prefering_assistants_.count(assistant) > 0:
                    teachers_preferences.append(lesson_with_deadline)
            if len(teachers_preferences) == 1:
                self.AddStudentToPair(assistant, teachers_preferences[0])
                return teachers_preferences[0]
            if len(teachers_preferences) > 1:
                for teacher_preference in teachers_preferences:
                    for assistant_preference in assistant.prefered_teachers_:
                        if assistant_preference == teacher_preference.teacher_:
                            self.AddStudentToPair(assistant, assistant_preference)
                            return assistant_preference
                self.AddStudentToPair(assistant, teachers_preferences[0])
                return teachers_preferences[0]
            # no teacher preferences
            for assistant_preference in assistant.prefered_teachers_:
                for lesson_with_deadline in have_deadline:
                    if assistant_preference == lesson_with_deadline.teacher_:
                        self.AddStudentToPair(assistant, assistant_preference)
                        return assistant_preference
            self.AddStudentToPair(assistant, have_deadline[0])
            return have_deadline[0]
        # no deadlines
        teachers_preferences = []
        for lesson in lessons:
            if lesson.teacher_.prefering_assistants_.count(assistant) > 0:
                teachers_preferences.append(lesson)
        if len(teachers_preferences) == 1:
            self.AddStudentToPair(assistant, teachers_preferences[0])
            return teachers_preferences[0]
        if len(teachers_preferences) > 1:
            for teacher_preference in teachers_preferences:
                for assistant_preference in assistant.prefered_teachers_:
                    if assistant_preference == teacher_preference.teacher_:
                        self.AddStudentToPair(assistant, assistant_preference)
                        return assistant_preference
            self.AddStudentToPair(assistant, teachers_preferences[0])
            return teachers_preferences[0]
        # no teacher preferences
        for assistant_preference in assistant.prefered_teachers_:
            for lesson in lessons:
                if assistant_preference == lesson.teacher_:
                    self.AddStudentToPair(assistant, assistant_preference)
                    return assistant_preference
        self.AddStudentToPair(assistant, lessons[0])
        return lessons[0]

    def ChooseAssistant(self, lesson):

        # копирует хранилище, а не сами объекты

        assistants = lesson.available_assistants_
        if len(assistants) == 0:
            return
        # find with min potentional score
        assistants_with_min_potentional_score = []
        min_potentional_score = assistants[0].potential_score_
        for assistant in assistants:
            if assistant.potential_score_ == min_potentional_score:
                assistants_with_min_potentional_score.append(assistant)
            if assistant.potential_score_ < min_potentional_score:
                assistants_with_min_potentional_score.clear()
                assistants_with_min_potentional_score.append(assistant)
                min_potentional_score = assistant.potential_score_
        if len(assistants_with_min_potentional_score) == 1:
            self.AddStudentToPair(assistants_with_min_potentional_score[0], lesson)
            return assistants_with_min_potentional_score[0]
        if len(assistants_with_min_potentional_score) > 1:
            # find with min amount of available pairs from assistants with min potentional score
            assistants_with_least_amount_of_planned_pairs = []
            least_amount_of_planned_pairs = len(assistants_with_min_potentional_score[0].lessons_)
            for assistant in assistants_with_min_potentional_score:
                if len(assistant.lessons_) == least_amount_of_planned_pairs:
                    assistants_with_least_amount_of_planned_pairs.append(assistant)
                if len(assistant.lessons_) < least_amount_of_planned_pairs:
                    assistants_with_least_amount_of_planned_pairs.clear()
                    assistants_with_least_amount_of_planned_pairs.append(assistant)
                    least_amount_of_planned_pairs = len(assistant.lessons_)
            if len(assistants_with_least_amount_of_planned_pairs) == 1:
                self.AddStudentToPair(assistants_with_least_amount_of_planned_pairs[0], lesson)
                return assistants_with_least_amount_of_planned_pairs[0]
            if len(assistants_with_least_amount_of_planned_pairs) > 1:
                # find teacher preferences of assistants with min amount of available
                # pairs from assistants with min potentional score
                prefering_assistants = []
                for assistant in assistants_with_least_amount_of_planned_pairs:
                    for prefering_assistant in lesson.teacher_.prefering_assistants_:
                        if assistant == prefering_assistant:
                            prefering_assistants.append(assistant)
                if len(prefering_assistants) == 1:
                    self.AddStudentToPair(prefering_assistants[0], lesson)
                if len(prefering_assistants) > 1:
                    # find assistants with min amount of available
                    # pairs from assistants with min potentional score,
                    # who like teacher of current pair
                    for assistant in prefering_assistants:
                        for prefering_teacher in assistant.prefered_teachers_:
                            if prefering_teacher == lesson.teacher_:
                                self.AddStudentToPair(assistant, lesson)
                                return assistant
                    self.AddStudentToPair(prefering_assistants[0], lesson)
                    return prefering_assistants[0]
                if len(prefering_assistants) == 0:
                    for assistant in assistants_with_least_amount_of_planned_pairs:
                        for prefering_teacher in assistant.prefered_teachers_:
                            if prefering_teacher == lesson.teacher_:
                                self.AddStudentToPair(assistant, lesson)
                                return assistant
                    self.AddStudentToPair(assistants_with_least_amount_of_planned_pairs[0], lesson)
                    return assistants_with_least_amount_of_planned_pairs[0]

    def AddStudentToPair(self, assistant, lesson):

        assistant.lessons_.append(lesson)

        for lesson_in_same_time in lesson.intersecting_lessons_:
            assistant.available_lessons_.remove(lesson_in_same_time)
        assistant.available_lessons_.remove(lesson)

        lesson.assistants_.append(assistant)
        for lesson_in_same_time in lesson.intersecting_lessons_:
            lesson_in_same_time.available_assistants_.remove(assistant)
        lesson.available_assistants_.remove(assistant)

manager = SchelduleManager('timetable.xlsx')