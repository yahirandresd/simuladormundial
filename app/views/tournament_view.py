import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, \
    QFileDialog, QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QFont, QIntValidator
from app.model.team import Team


class TournamentView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Equipos de Fútbol")

        # Diccionario para almacenar las tablas de equipos por grupo
        self.tablas_por_grupo = {}

        # Widgets para ingresar datos del equipo
        self.nombre_equipo = QLineEdit()
        self.resistencia = QLineEdit()
        self.fuerza = QLineEdit()
        self.velocidad = QLineEdit()

        # Establecer un tamaño de fuente más grande para los widgets de entrada de texto
        font = QFont()
        font.setPointSize(14)
        self.nombre_equipo.setFont(font)
        self.resistencia.setFont(font)
        self.fuerza.setFont(font)
        self.velocidad.setFont(font)

        # Lista desplegable para precisión, criterio y grupo
        self.lista_precision = QComboBox()
        self.lista_precision.addItems(["Alto", "Medio", "Bajo"])
        self.lista_precision.setFont(font)

        self.lista_criterio = QComboBox()
        self.lista_criterio.addItems(["Resistencia", "Velocidad", "Fuerza", "Precisión"])
        self.lista_criterio.setFont(font)

        self.lista_grupo = QComboBox()
        self.lista_grupo.addItems(["Grupo A", "Grupo B", "Grupo C", "Grupo D",
                                   "Grupo E", "Grupo F", "Grupo G", "Grupo H"])
        self.lista_grupo.setFont(font)

        # Botones para cargar, ingresar datos y simular fecha
        self.boton_cargar = QPushButton("Cargar archivo")
        self.boton_cargar.clicked.connect(self.cargar_archivo)
        self.boton_cargar.setFont(font)

        self.boton_ingresar = QPushButton("Ingresar")
        self.boton_ingresar.clicked.connect(self.ingresar_datos)
        self.boton_ingresar.setFont(font)

        self.boton_simular_fecha = QPushButton("Simular Fecha")
        self.boton_simular_fecha.clicked.connect(self.simular_fecha)
        self.boton_simular_fecha.setFont(font)

        # Widget para mostrar información
        self.info_texto = QTextEdit()
        self.info_texto.setReadOnly(True)
        self.info_texto.setFont(font)

        # TabWidget para organizar las tablas por grupo
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(font)

        # Configurar diseño
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
        layout.addWidget(QLabel("Criterio:", font=font))
        layout.addWidget(self.lista_criterio)
        layout.addWidget(QLabel("Grupo:", font=font))
        layout.addWidget(self.lista_grupo)

        layout.addStretch()

        layout_h = QHBoxLayout()
        layout_h.addWidget(self.boton_cargar)
        layout_h.addWidget(self.boton_ingresar)
        layout_h.addWidget(self.boton_simular_fecha)
        layout.addLayout(layout_h)

        layout.addWidget(self.info_texto)
        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

        # Configurar validadores para los campos de resistencia, fuerza y velocidad
        self.resistencia.setValidator(QIntValidator(0, 99, self))
        self.fuerza.setValidator(QIntValidator(0, 99, self))
        self.velocidad.setValidator(QIntValidator(0, 99, self))

    def cargar_archivo(self):
        # Aquí puedes agregar la lógica para cargar un archivo
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivos CSV (*.csv)")
        if archivo:
            with open(archivo, "r") as file:
                contenido = file.read()
                self.info_texto.setText(contenido)

    def ingresar_datos(self):
        # Obtener nombre, resistencia, fuerza y velocidad del equipo
        nombre = self.nombre_equipo.text()
        resistencia = self.resistencia.text()
        fuerza = self.fuerza.text()
        velocidad = self.velocidad.text()

        # Verificar si algún campo está vacío
        if not nombre or not resistencia or not fuerza or not velocidad:
            QMessageBox.warning(self, "Campos incompletos", "Por favor, complete todos los campos.")
            return

        # Verificar si el equipo ya está en el grupo seleccionado
        grupo = self.lista_grupo.currentText()
        tabla_grupo = self.tablas_por_grupo.get(grupo)
        if not tabla_grupo:
            tabla_grupo = QTableWidget()
            tabla_grupo.setColumnCount(8)
            tabla_grupo.setHorizontalHeaderLabels(["Equipo", "PJ", "PG", "PE", "PP", "GF", "GC", "Puntos"])
            self.tablas_por_grupo[grupo] = tabla_grupo
            self.tab_widget.addTab(tabla_grupo, grupo)

        equipos_grupo = [tabla_grupo.item(fila, 0).text() for fila in range(tabla_grupo.rowCount())]
        if nombre in equipos_grupo:
            QMessageBox.warning(self, "Equipo duplicado", "Este equipo ya está en el grupo {}.".format(grupo))
            return

        # Verificar si el equipo ya está en otro grupo
        for otro_grupo, otra_tabla in self.tablas_por_grupo.items():
            if otro_grupo != grupo and nombre in [otra_tabla.item(fila, 0).text() for fila in
                                                  range(otra_tabla.rowCount())]:
                QMessageBox.warning(self, "Equipo duplicado", "Este equipo ya está en el grupo {}.".format(otro_grupo))
                return

        # Si el equipo no está en ninguna tabla del grupo, continuar con la inserción
        fila = tabla_grupo.rowCount()
        if fila < 4:  # Máximo 4 equipos por grupo
            tabla_grupo.insertRow(fila)
            tabla_grupo.setItem(fila, 0, QTableWidgetItem(nombre))

            # Crear un objeto Team y guardar los datos en el archivo CSV
            equipo = Team(nombre, resistencia, fuerza, velocidad, self.lista_precision.currentText(), grupo)
            equipo.guardar_datos_csv()
        else:
            QMessageBox.warning(self, "Límite de equipos", "Ya hay 4 equipos en el grupo {}.".format(grupo))

    def simular_fecha(self):
        # Aquí puedes agregar la lógica para simular una fecha
        pass

