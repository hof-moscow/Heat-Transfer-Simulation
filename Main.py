from About import AboutWindow
from Graph import GraphWindow
from Body import Body
from PySide6.QtCore import QTimer
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QSlider, QDoubleSpinBox, QVBoxLayout,
    QHBoxLayout, QGroupBox,QMessageBox,QComboBox
)
from PySide6.QtCore import Qt


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()

        self.i_heat = 1.23
        self.time_step = 100
        self.elapsed_time = 0

        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_method)

        self.about_window = AboutWindow()
        self.graph_window = GraphWindow(self)
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

        left_layout.addWidget(QLabel("Material"))

        self.left_material = QComboBox()
        self.left_material.addItems([
            "Custom", "Aluminum", "Copper", "Steel"
        ])
        self.left_material.currentTextChanged.connect(
            self.left_material_changed
        )
        left_layout.addWidget(self.left_material)


        left_layout.addWidget(QLabel("Heat Capacity"))
        self.left_capacity = QDoubleSpinBox()
        self.left_capacity.setRange(1, 5000)
        self.left_capacity.setValue(490)
        self.left_capacity.setSuffix(" J/kg°C")
        left_layout.addWidget(self.left_capacity)

        left_group.setLayout(left_layout)
        bodies_layout.addWidget(left_group)


        controls = QVBoxLayout()

        controls.addWidget(QLabel("Conductivity"))
        self.conductivity = QDoubleSpinBox()
        self.conductivity.setRange(0.01, 1000)
        self.conductivity.setValue(self.i_heat)
        self.conductivity.setSuffix(" J/s°C")
        controls.addWidget(self.conductivity)

        controls.addStretch()

        self.start_button = QPushButton("Start")
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.start_stop_button_method)
        controls.addWidget(self.start_button)

        self.graph_button = QPushButton("Graphs")
        self.graph_button.clicked.connect(self.graph_window.show)
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

        right_layout.addWidget(QLabel("Material"))

        self.right_material = QComboBox()
        self.right_material.addItems([
            "Custom", "Aluminum", "Copper", "Steel"
        ])
        self.right_material.currentTextChanged.connect(
            self.right_material_changed
        )
        right_layout.addWidget(self.right_material)

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

    def start_stop_button_method(self):
        if self.start_button.isChecked():
            self.body1 = Body(
                self.left_mass.value(),
                self.left_capacity.value(),
                self.left_slider.value()
            )

            self.body2 = Body(
                self.right_mass.value(),
                self.right_capacity.value(),
                self.right_slider.value()
            )

            self.elapsed_time = 0
            self.time_history = [0]
            self.body1_temp_history = [self.body1.temperature]
            self.body2_temp_history = [self.body2.temperature]

            self.start_button.setText("Stop")
            self.left_slider.setEnabled(False)
            self.right_slider.setEnabled(False)

            self.timer.start(100)

        else:
            self.timer.stop()
            self.start_button.setText("Start")
            self.left_slider.setEnabled(True)
            self.right_slider.setEnabled(True)

    def timer_method(self):

        sigma = self.conductivity.value()

        heat_flow = sigma * (
            self.body2.temperature - self.body1.temperature
        )

        max_step = 0.9 / (
            sigma * (
                1 / (self.body1.mass * self.body1.heat_capacity)
                + 1 / (self.body2.mass * self.body2.heat_capacity)
            )
        )

        dt = min(self.time_step, max_step)

        heat1 = heat_flow * dt
        heat2 = -heat1


        temp1 = self.body1.add_heat(heat1)
        temp2 = self.body2.add_heat(heat2)

        self.elapsed_time = self.elapsed_time + dt

        self.time_history.append(self.elapsed_time)
        self.body1_temp_history.append(temp1)
        self.body2_temp_history.append(temp2)

        self.left_slider.setValue(round(temp1))
        self.right_slider.setValue(round(temp2))

        self.left_temperature_changed(temp1)
        self.right_temperature_changed(temp2)

        if abs(temp1 - temp2) <= 0.1:
            self.timer.stop()
            self.start_button.setChecked(False)
            self.start_button.setText("Start")

            self.left_slider.setEnabled(True)
            self.right_slider.setEnabled(True)

            QMessageBox.information(
                self,
                "Simulation Complete",
                "Thermal equilibrium reached!"
            )

    def left_material_changed(self, material):
        capacities = {
            "Aluminum": 900,
            "Copper": 385,
            "Steel": 490
        }

        if material == "Custom":
            self.left_capacity.setEnabled(True)
        else:
            self.left_capacity.setValue(capacities[material])
            self.left_capacity.setEnabled(False)

    def right_material_changed(self, material):
        capacities = {
            "Aluminum": 900,
            "Copper": 385,
            "Steel": 490
        }

        if material == "Custom":
            self.right_capacity.setEnabled(True)
        else:
            self.right_capacity.setValue(capacities[material])
            self.right_capacity.setEnabled(False)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatTransfer()
    window.show()
    app.exec()
