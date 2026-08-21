import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from database import Database
from windows.login_window import LoginWindow
from windows.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("ege.ico"))
    db = Database()
    login = LoginWindow(db)
    login.show()
    app.exec()
    if not login.user_id:
        return
    uid = login.user_id
    cur = db.conn.cursor()
    cur.execute("""SELECT name FROM users WHERE id = ?""", (uid,))
    name = cur.fetchone()[0]
    mw = MainWindow(db, uid, name)
    mw.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
