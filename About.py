
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("About - Heat Transfer Simulation")
        self.resize(560, 500)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Heat Transfer Simulation")
        title.setObjectName("mainTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        picture = QLabel()
        image = QPixmap("simulation.png")
        picture.setPixmap(
            image.scaled(440, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        picture.setAlignment(Qt.AlignCenter)
        layout.addWidget(picture)

        description = QLabel(
            "A heat transfer simulation between two bodies"
        )
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)

        name = QLabel("Created by: Hof Moscow")
        name.setAlignment(Qt.AlignCenter)
        layout.addWidget(name)

        email = QLabel("Email: hmoscow1234@gmail.com")
        email.setAlignment(Qt.AlignCenter)
        layout.addWidget(email)

        github = QLabel(
            '<a href="https://github.com/hof-moscow/Heat-Transfer-Simulation">'
            'View project on GitHub</a>'
        )
        github.setOpenExternalLinks(True)
        github.setAlignment(Qt.AlignCenter)
        layout.addWidget(github)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())
