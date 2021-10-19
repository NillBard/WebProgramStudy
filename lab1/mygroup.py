groupmates = [
        {
        "name": "Иван",
        "surname": "Иванов",
        "exams": ["Информатика", "ЭЭиС", "Web"],
        "marks": [4, 4, 5]
        },
          {
        "name": "Александр",
        "surname": "Петров",
        "exams": ["Литература", "Высшая математика", "Иностранный язык"],
        "marks": [5, 3, 4]
        },
          {
        "name": "Сергей",
        "surname": "Власов",
        "exams": ["Математика", "ЭЭиС", "История"],
        "marks": [3, 3, 5]
        },
          {
        "name": "Юлий",
        "surname": "Цезарь",
        "exams": ["Русский язык", "ЭЭиС", "Высшая математика"],
        "marks": [4, 2, 5]
        },
          {
        "name": "Дмитрий",
        "surname": "Гордон",
        "exams": ["История", "Литература", "Иностранный язык"],
        "marks": [5, 3, 2]
        },
          {
        "name": "Александр",
        "surname": "Иванов",
        "exams": ["Информатика", "ЭЭиС", "Web"],
        "marks": [4, 3, 5]
        },
          {
        "name": "Александр",
        "surname": "Иванов",
        "exams": ["Информатика", "ЭЭиС", "Web"],
        "marks": [5, 4, 3]
        },
          {
        "name": "Евгений",
        "surname": "Сидоров",
        "exams": ["Информатика", "История", "Web"],
        "marks": [4, 3, 2]
        },
]



def print_students(students):
    print(u"Имя".ljust(15), u"Фамилия".ljust(10), u"Экзамены".ljust(60), u"Оценки".ljust(20))
    for student in groupmates: 
      print(student["name"].ljust(15), student["surname"].ljust(10), str(student["exams"]).ljust(60), str(student["marks"]).ljust(20))

print_students(groupmates)

mid = input('Средняя оценка ')

def findMin(student): 
    for student in groupmates:
        if sum(student['marks'])/len(student['marks']) > float(mid):
            print(student["name"].ljust(15), student["surname"].ljust(10), str(student["exams"]).ljust(60), str(student["marks"]).ljust(20))
findMin(groupmates)