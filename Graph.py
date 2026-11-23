
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
        self.draw_button.clicked.connect(self.draw_graph)
        controls.addWidget(self.draw_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_graph)
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
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)

        self.ax.set_title("Heat Transfer")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True)

        self.canvas.draw()


    def draw_graph(self):
        if self.main_window.time_history:
            times = self.main_window.time_history

            if self.body_combo.currentText() == "Body 1":
                temperatures = self.main_window.body1_temp_history
                self.ax.plot(times, temperatures, color="red", label="Body 1")

            else:
                temperatures = self.main_window.body2_temp_history
                self.ax.plot(times, temperatures, color="blue", label="Body 2")

            self.ax.legend()
            self.canvas.draw()
            
    def clear_graph(self):
        self.setup_graph()
