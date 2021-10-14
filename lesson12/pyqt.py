from storage import ClientStorage
from tables import Client
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton
import sys


class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Асинхронный чат: список клиентов")
        self.resize(500, 320)

        self.textEdit = QTextEdit()
        self.btnPress = QPushButton("Получить список клиентов")

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btnPress)
        self.setLayout(layout)

        self.btnPress.clicked.connect(self.getClients)

    def getClients(self):
        client_storage = ClientStorage()
        clients = client_storage.get_list(Client)
        text = ''
        for client in clients:
            text += f"{client.id} {client.login}\n"
        self.textEdit.setPlainText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TextEditDemo()
    win.show()
    sys.exit(app.exec_())
    