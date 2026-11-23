import sys
import os
import subprocess
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QComboBox,QFileDialog, QMessageBox,
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
        self.export_button.clicked.connect(self.export_csv)
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

    def export_csv(self):
        if not self.main_window.time_history:
            QMessageBox.information(self, "No Data", "Run a simulation first.")
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Simulation Data", "heat_transfer.csv",
            "CSV Files (*.csv)"
        )

        if file_name:
            if not file_name.lower().endswith(".csv"):
                file_name = file_name + ".csv"

            with open(file_name, "w", encoding="utf-8-sig") as f:
                f.write("Time (s),Body 1 Temperature (C),Body 2 Temperature (C)\n")

                for i in range(len(self.main_window.time_history)):
                    time = self.main_window.time_history[i]
                    temp1 = self.main_window.body1_temp_history[i]
                    temp2 = self.main_window.body2_temp_history[i]

                    f.write(f"{time:.2f},{temp1:.2f},{temp2:.2f}\n")

            if sys.platform == "win32":
                os.startfile(file_name)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", file_name])
            else:
                subprocess.Popen(["xdg-open", file_name])

