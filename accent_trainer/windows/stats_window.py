from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class StatsWindow(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Статистика')
        self.setFixedSize(750, 520)

        self.title = QLabel("Статистика по тестам", self)
        self.title.setFont(QFont('Arial', 22))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.move(0, 10)
        self.title.resize(750, 40)

        self.tests_label = QLabel(self)
        self.tests_label.setFont(QFont('Arial', 14))
        self.tests_label.move(40, 70)

        self.avg_label = QLabel(self)
        self.avg_label.setFont(QFont('Arial', 14))
        self.avg_label.move(40, 100)

        self.best_label = QLabel(self)
        self.best_label.setFont(QFont('Arial', 14))
        self.best_label.move(40, 130)

        self.words_table = QTableWidget(self)
        self.words_table.setSortingEnabled(True)
        self.words_table.move(40, 170)
        self.words_table.resize(650, 270)
        self.words_table.setColumnCount(2)
        self.words_table.setHorizontalHeaderLabels(['Слово', 'Процент'])
        self.words_table.setColumnWidth(0, 300)
        self.words_table.setColumnWidth(1, 305)
        self.words_table.setEditTriggers(self.words_table.EditTrigger.NoEditTriggers)

        self.clear_btn = QPushButton('Очистить статистику', self)
        self.clear_btn.move(200, 460)
        self.clear_btn.resize(180, 40)
        self.clear_btn.clicked.connect(self.clear)

        self.back_btn = QPushButton('Назад', self)
        self.back_btn.move(400, 460)
        self.back_btn.resize(180, 40)
        self.back_btn.clicked.connect(self.close)
        self.load()

    def load(self):
        s = self.db.get_stats_for_user(self.user_id)
        self.tests_label.setText(f'Тестов: {s["tests"]}')
        self.avg_label.setText(f'Средний результат: {int(s["avg"] * 100)}%')
        self.best_label.setText(f'Лучший результат: {s["best"]}%')
        self.load_word_stats()

    def clear(self):
        r = QMessageBox.question(self, 'Удалить?', 'Очистить статистику?')
        if r == QMessageBox.StandardButton.Yes:
            cur = self.db.conn.cursor()
            cur.execute('DELETE FROM results WHERE user_id = ?', (self.user_id,))
            cur.execute('UPDATE word_stats SET correct_count = 0, wrong_count = 0 WHERE user_id = ?', (self.user_id,))
            cur.execute('UPDATE users SET best_score = 0 WHERE id = ?', (self.user_id,))
            self.db.conn.commit()
            self.load()

    def load_word_stats(self):
        cur = self.db.conn.cursor()
        rows = cur.execute('SELECT * FROM word_stats WHERE user_id = ?', (self.user_id,)).fetchall()
        self.words_table.clearContents()
        self.words_table.setRowCount(len(rows))
        for i, (id, user_id, word_id, correct, wrong) in enumerate(rows):
            total = correct + wrong
            percent = round((correct / total * 100), 1) if total > 0 else 0
            if percent == 0.0:
                percent = 0
            word = cur.execute('SELECT word FROM words WHERE id = ?', (word_id,)).fetchone()[0]
            print(word, percent)
            self.words_table.setItem(i, 0, QTableWidgetItem(word))
            self.words_table.setItem(i, 1, QTableWidgetItem(f"{percent}%"))