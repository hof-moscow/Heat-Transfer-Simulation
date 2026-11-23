from About import AboutWindow
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QSlider, QDoubleSpinBox, QVBoxLayout,
    QHBoxLayout, QGroupBox
)
from PySide6.QtCore import Qt


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.about_window = AboutWindow()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer Simulation")
        self.resize(950, 520)

        main_layout = QVBoxLayout()

        title = QLabel("Heat Transfer Simulation")
        title.setObjectName("mainTitle")
        main_layout.addWidget(title)

        bodies_layout = QHBoxLayout()


        left_group = QGroupBox("Body 1")
        left_layout = QVBoxLayout()

        self.left_slider = QSlider(Qt.Vertical)
        self.left_slider.setRange(0, 200)
        self.left_slider.setValue(200)
        self.left_slider.valueChanged.connect(self.left_temperature_changed)

        self.left_body = QLabel("BODY 1")
        self.left_body.setObjectName("hotBody")
        self.left_body.setAlignment(Qt.AlignCenter)
        self.left_body.setFixedSize(165, 190)

        left_visual = QHBoxLayout()
        left_visual.addWidget(self.left_slider)
        left_visual.addWidget(self.left_body)
        left_layout.addLayout(left_visual)

        self.left_temperature = QLabel("Temperature: 200.0 °C")
        left_layout.addWidget(self.left_temperature)

        left_layout.addWidget(QLabel("Mass"))
        self.left_mass = QDoubleSpinBox()
        self.left_mass.setRange(0.01, 10000)
        self.left_mass.setValue(10)
        self.left_mass.setSuffix(" kg")
        left_layout.addWidget(self.left_mass)

        left_layout.addWidget(QLabel("Heat Capacity"))
        self.left_capacity = QDoubleSpinBox()
        self.left_capacity.setRange(0.01, 1000)
        self.left_capacity.setValue(0.40)
        self.left_capacity.setSuffix(" J/kg°C")
        left_layout.addWidget(self.left_capacity)

        left_group.setLayout(left_layout)
        bodies_layout.addWidget(left_group)


        controls = QVBoxLayout()

        controls.addWidget(QLabel("Conductivity"))
        self.conductivity = QDoubleSpinBox()
        self.conductivity.setRange(0.01, 1000)
        self.conductivity.setValue(1.00)
        self.conductivity.setSuffix(" J/s°C")
        controls.addWidget(self.conductivity)

        controls.addStretch()

        self.start_button = QPushButton("Start")
        self.start_button.setCheckable(True)
        controls.addWidget(self.start_button)

        self.graph_button = QPushButton("Graphs")
        controls.addWidget(self.graph_button)

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.about_window.show)
        controls.addWidget(self.about_button)

        controls.addStretch()
        bodies_layout.addLayout(controls)


        right_group = QGroupBox("Body 2")
        right_layout = QVBoxLayout()

        self.right_slider = QSlider(Qt.Vertical)
        self.right_slider.setRange(0, 200)
        self.right_slider.setValue(0)
        self.right_slider.valueChanged.connect(self.right_temperature_changed)

        self.right_body = QLabel("BODY 2")
        self.right_body.setObjectName("coldBody")
        self.right_body.setAlignment(Qt.AlignCenter)
        self.right_body.setFixedSize(165, 190)

        right_visual = QHBoxLayout()
        right_visual.addWidget(self.right_body)
        right_visual.addWidget(self.right_slider)
        right_layout.addLayout(right_visual)

        self.right_temperature = QLabel("Temperature: 0.0 °C")
        right_layout.addWidget(self.right_temperature)

        right_layout.addWidget(QLabel("Mass"))
        self.right_mass = QDoubleSpinBox()
        self.right_mass.setRange(0.01, 10000)
        self.right_mass.setValue(10)
        self.right_mass.setSuffix(" kg")
        right_layout.addWidget(self.right_mass)

        right_layout.addWidget(QLabel("Heat Capacity"))
        self.right_capacity = QDoubleSpinBox()
        self.right_capacity.setRange(0.01, 1000)
        self.right_capacity.setValue(0.40)
        self.right_capacity.setSuffix(" J/kg°C")
        right_layout.addWidget(self.right_capacity)

        right_group.setLayout(right_layout)
        bodies_layout.addWidget(right_group)

        main_layout.addLayout(bodies_layout)
        self.setLayout(main_layout)

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

    def left_temperature_changed(self, value):
        self.left_temperature.setText(f"Temperature: {value:.1f} °C")

        red = int(value * 255 / 200)
        self.left_body.setStyleSheet(
            f"background-color: rgb({red}, 0, 0); color: white;"
        )

    def right_temperature_changed(self, value):
        self.right_temperature.setText(f"Temperature: {value:.1f} °C")

        red = int(value * 255 / 200)
        self.right_body.setStyleSheet(
            f"background-color: rgb({red}, 0, 0); color: white;"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatTransfer()
    window.show()
    app.exec()
