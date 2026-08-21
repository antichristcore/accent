from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QProgressBar, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import random


class TestWindow(QWidget):
    def __init__(self, db, user_id, total):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.total = total

        self.setWindowTitle('Тест')
        self.setFixedSize(700, 300)

        self.word_label = QLabel(self)
        self.word_label.setFont(QFont('Arial', 28))
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.move(0, 30)
        self.word_label.resize(700, 50)

        self.btn1 = QPushButton(self)
        self.btn1.move(150, 100)
        self.btn1.resize(180, 50)

        self.btn2 = QPushButton(self)
        self.btn2.move(370, 100)
        self.btn2.resize(180, 50)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(150, 180, 400, 25)
        self.progress.setMaximum(self.total)

        self.status_label = QLabel(self)
        self.status_label.move(340, 220)
        self.status_label.resize(200, 30)

        self.btn1.clicked.connect(lambda: self.answer(self.btn1.text()))
        self.btn2.clicked.connect(lambda: self.answer(self.btn2.text()))

        self.index = 0
        self.correct_count = 0
        self.questions = self.db.get_random_words(self.total, self.user_id)

        if not self.questions:
            QMessageBox.warning(self, 'Ошибка', 'Нет слов в базе')
            self.close()
        else:
            self.load()

    def load(self):
        if self.index >= len(self.questions):
            self.finish()
            return

        wid, w, correct, wrong = self.questions[self.index]
        self.word_id = wid
        if random.choice([True, False]):
            self.btn1.setText(correct)
            self.btn2.setText(wrong)
            self.correct = correct
        else:
            self.btn1.setText(wrong)
            self.btn2.setText(correct)
            self.correct = correct

        self.word_label.setText(w)
        self.progress.setValue(self.index)
        self.status_label.setText(f'{self.index + 1}/{self.total}')

    def answer(self, chosen):
        if chosen == self.correct:
            self.correct_count += 1
            self.db.update_stat(self.user_id, self.word_id, True)
        else:
            self.db.update_stat(self.user_id, self.word_id, False)
        self.index += 1
        self.load()

    def finish(self):
        self.progress.setValue(self.total)
        result_msg = f'Результат: {self.correct_count}/{self.total}'
        QMessageBox.information(self, 'Результат', result_msg)
        self.percentage = (self.correct_count / self.total) * 100
        self.db.save_result(self.user_id, self.correct_count, self.total, self.percentage)
        self.close()
