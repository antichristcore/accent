from PyQt6.QtWidgets import QWidget, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import random


class TrainingWindow(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.setWindowTitle('Обучение')
        self.setFixedSize(600, 250)
        self.user_id = user_id

        self.word_label = QLabel(self)
        self.word_label.setFont(QFont('Arial', 24))
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.move(0, 30)
        self.word_label.resize(600, 50)

        self.btn1 = QPushButton(self)
        self.btn1.move(120, 100)
        self.btn1.resize(160, 40)

        self.btn2 = QPushButton(self)
        self.btn2.move(320, 100)
        self.btn2.resize(160, 40)

        self.result_label = QLabel(self)
        self.result_label.move(0, 160)
        self.result_label.resize(600, 30)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont('Arial', 12))

        self.next_btn = QPushButton('Следующее слово', self)
        self.next_btn.move(230, 200)
        self.next_btn.resize(140, 40)

        self.btn1.clicked.connect(lambda: self.check(self.btn1.text()))
        self.btn2.clicked.connect(lambda: self.check(self.btn2.text()))
        self.next_btn.clicked.connect(self.next)

        self.next()

    def next(self):
        words = self.db.get_random_words(1, self.user_id)
        if not words:
            self.word_label.setText('Нет слов в базе')
            return

        wid, w, correct, wrong = words[0]
        if random.choice([True, False]):
            self.btn1.setText(correct)
            self.btn2.setText(wrong)
            self.correct = correct
        else:
            self.btn1.setText(wrong)
            self.btn2.setText(correct)
            self.correct = correct

        self.word_label.setText(w)
        self.result_label.setText('')
        self.word_id = wid

    def check(self, chosen):
        if chosen == self.correct:
            self.result_label.setText('✅ Правильно!')
        else:
            self.result_label.setText(f'❌ Неправильно — правильно: {self.correct}')



