import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, \
    QFileDialog, QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QInputDialog
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QFont, QIntValidator, QIcon
from app.model.match import Match
from app.model.tournament import Tournament


class TournamentView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Copa Mundial de la FIFA 2026")
        self.tablas_por_grupo = {}
        self.nombre_equipo = QLineEdit()
        self.resistencia = QLineEdit()
        self.fuerza = QLineEdit()
        self.velocidad = QLineEdit()
        font = QFont()
        font.setPointSize(14)
        self.nombre_equipo.setFont(font)
        self.resistencia.setFont(font)
        self.fuerza.setFont(font)
        self.velocidad.setFont(font)
        self.lista_precision = QComboBox()
        self.lista_precision.addItems(["Alto", "Medio", "Bajo"])
        self.lista_precision.setFont(font)
        self.lista_grupo = QComboBox()
        self.lista_grupo.addItems(["Grupo A", "Grupo B", "Grupo C", "Grupo D",
                                   "Grupo E", "Grupo F", "Grupo G", "Grupo H"])
        self.lista_grupo.setFont(font)
        self.boton_cargar = QPushButton("Cargar archivo")
        self.boton_cargar.clicked.connect(self.cargar_archivo)
        self.boton_cargar.setFont(font)
        self.boton_ingresar = QPushButton("Ingresar")
        self.boton_ingresar.clicked.connect(self.ingresar_datos)
        self.boton_ingresar.setFont(font)
        self.boton_simular_fecha = QPushButton("Simular Fecha")
        self.boton_simular_fecha.clicked.connect(self.simular_fecha)
        self.boton_simular_fecha.setFont(font)
        self.info_texto = QTextEdit()
        self.info_texto.setReadOnly(True)
        self.info_texto.setFont(font)
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(font)
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nombre del equipo:", font=font))
        layout.addWidget(self.nombre_equipo)
        layout.addWidget(QLabel("Resistencia:", font=font))
        layout.addWidget(self.resistencia)
        layout.addWidget(QLabel("Fuerza:", font=font))
        layout.addWidget(self.fuerza)
        layout.addWidget(QLabel("Velocidad:", font=font))
        layout.addWidget(self.velocidad)
        layout.addWidget(QLabel("Precisión:", font=font))
        layout.addWidget(self.lista_precision)
        layout.addWidget(QLabel("Grupo:", font=font))
        layout.addWidget(self.lista_grupo)
        layout.addStretch()
        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.boton_cargar)
        botones_layout.addWidget(self.boton_ingresar)
        layout_left.addLayout(layout)
        layout_left.addLayout(botones_layout)
        layout_right.addWidget(self.boton_simular_fecha)
        layout_right.addWidget(self.info_texto)
        layout_right.addWidget(self.tab_widget)
        main_layout = QHBoxLayout()
        main_layout.addLayout(layout_left)
        main_layout.addLayout(layout_right)
        self.setLayout(main_layout)
        self.resistencia.setValidator(QIntValidator(0, 99, self))
        self.fuerza.setValidator(QIntValidator(0, 99, self))
        self.velocidad.setValidator(QIntValidator(0, 99, self))
        self.controller = Tournament(self.tablas_por_grupo)

    def cargar_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivos CSV (*.csv)")
        if archivo:
            with open(archivo, "r") as file:
                contenido = file.read()
                self.info_texto.setText(contenido)

    def ingresar_datos(self, pj=None):
        self.controller.ingresar_datos(self)

    def simular_fecha(self):
        opciones_criterio = ["Resistencia", "Velocidad", "Fuerza", "Precisión"]
        criterio, ok = QInputDialog.getItem(self, "Seleccionar Criterio", "Selecciona un criterio:", opciones_criterio)

        if ok:
            print("Se seleccionó el criterio:", criterio)