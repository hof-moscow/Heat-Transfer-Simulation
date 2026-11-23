
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class GraphWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer - Graphs")
        self.resize(850, 550)

        main_layout = QHBoxLayout()

        graph_layout = QVBoxLayout()

        title = QLabel("Temperature vs Time")
        title.setObjectName("mainTitle")
        graph_layout.addWidget(title)

        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)

        main_layout.addLayout(graph_layout)

        controls = QVBoxLayout()

        controls.addWidget(QLabel("Select Body"))

        self.body_combo = QComboBox()
        self.body_combo.addItems(["Body 1", "Body 2"])
        controls.addWidget(self.body_combo)

        self.draw_button = QPushButton("Draw")
        controls.addWidget(self.draw_button)

        self.clear_button = QPushButton("Clear")
        controls.addWidget(self.clear_button)

        self.export_button = QPushButton("Export to CSV")
        controls.addWidget(self.export_button)

        controls.addStretch()

        main_layout.addLayout(controls)
        self.setLayout(main_layout)

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.setup_graph()

    def setup_graph(self):
        ax = self.figure.add_subplot(111)
        ax.set_title("Heat Transfer")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Temperature (°C)")
        ax.grid(True)
        self.canvas.draw()
