import sqlite3
import sys
from PyQt5 import uic, QtWidgets  # Импортируем uic
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTableWidgetItem, QDialog, QMessageBox

"""ОКНО ТИТУЛЬНОЕ """


class TitleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('title_window2.ui', self)  # Загружаем дизайн
        self.start_button.clicked.connect(self.menu_open)
        self.add_worktime.clicked.connect(self.AddWorkTime_open)

    def AddWorkTime_open(self):
        self.newWindow = AddWorkTimeDialog()
        self.newWindow.show()

    def menu_open(self):
        self.hide()
        self.newWindow = MenuWindow()
        self.newWindow.show()


"""ОКНО ГЛАВНОГО МЕНЮ РАБОТЫ """


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu_window.ui', self)  # Загружаем дизайн
        self.workers_button.clicked.connect(self.employees_window_open)
        self.work_button.clicked.connect(self.WorkWindow_open)
        self.prize_button.clicked.connect(self.PrizeWindow_open)
        self.reset_month.clicked.connect(self.month_null)
        self.information_button.clicked.connect(self.List_open)

    """ОТКРЫТЬ ОКНО РАБОТНИКОВ"""

    def employees_window_open(self):
        self.newWindow = EmployeesWindow()
        self.newWindow.show()

    """ОТКРЫТЬ ОКНО РАБОТЫ"""

    def WorkWindow_open(self):
        self.newWindow = WorkWindow()
        self.newWindow.show()
        # self.shift_button.clicked.connect(self.PrizeWindow_open)
        # self.salary_button.clicked.connect(self.PrizeWindow_open)

    """ИНФОРМАЦИЯ О СОТРУДНИКЕ"""

    def List_open(self):
        self.newWindow = ID_input_Window()
        self.newWindow.show()

    """ОКНО ПРЕМИИ"""

    def PrizeWindow_open(self):
        self.newWindow = PrizeAction()
        self.newWindow.show()

    """"СДЕЛАТЬ ОБНУЛЕНИЕ МЕСЯЦА"""

    def month_null(self):
        conn = sqlite3.connect('database.db')

        # выполнение запроса на обнуление значений в столбце work_time
        cursor = conn.cursor()
        cursor.execute("UPDATE employees SET work_time = 0 WHERE work_time > 0")
        cursor.execute("UPDATE employees SET salary = 0 WHERE salary > 0")
        conn.commit()

        # закрытие соединения с базой данных
        conn.close()
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Обнуление месяца")

        msg_box.setText("Месяц обнулен!")
        msg_box.exec_()


"""ОКНО РАБОТЫ"""


class WorkWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('salary_shift_window.ui', self)  # Загружаем дизайн
        self.shift_button.clicked.connect(self.AddWorkTime_open)
        self.salary_button.clicked.connect(self.SalaryWindow_open)

    # РАБОТА - СМЕНА
    def AddWorkTime_open(self):
        self.newWindow = AddWorkTimeDialog()
        self.newWindow.show()

    # РАБОТА - ЗАРПЛАТА
    def SalaryWindow_open(self):
        self.newWindow = EmployeeInfo()
        self.newWindow.show()


# РАБОТА - ЗАРПЛАТА - ТАБЛИЦА ЗАРПЛАТ
class EmployeeInfo(QtWidgets.QDialog):
    def __init__(self):
        super(EmployeeInfo, self).__init__()

        uic.loadUi('employee_info.ui', self)

        # СОЕДИНЕНИЕ С БД
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()

        # ФОРМИРОВАНИЕ ТАБЛИЦЫ ИМЕНА- ЗАРПЛАТА
        self.cur.execute('UPDATE employees SET salary = work_time * rate;')
        self.cur.execute('SELECT name, salary FROM employees')
        self.cur.execute('SELECT name, salary FROM employees')
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Salary'])
        for row, emp in enumerate(data):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(emp[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(emp[1])))

        # КНОПКА ОК - ЗАКРЫТЬ
        self.button.clicked.connect(self.close)

# РАБОТА - СМЕНА - ДОБАВИТЬ ЧАСЫ РАБОТЫ


class AddWorkTimeDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('AddWorktimeWindow.ui', self)  # Загружаем дизайн
        self.add_button.clicked.connect(self.add_work_time)

# ОБРАБОТКА ОШИБОК С ВВОДОМ
    def add_work_time(self):
        id = self.id_input.text()
        work_time = self.work_time_input.text()
        if id == '' or work_time == '':
            QMessageBox.warning(self, 'Предупреждение', 'Заполните все поля')
            return
        try:
            id = int(id)
            work_time = float(work_time)
        except ValueError:
            QMessageBox.warning(self, 'Предупреждение', 'Некорректные данные')
            return
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # ПРИБАВЛЕНИЕ ЧАСОВ В БД В ЯЧЕЙКАХ work_time
        cursor.execute('UPDATE employees SET work_time = work_time + ? WHERE id = ?', (work_time, id))
        conn.commit()
        conn.close()
        QMessageBox.information(self, 'Успех', 'Рабочие часы добавлены!')
        self.close()


"""ОКНО ПРЕМИЙ ВИДЖЕТ"""
# РАБОТА С CSV-ФАЙЛОМ НА ПРИМЕРЕ ЗАМЕТОК


class PrizeAction(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('PrizeAction.ui', self)  # Загружаем дизайн
        self.add_line_button.clicked.connect(self.add_prize_open)
        self.see_lines_button.clicked.connect(self.see_clear_open)

# ПРЕМИЯ - ДОБАВИТЬ ЗАМЕТКУ О ПРЕМИИ
    def add_prize_open(self):
        self.newWindow = Form()
        self.newWindow.show()

# ПРЕМИЯ - ПОСМОТРЕТЬ ЗАМЕТКИ
    def see_clear_open(self):
        self.newWindow = LinesWindow()
        self.newWindow.show()


class LinesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('see_clear_lines_widget.ui', self)
        self.clear_button.clicked.connect(self.clear_data)
        self.load_data()

    def load_data(self):
        # загрузка данных из csv-файла в таблицу
        with open('employees.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            row_count = len(data)
            self.table.setRowCount(row_count)
            for i in range(row_count):
                name = data[i][0]
                name_item = QTableWidgetItem(name)
                self.table.setItem(i, 0, name_item)

    def clear_data(self):
        # очистка csv-файла и таблицы
        with open('employees.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
        self.table.clearContents()
        self.table.setRowCount(0)


class Form(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_name_widget.ui', self)

        # создание кнопки для сохранения имени в csv-файл

        self.save_button.clicked.connect(self.save_name)
        self.v_layout.addWidget(self.save_button)

    def save_name(self):
        # получение имени работника из текстового поля
        name = self.name_edit.text()

        # сохранение имени в csv-файл
        with open('employees.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name])

        self.name_edit.setText('')


"""ОКНО СОТРУДНИКИ"""


class EmployeesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('employees_actions_window.ui', self)  # Загружаем дизайн
        self.add_employee_button.clicked.connect(self.add_employee_open)
        self.riskgroupbutton.clicked.connect(self.risk_group_label)
        self.dismiss_employee_button.clicked.connect(self.delete_employee_open)
        self.best_list.clicked.connect(self.bestlabel_open)

    def add_employee_open(self):
        self.newWindow = AddDialog()
        self.newWindow.show()

    def delete_employee_open(self):
        self.newWindow = DeleteDialog()
        self.newWindow.show()

    def risk_group_label(self):
        self.newWindow = PopupWindow()
        self.newWindow.show()

    def bestlabel_open(self):
        self.newWindow = BestEmployeesWindow()
        self.newWindow.show()
        pass


# СОТРУДНИКИ - ГРУППА РИСКА(ТЕ, У КОГО ЧАСОВ РАБОТЫ МЕНЬШЕ 5, ВОЗМОЖНЫЕ ПРЕТЕНДЕНТЫ НА УВОЛЬННИЕ В КОНЦЕ МЕСЯЦА)
class PopupWindow(QDialog):
    def __init__(self):
        super(PopupWindow, self).__init__()
        uic.loadUi('popup_window.ui', self)
        self.setWindowTitle('Employees with work time less than 5 hours')
        self.button_ok.clicked.connect(self.close)
        # Подключение к БД
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()

        # Получить данные из базы данных и отобразить их в виджете редактирования текста
        self.cur.execute('SELECT name FROM employees WHERE work_time < 5')
        data = self.cur.fetchall()
        for row in data:
            self.textEdit.append(row[0])


# СОТРУДНИКИ - СПИСОК ЛУЧШИХ(ОЦЕНИВАЕТСЯ ПО ВРЕМЕНИ РАБОТЫ, ПРЕДПОЛОЖИТЕЛЬНО ДЛЯ АНАЛИЗА КОМУ ПОЙДЕТ ПРЕМИЯ)
class BestEmployeesWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Best_Employees.ui', self)  # Загружаем дизайн

        self.ok_button.clicked.connect(self.close)

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT id, name FROM employees ORDER BY work_time DESC LIMIT 10')
        best_employees = cursor.fetchall()
        connection.close()

        text = ''
        for employee in best_employees:
            text += f'ID: {employee[0]}|| Name: {employee[1]}\n'

        self.textEdit.append(text)
        self.show()


# СОТРУДНИКИ - ДОБАВИТЬ(ВСЕ ПАРАМЕТРЫ ДЛЯ НОВОГО СОТРУДНИКА)
class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('AddDialog.ui', self)  # Загружаем дизайн
        self.btn_add.clicked.connect(self.add_employee)

    def add_employee(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        employee_id = int(self.txt_id.text())
        employee_name = self.txt_name.text()
        employee_rate = float(self.txt_rate.text())
        employee_work_time = float(self.txt_work_time.text())
        employee_salary = employee_rate * employee_work_time

        cursor.execute(
            f"INSERT INTO employees (id, name, rate, work_time, salary) VALUES ({employee_id}, '{employee_name}', \
                                    {employee_rate}, {employee_work_time}, {employee_salary})")

        conn.commit()
        conn.close()

        self.close()


# СОТРУДНИКИ - УВОЛИТЬ(СРАВНИМО С УДАЛЕНИЕМ ИЗ БД ВСЕЙ ЕГО СТРОКИ)
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('DeleteDialog.ui', self)
        self.delete_button.clicked.connect(self.delete_employee)

    def delete_employee(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        employee_id = int(self.txt_id.text())

        cursor.execute(f"DELETE FROM employees WHERE id={employee_id}")

        conn.commit()
        conn.close()

        self.close()


"""ИНФОРМАЦИЯ О СОТРУДНИКЕ - ГЛАВНОЕ МЕНЮ"""


class ID_input_Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('id_input.ui', self)
        self.ok_button.clicked.connect(self.open_employee_info_window)

    def open_employee_info_window(self):
        employee_id = int(self.id_input.text())
        self.employee_info_window = EmployeeInfoWindow(employee_id)
        self.employee_info_window.show()


# ГЛАВНОЕ МЕНЮ - ИНФОРМАЦИЯ - ВВЕСТИ ID
class EmployeeInfoWindow(QWidget):
    def __init__(self, employee_id):
        super().__init__()
        uic.loadUi('list_about_employee.ui', self)  # Загружаем дизайн
        self.employee_id = int(employee_id)
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT name, rate, work_time, salary FROM employees WHERE id={self.employee_id}")
        employee_info = cursor.fetchone()
        connection.close()

        # ТАБЛИЦА ИЗ ДАННЫХ СОТРУДНИКА ПОД НОМЕРОМ ID

        self.name_label.setText(f"{employee_info[0]}".capitalize())
        self.rate_label.setText(f"{employee_info[1]}")
        self.work_label.setText(f"{employee_info[2]}")
        self.salary_label.setText(f"{employee_info[3]}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TitleWindow()
    ex.show()
    sys.exit(app.exec_())
