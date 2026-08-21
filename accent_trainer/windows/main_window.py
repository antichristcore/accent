from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QInputDialog, QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from .training_window import TrainingWindow
from .test_window import TestWindow
from .stats_window import StatsWindow
from .settings_window import SettingsWindow


class MainWindow(QMainWindow):
    def __init__(self, db, user_id, name):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.name = name
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Главное меню')
        self.setFixedSize(640, 360)

        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.label = QLabel(f'Привет, {self.name}!', self.central)
        self.label.setFont(QFont('Arial', 24))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.move(0, 30)
        self.label.resize(640, 50)

        self.b1 = QPushButton('Обучение', self.central)
        self.b1.move(220, 100)
        self.b1.resize(200, 40)

        self.b2 = QPushButton('Тестирование', self.central)
        self.b2.move(220, 150)
        self.b2.resize(200, 40)

        self.b3 = QPushButton('Статистика', self.central)
        self.b3.move(220, 200)
        self.b3.resize(200, 40)

        self.b4 = QPushButton('Настройки', self.central)
        self.b4.move(220, 250)
        self.b4.resize(200, 40)

        self.b5 = QPushButton('Выход', self.central)
        self.b5.move(220, 300)
        self.b5.resize(200, 40)

        self.b1.clicked.connect(self.train)
        self.b2.clicked.connect(self.test)
        self.b3.clicked.connect(self.stats)
        self.b4.clicked.connect(self.settings)
        self.b5.clicked.connect(self.exit)

    def train(self):
        self.ttw = TrainingWindow(self.db, self.user_id)
        self.ttw.show()

    def test(self):
        total, ok_pressed = QInputDialog.getInt(
            self, "Настройки", "Введите количество слов:",
            20, 5, 200, 1
        )
        if ok_pressed:
            self.tw = TestWindow(self.db, self.user_id, total)
            self.tw.show()

    def stats(self):
        self.sw = StatsWindow(self.db, self.user_id)
        self.sw.show()

    def settings(self):
        self.st = SettingsWindow(self.db, self.user_id)
        self.st.show()

    def exit(self):
        QApplication.instance().quit()