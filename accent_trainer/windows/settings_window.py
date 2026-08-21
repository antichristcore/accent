from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView
from utils import load_words

class SettingsWindow(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Настройки')
        self.setFixedSize(700, 500)

        self.table = QTableWidget(self)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.table.move(30, 20)
        self.table.resize(640, 220)
        self.table.setColumnCount(3)
        self.table.setColumnWidth(0, 199)
        self.table.setColumnWidth(1, 199)
        self.table.setColumnWidth(2, 199)
        self.table.setHorizontalHeaderLabels(['Слово', 'Правильно', 'Неправильно'])
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)

        self.correct_label = QLabel('Корректное написание:', self)
        self.correct_label.move(40, 270)
        self.correct_label.resize(250, 30)

        self.correct_input = QLineEdit(self)
        self.correct_input.move(260, 270)
        self.correct_input.resize(380, 30)

        self.incorrect_label = QLabel('Некорректное написание:', self)
        self.incorrect_label.move(40, 320)
        self.incorrect_label.resize(250, 30)

        self.incorrect_input = QLineEdit(self)
        self.incorrect_input.move(260, 320)
        self.incorrect_input.resize(380, 30)

        self.delete_btn = QPushButton('Удалить выбранное', self)
        self.delete_btn.move(50, 370)
        self.delete_btn.resize(180, 40)
        self.delete_btn.clicked.connect(self.delete_word)

        self.add_btn = QPushButton('Добавить слово', self)
        self.add_btn.move(260, 370)
        self.add_btn.resize(180, 40)
        self.add_btn.clicked.connect(self.add_word)

        self.reset_btn = QPushButton('Сбросить', self)
        self.reset_btn.move(470, 370)
        self.reset_btn.resize(180, 40)
        self.reset_btn.clicked.connect(self.reset)
        self.load_words_to_table()

    def is_russian_word(self, text):
        for ch in text:
            code = ord(ch.lower())
            if not (1072 <= code <= 1103 or code == 1105):
                return False
        return True

    def has_one_uppercase(self, text):
        count = 0
        for ch in text:
            code = ord(ch)
            if (code >= 1040 and code <= 1071) or code == 1025:
                count += 1
        if count == 1:
            return True
        return False

    def load_words_to_table(self):
        words = self.db.get_all_words(self.user_id)
        self.table.setRowCount(len(words))
        for i, (wid, w, correct, incorrect) in enumerate(words):
            self.table.setItem(i, 0, QTableWidgetItem(w))
            self.table.setItem(i, 1, QTableWidgetItem(correct))
            self.table.setItem(i, 2, QTableWidgetItem(incorrect))

    def delete_word(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            QMessageBox.warning(self, 'Ошибка', 'Выберите одно или несколько слов для удаления.')
            return
        reply = QMessageBox.question(self, 'Удалить?', f'Удалить выбранные слова ({len(rows)} шт.)?')
        if reply != QMessageBox.StandardButton.Yes:
            return
        cur = self.db.conn.cursor()
        for row in rows:
            word = self.table.item(row.row(), 0).text()
            cur.execute('DELETE FROM words WHERE word = ?', (word,))
        self.db.conn.commit()
        self.load_words_to_table()
        self.table.clearSelection()
        self.table.setCurrentCell(-1, -1)

    def add_word(self):
        correct = self.correct_input.text().strip()
        incorrect = self.incorrect_input.text().strip()
        word = correct.lower()

        if not correct or not incorrect:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля!')
            return

        if not self.is_russian_word(word):
            QMessageBox.warning(self, 'Ошибка', 'Слово должно содержать только русские буквы.')
            return

        if not self.has_one_uppercase(correct):
            QMessageBox.warning(self, 'Ошибка',
                                'В корректном написании должно быть хотя бы одно ударение (заглавная буква).')
            return

        if not self.has_one_uppercase(incorrect):
            QMessageBox.warning(self, 'Ошибка',
                                'В некорректном написании должно быть хотя бы одно ударение (заглавная буква).')
            return

        if word != incorrect.lower():
            QMessageBox.warning(self, 'Ошибка', 'Введены разные слова')
            return
        if correct == incorrect:
            QMessageBox.warning(self, 'Ошибка', 'Корректное слово должно быть отличным от некорректного')
            return
        try:
            self.db.add_word(word, correct, incorrect, self.user_id)
            QMessageBox.information(self, 'Успешно', f'Слово «{word}» добавлено!')
            self.correct_input.clear()
            self.incorrect_input.clear()
            self.table.clearContents()
            self.load_words_to_table()
        except Exception as e:
            print('Ошибка', f'Не удалось добавить слово: {e}')

    def reset(self):
        cur = self.db.conn.cursor()
        try:
            cur.execute('DELETE FROM words WHERE user_id = ?', (self.user_id,))
            cur.execute('DELETE FROM word_stats WHERE user_id = ?', (self.user_id,))
            self.db.conn.commit()
            load_words('accent_trainer.db', self.user_id)
            self.load_words_to_table()
        except Exception as e:
            print(e)

