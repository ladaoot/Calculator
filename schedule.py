import psycopg2
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QAbstractScrollArea, QVBoxLayout, QHBoxLayout, \
    QTableWidget, QGroupBox, QTableWidgetItem, QPushButton, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()
        self.vbox = QVBoxLayout(self)
        self.setWindowTitle("Schedule")

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_schedule_tab()
        self._create_teacher_tab()
        self._create_subject_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="schedule",
                                     user="postgres",
                                     password='lada',
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Subjects")

        self.svbox2 = QVBoxLayout()

        self.subject_gbox = QGroupBox("Предмены")

        self.shboxSS1 = QHBoxLayout()
        self.shboxSS2 = QHBoxLayout()

        self.svbox2.addLayout(self.shboxSS1)
        self.svbox2.addLayout(self.shboxSS2)

        self.shboxSS1.addWidget(self.subject_gbox)

        self._create_subject_table()

        self.subject_tab.setLayout(self.svbox2)
        self.update_subject_button = QPushButton("Update")
        self.shboxSS2.addWidget(self.update_subject_button)

        self.update_subject_button.clicked.connect(self._update_subject_table)

    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.monday_table.setVerticalScrollBarPolicy()

        self.subject_table.setColumnCount(3)
        self.subject_table.setHorizontalHeaderLabels(["Subject", "", ""])

        self._update_subject_table()

        self.mvboxSS = QVBoxLayout()
        self.mvboxSS.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvboxSS)

    def _update_subject_table(self):
        self.cursor.execute("SELECT * FROM subject")
        records = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            id = r[0]
            join_button = QPushButton("Join")
            delete_button = QPushButton("Delete")

            self.subject_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))

            self.subject_table.setCellWidget(i, 1, join_button)

            self.subject_table.setCellWidget(i, 2, delete_button)

            join_button.clicked.connect(lambda ch, st=r[0], num=i: self._change_day_from_table_s(num, st))

            delete_button.clicked.connect(lambda ch, st=r[0]: self._delete_day_from_table_s(st))

        set_button = QPushButton("Set")

        self.subject_table.setCellWidget(len(records), 1, set_button)
        set_button.clicked.connect(lambda ch: self._set_day_to_table_s(len(records)))

        self.subject_table.resizeRowsToContents()

    def _change_day_from_table_s(self, num, st):
        row = list()
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(num, i).text())
            except Exception:
                row.append(None)
        try:
            self.cursor.execute(
                f"UPDATE subject set name = '{row[0]}' where name = {st}")
            self.conn.commit()
        except Exception:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_day_from_table_s(self, st):
        try:
            self.cursor.execute(
                f"delete from subject where name = {st}")
            self.conn.commit()
        except Exception:
            QMessageBox.about(self, "Error", "Cant delete row")

    def _set_day_to_table_s(self, num):
        row = list()
        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(num, i).text())
            except Exception:
                row.append(None)
        try:
            self.cursor.execute(
                f"insert into subject (name) values('{row[0]}')")
            self.conn.commit()
        except Exception:
            QMessageBox.about(self, "Error", "Cant insert row")

    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teacher")

        self.svbox1 = QVBoxLayout()

        self.teacher_gbox = QGroupBox("Учителя")

        self.shboxTT1 = QHBoxLayout()
        self.shboxTT2 = QHBoxLayout()

        self.svbox1.addLayout(self.shboxTT1)
        self.svbox1.addLayout(self.shboxTT2)

        self.shboxTT1.addWidget(self.teacher_gbox)

        self._create_teacher_table()

        self.teacher_tab.setLayout(self.svbox1)
        self.update_teacher_button = QPushButton("Update")
        self.shboxTT2.addWidget(self.update_teacher_button)

        self.update_teacher_button.clicked.connect(self._update_teacher_table)

    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.monday_table.setVerticalScrollBarPolicy()

        self.teacher_table.setColumnCount(4)
        self.teacher_table.setHorizontalHeaderLabels(["Name", "Subject", "", ""])

        self._update_teacher_table()

        self.mvboxT = QVBoxLayout()
        self.mvboxT.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvboxT)

    def _update_teacher_table(self):
        self.cursor.execute(f"SELECT * FROM teacher")
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            id = r[0]
            join_button = QPushButton("Join")
            delete_button = QPushButton("Delete")

            self.teacher_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[2])))

            self.teacher_table.setCellWidget(i, 2, join_button)

            self.teacher_table.setCellWidget(i, 3, delete_button)

            join_button.clicked.connect(lambda ch, id_n=id, num=i: self._change_day_from_table_t(num, id_n))

            delete_button.clicked.connect(lambda ch, id_n=id: self._delete_day_from_table_t(id_n))

        set_button = QPushButton("Set")

        self.teacher_table.setCellWidget(len(records), 2, set_button)
        set_button.clicked.connect(lambda ch, num=len(records): self._set_day_to_table_t(num))

        self.teacher_table.resizeRowsToContents()

    def _change_day_from_table_t(self, num, id_n):
        row = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(num, i).text())
            except Exception:
                row.append(None)
        try:
            self.cursor.execute(
                f"UPDATE teacher set full_name = '{row[0]}', subject = '{row[1]}' where id = {id_n}")
            self.conn.commit()
        except Exception:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_day_from_table_t(self, id):
        try:
            self.cursor.execute(
                f"delete from teacher where id = {id}")
            self.conn.commit()
        except Exception:
            QMessageBox.about(self, "Error", "Cant delete row")

    def _set_day_to_table_t(self, num):
        row = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(num, i).text())
            except Exception:
                row.append(None)
        try:
            self.cursor.execute(
                f"insert into teacher (full_name, subject) values( '{row[0]}','{row[1]}')")
            self.conn.commit()
        except Exception:
            QMessageBox.about(self, "Error", "Cant insert row")

    def _create_schedule_tab(self):
        self.schedule_tab = QWidget()
        # self.scroll = QScrollArea(self.schedule_tab)
        # # self.scroll.setWidgetResizable(True)
        #
        self.tabs.addTab(self.schedule_tab, "Schedule")

        self.monday_gbox = QGroupBox("Понедельник")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)

        self._create_monday_table()

        self.tuesday_gbox = QGroupBox("Вторник")

        self.svboxT = QVBoxLayout()
        self.shboxT1 = QHBoxLayout()
        self.shboxT2 = QHBoxLayout()

        self.svbox.addLayout(self.shboxT1)
        self.svbox.addLayout(self.shboxT2)

        self.shboxT1.addWidget(self.tuesday_gbox)

        self._create_tuesday_table()

        self.wednesday_gbox = QGroupBox("Среда")

        self.svboxW = QVBoxLayout()
        self.shboxW1 = QHBoxLayout()
        self.shboxW2 = QHBoxLayout()

        self.svbox.addLayout(self.shboxW1)
        self.svbox.addLayout(self.shboxW2)

        self.shboxW1.addWidget(self.wednesday_gbox)

        self._create_wednesday_table()

        self.thursday_gbox = QGroupBox("Четверг")

        self.svboxTH = QVBoxLayout()
        self.shboxTH1 = QHBoxLayout()
        self.shboxTH2 = QHBoxLayout()

        self.svbox.addLayout(self.shboxTH1)
        self.svbox.addLayout(self.shboxTH2)

        self.shboxTH1.addWidget(self.thursday_gbox)

        self._create_thursday_table()

        self.friday_gbox = QGroupBox("Пятница")

        # self.svboxTH = QVBoxLayout()
        self.shboxF1 = QHBoxLayout()
        self.shboxF2 = QHBoxLayout()

        self.svbox.addLayout(self.shboxF1)
        self.svbox.addLayout(self.shboxF2)

        self.shboxF1.addWidget(self.friday_gbox)

        self._create_friday_table()

        self.saturday_gbox = QGroupBox("Суббота")

        # self.svboxTH = QVBoxLayout()
        self.shboxS1 = QHBoxLayout()
        self.shboxS2 = QHBoxLayout()

        self.svbox.addLayout(self.shboxS1)
        self.svbox.addLayout(self.shboxS2)

        self.shboxS1.addWidget(self.saturday_gbox)

        self._create_saturday_table()

        self.update_schedule_button = QPushButton("Update")
        self.shboxS2.addWidget(self.update_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_schedule)

        self.schedule_tab.setLayout(self.svbox)

    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.monday_table.setVerticalScrollBarPolicy()

        self.monday_table.setColumnCount(6)
        self.monday_table.setHorizontalHeaderLabels(["Subject", "Time", "Week", "Room number", "", ""])

        self._update_table(self.monday_table, 'Понедельник')

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table.setColumnCount(6)
        self.tuesday_table.setHorizontalHeaderLabels(["Subject", "Time", "Week", "Room number", "", ""])

        self._update_table(self.tuesday_table, 'Вторник')

        self.mvboxT = QVBoxLayout()
        self.mvboxT.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvboxT)

    def _create_wednesday_table(self):
        self.wednesday_table = QTableWidget()
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)

        self.wednesday_table.setColumnCount(6)
        self.wednesday_table.setHorizontalHeaderLabels(["Subject", "Time", "Week", "Room number", "", ""])

        self._update_table(self.wednesday_table, 'Среда')

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.mvbox)

    def _create_thursday_table(self):
        self.thursday_table = QTableWidget()
        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.thursday_table.setColumnCount(6)
        self.thursday_table.setHorizontalHeaderLabels(["Subject", "Time", "Week", "Room number", "", ""])

        self._update_table(self.thursday_table, 'Четверг')

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.thursday_table)
        self.thursday_gbox.setLayout(self.mvbox)

    def _create_friday_table(self):
        self.friday_table = QTableWidget()
        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.friday_table.setColumnCount(6)
        self.friday_table.setHorizontalHeaderLabels(["Subject", "Time", "Week", "Room number", "", ""])

        self._update_table(self.friday_table, 'Пятница')

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.friday_table)
        self.friday_gbox.setLayout(self.mvbox)

    def _create_saturday_table(self):
        self.saturday_table = QTableWidget()
        self.saturday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.saturday_table.setColumnCount(6)
        self.saturday_table.setHorizontalHeaderLabels(["Subject", "Time", "Week", "Room number", "", ""])

        self._update_table(self.saturday_table, 'Суббота')

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.saturday_table)
        self.saturday_gbox.setLayout(self.mvbox)

    def _update_table(self, table, st):
        self.cursor.execute(f"SELECT * FROM timetable WHERE day='{st}' order by week, start_time ")
        records = list(self.cursor.fetchall())

        table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            id = r[0]
            join_button = QPushButton("Join")
            delete_button = QPushButton("Delete")

            table.setItem(i, 0,
                          QTableWidgetItem(str(r[3])))
            table.setItem(i, 1,
                          QTableWidgetItem(str(r[5])))
            table.setItem(i, 2,
                          QTableWidgetItem(str(r[2])))
            table.setItem(i, 3,
                          QTableWidgetItem(str(r[4])))

            table.setCellWidget(i, 4, join_button)

            table.setCellWidget(i, 5, delete_button)

            join_button.clicked.connect(lambda ch, id_n=id, num=i: self._change_day_from_table(num, id_n, table))

            delete_button.clicked.connect(lambda ch, id_n=id: self._delete_day_from_table(id_n))

        set_button = QPushButton("Set")

        table.setCellWidget(len(records), 4, set_button)
        set_button.clicked.connect(lambda ch, num=len(records): self._set_day_to_table(num, st, table))

        table.resizeRowsToContents()

    def _change_day_from_table(self, num, id_n, table):
        row = list()
        for i in range(table.columnCount()):
            try:
                row.append(table.item(num, i).text())
            except Exception:
                row.append(None)
        try:
            self.cursor.execute(
                f"UPDATE timetable set start_time = '{row[1]}', week= '{row[2]}', subject = '{row[0]}', room_number='{row[3]}' where id = {id_n}")
            self.conn.commit()
        except Exception:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_day_from_table(self, id):
        try:
            self.cursor.execute(
                f"delete from timetable where id = {id}")
            self.conn.commit()
        except Exception:
            QMessageBox.about(self, "Error", "Cant delete row")

    def _set_day_to_table(self, num, st, table):
        row = list()
        for i in range(table.columnCount()):
            try:
                row.append(table.item(num, i).text())
            except Exception:
                row.append(None)
        try:
            self.cursor.execute(
                f"insert into timetable (start_time, week, subject, day, room_number) values( '{row[1]}','{row[2]}','{row[0]}', '{st}', '{row[3]}')")
            self.conn.commit()
        except Exception:
            QMessageBox.about(self, "Error", "Cant insert row")

    def _update_schedule(self):
        self._update_table(self.monday_table, "Понедельник")
        self._update_table(self.tuesday_table, "Вторник")
        self._update_table(self.wednesday_table, "Среда")
        self._update_table(self.thursday_table, "Четверг")
        self._update_table(self.friday_table, "Пятница")
        self._update_table(self.saturday_table, "Суббота")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
