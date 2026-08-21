from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
import sqlite3

from utils import load_words


class LoginWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.conn = sqlite3.connect("accent_trainer.db")
        self.user_id = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Вход')
        self.setFixedSize(400, 200)

        self.label = QLabel('Введите имя пользователя:', self)
        self.label.move(40, 30)
        self.label.resize(320, 30)

        self.name_input = QLineEdit(self)
        self.name_input.move(40, 70)
        self.name_input.resize(320, 30)

        self.login_btn = QPushButton('Войти', self)
        self.login_btn.move(60, 130)
        self.login_btn.resize(120, 40)

        self.create_btn = QPushButton('Создать профиль', self)
        self.create_btn.move(220, 130)
        self.create_btn.resize(120, 40)

        self.login_btn.clicked.connect(self.login)
        self.create_btn.clicked.connect(self.create_profile)


    def load_words(self):
        cur = self.conn.cursor()
        if len(cur.execute('SELECT word FROM words WHERE user_id == ?', (self.user_id,)).fetchall()) == 0:
            load_words("accent_trainer.db", self.user_id)


    def login(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, 'Ошибка', 'Введите имя')
            return
        uid = self.db.get_user_id(name)
        if uid is None:
            QMessageBox.warning(self, 'Не найдено', 'Создайте профиль.')
            return
        self.user_id = uid
        self.load_words()
        self.close()

    def create_profile(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, 'Ошибка', 'Введите имя')
            return
        if self.db.get_user_id(name):
            QMessageBox.warning(self, 'Ошибка', 'Профиль с таким именем уже существует.')
            return
        uid = self.db.add_user(name)
        QMessageBox.information(self, 'Готово', f'Профиль {name} создан.')
        self.user_id = uid
        self.load_words()
        self.close()