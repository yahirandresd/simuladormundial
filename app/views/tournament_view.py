import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, \
    QFileDialog, QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QInputDialog, QAbstractItemView
import  os
from PyQt5.QtGui import QRegExpValidator, QFont, QIntValidator, QIcon
from app.model.match import Match
from app.model.tournament import Tournament
from app.model.team import Team


class TournamentView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Copa Mundial de la FIFA 2026")
        self.tablas_por_grupo = {}
        self.nombre_equipo = QLineEdit()
        self.resistencia = QLineEdit()
        self.fuerza = QLineEdit()
        self.velocidad = QLineEdit()
        self.plantilla = ""
        self.nombre_archivo_label = QLineEdit()
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
        self.boton_ingresar = QPushButton("Ingresar Equipo")
        self.boton_ingresar.clicked.connect(self.ingresar_datos)
        self.boton_ingresar.setFont(font)
        self.boton_simular_fecha = QPushButton("Simular Fecha")
        self.boton_simular_fecha.clicked.connect(self.simular_fecha)
        self.boton_simular_fecha.setEnabled(False)
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
        label_plantilla = QLabel("Plantilla jugadores", font=font)
        botones_layout.addWidget(self.boton_cargar)
        botones_layout.addWidget(self.boton_ingresar)
        layout_left.addLayout(layout)
        layout_left.addWidget(label_plantilla)
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
            self.plantilla = os.path.basename(archivo)
            self.nombre_archivo_label.setText(self.plantilla)
            with open(archivo, "r", encoding="utf-8") as file:  # Especificar encoding utf-8
                contenido = file.read()
                self.info_texto.setText(contenido)

    def ingresar_datos(self):
        self.controller.ingresar_datos(self, self.plantilla)
        self.limpiar_campos()


        # Verificar si se alcanzó el límite de 4 equipos en el grupo seleccionado
        grupo_seleccionado = self.lista_grupo.currentText()
        tabla_grupo = self.tablas_por_grupo.get(grupo_seleccionado)
        if tabla_grupo and tabla_grupo.rowCount() <= 2:
            self.boton_simular_fecha.setEnabled(True)  # Activar el botón si hay 4 equipos en el grupo
        else:
            self.boton_simular_fecha.setEnabled(True)

    def limpiar_campos(self):
        self.nombre_equipo.clear()
        self.resistencia.clear()
        self.fuerza.clear()
        self.velocidad.clear()
        self.lista_precision.setCurrentIndex(0)
        self.lista_grupo.setCurrentIndex(0)
        self.plantilla = None
        self.info_texto.clear()

    def simular_fecha(self):
        opciones_criterio = ["Resistencia", "Velocidad", "Fuerza", "Precisión"]
        criterio, ok = QInputDialog.getItem(self, "Seleccionar Criterio", "Selecciona un criterio:", opciones_criterio)

        if ok:
            # Obtener el grupo seleccionado
            grupo_seleccionado = self.lista_grupo.currentText()

            # Obtener la tabla del grupo seleccionado
            tabla_grupo = self.tablas_por_grupo.get(grupo_seleccionado)

            if not tabla_grupo or tabla_grupo.rowCount() < 2:
                QMessageBox.warning(self, "Grupo incompleto", "El grupo seleccionado no tiene suficientes equipos para simular una fecha.")
                return

            # Obtener equipos del grupo seleccionado
            equipos_grupo = [tabla_grupo.item(fila, 0).text() for fila in range(tabla_grupo.rowCount())]

            # Jugar partidos entre equipos del mismo grupo
            for i in range(len(equipos_grupo)):
                for j in range(i+1, len(equipos_grupo)):
                    equipo1_nombre = equipos_grupo[i]
                    equipo2_nombre = equipos_grupo[j]

                    equipo1 = self.controller.get_equipo_por_nombre(equipo1_nombre)
                    equipo2 = self.controller.get_equipo_por_nombre(equipo2_nombre)

                    partido = Match(equipo1, equipo2, criterio)
                    partido.jugar_partido()

                    # Actualizar la tabla con los resultados del partido
                    # (Suponiendo que tienes un método para actualizar la tabla)
                    self.actualizar_tabla_resultados(partido)

    def actualizar_tabla_resultados(self, partido):
        equipo1_nombre = partido.equipo1.nombre
        equipo2_nombre = partido.equipo2.nombre

        # Encontrar la tabla correspondiente al grupo de los equipos
        grupo = partido.equipo1.grupo
        tabla_grupo = self.tablas_por_grupo.get(grupo)

        if tabla_grupo:
            # Encontrar las filas correspondientes a los equipos en la tabla
            equipo1_row = -1
            equipo2_row = -1
            for row in range(tabla_grupo.rowCount()):
                if tabla_grupo.item(row, 0).text() == equipo1_nombre:
                    equipo1_row = row
                elif tabla_grupo.item(row, 0).text() == equipo2_nombre:
                    equipo2_row = row

            # Actualizar la tabla con los resultados del partido
            if equipo1_row != -1 and equipo2_row != -1:
                #Actualiza el GF y GC
                tabla_grupo.setItem(equipo1_row, 5, QTableWidgetItem(str(partido.equipo1.ga)))  # GF equipo1
                tabla_grupo.setItem(equipo1_row, 6, QTableWidgetItem(str(partido.equipo1.ge)))  # GC equipo1
                tabla_grupo.setItem(equipo2_row, 5, QTableWidgetItem(str(partido.equipo2.ga)))  # GF equipo2
                tabla_grupo.setItem(equipo2_row, 6, QTableWidgetItem(str(partido.equipo2.ge)))  # GC equipo2
                #Actualiza PJ y PG, PE, PP
                tabla_grupo.setItem(equipo1_row, 1, QTableWidgetItem(str(partido.equipo1.pj)))  # GF equipo1
                tabla_grupo.setItem(equipo1_row, 2, QTableWidgetItem(str(partido.equipo1.pg)))  # GC equipo1
                tabla_grupo.setItem(equipo2_row, 1, QTableWidgetItem(str(partido.equipo2.pj)))  # GF equipo2
                tabla_grupo.setItem(equipo2_row, 2, QTableWidgetItem(str(partido.equipo2.pg)))  # GC equipo2
