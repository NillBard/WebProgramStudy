// var groupmates = [
//   {
//     name: "Александр",
//     surname: "Иванов",
//     group: "БВТ1702",
//     marks: [4, 3, 5],
//   },
//   {
//     name: "Иван",
//     surname: "Петров",
//     group: "БСТ1702",
//     marks: [4, 4, 4],
//   },
//   {
//     name: "Кирилл",
//     surname: "Смирнов",
//     group: "БАП1801",
//     marks: [5, 5, 5],
//   },
// ];

// var rpad = function (str, length) {
//   str = str.toString(); // преобразование в строку
//   while (str.length < length) str = str + " ";
//   return str; // добавление пробела в конец строки return str; // когда все пробелы добавлены, возвратить строку
// };

// var printStudents = function (students) {
//   console.log(
//     rpad("Имя", 15),
//     rpad("Фамилия", 15),
//     rpad("Группа", 8),
//     "Оценки"
//   );

//   for (var i = 0; i <= students.length - 1; i++) {
//     console.log(
//       rpad(students[i]["name"], 15),
//       rpad(students[i]["surname"], 15),
//       rpad(students[i]["group"], 8),
//       students[i]["marks"].join(",")
//     );
//   }
//   console.log("\n"); // добавляется пустая строка в конце вывода
// };

// let groupFilter = () => {
//   let group = prompt("Введите группу");
//   let newGroups = groupmates.filter((item) => item["group"] == group);
//   if (newGroups.length == 0) {
//     console.log("Студентов из такой группы нет");
//   } else {
//     printStudents(newGroups);
//   }
// };

// let marksFilter = () => {
//   let marks = +prompt("Введите среднюю оценку");
//   let newMarks = groupmates.filter(
//     (item) =>
//       item["marks"].reduce((prev, next) => prev + next) /
//         item["marks"].length >=
//       marks
//   );

//   if (newMarks.length == 0) {
//     console.log("Студентов с таким средним баллом нет");
//   } else {
//     printStudents(newMarks);
//   }
// };

// groupFilter();
// marksFilter();
