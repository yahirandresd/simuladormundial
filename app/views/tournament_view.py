from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, \
    QFileDialog, QTextEdit, QTableWidgetItem, QMessageBox, QTabWidget, QInputDialog, QDialog
import  os
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QIntValidator, QColor
from app.model.match import Match
from app.controllers.tournament_controller import TournamentController
from app.model.team import *
from app.views.arbol import Arbol


class TournamentView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Copa Mundial de la FIFA 2026")
        self.tablas_por_grupo = {}
        self.jornada_actual = 0
        self.equipo = 0
        self.nombre_equipo = QLineEdit()
        self.resistencia = QLineEdit()
        self.fuerza = QLineEdit()
        self.velocidad = QLineEdit()
        self.plantilla = "*ningun archivo*"
        self.jornadas_por_grupo = {"Grupo A": 0, "Grupo B": 0, "Grupo C": 0, "Grupo D": 0,
                                   "Grupo E": 0, "Grupo F": 0, "Grupo G": 0, "Grupo H": 0}
        self.max_jornadas = 3  # Cantidad total de jornadas por grupo
        self.font = QFont()
        self.font.setPointSize(12)
        fontA = QFont("Arial", 18, QFont.Bold)
        self.nombre_equipo.setFont(self.font)
        self.resistencia.setFont(self.font)
        self.fuerza.setFont(self.font)
        self.velocidad.setFont(self.font)
        self.lista_precision = QComboBox()
        self.lista_precision.addItems(["Alto", "Medio", "Bajo"])
        self.lista_precision.setFont(self.font)
        self.lista_grupo = QComboBox()
        self.lista_grupo.addItems(["Grupo A", "Grupo B", "Grupo C", "Grupo D",
                                   "Grupo E", "Grupo F", "Grupo G", "Grupo H"])
        self.lista_grupo.setFont(self.font)
        self.boton_cargar = QPushButton("Cargar archivo")
        self.boton_cargar.clicked.connect(self.cargar_archivo)
        self.boton_cargar.setFont(self.font)
        self.boton_ingresar = QPushButton("Ingresar Equipo")
        self.boton_ingresar.clicked.connect(self.ingresar_datos)
        self.boton_ingresar.setFont(self.font)
        self.boton_simular_fecha = QPushButton("Simular Fecha")
        self.boton_simular_fecha.clicked.connect(self.simular_fecha)
        self.boton_simular_fecha.setEnabled(False)
        self.boton_simular_fecha.setFont(self.font)
        self.info_texto = QTextEdit()
        self.info_texto.setReadOnly(True)
        self.info_texto.setFont(self.font)
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(self.font)
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nombre del equipo:", font=self.font))
        layout.addWidget(self.nombre_equipo)
        layout.addWidget(QLabel("Resistencia:", font=self.font))
        layout.addWidget(self.resistencia)
        layout.addWidget(QLabel("Fuerza:", font=self.font))
        layout.addWidget(self.fuerza)
        layout.addWidget(QLabel("Velocidad:", font=self.font))
        layout.addWidget(self.velocidad)
        layout.addWidget(QLabel("Precisión:", font=self.font))
        layout.addWidget(self.lista_precision)
        layout.addWidget(QLabel("Grupo:", font=self.font))
        layout.addWidget(self.lista_grupo)
        layout.addStretch()
        botones_layout = QHBoxLayout()
        self.label_plantilla = QLabel(f"Plantilla jugadores: {self.plantilla}", font=self.font)
        botones_layout.addWidget(self.boton_cargar)
        botones_layout.addWidget(self.boton_ingresar)
        layout_left.addLayout(layout)
        layout_left.addWidget(self.label_plantilla)
        layout_left.addLayout(botones_layout)
        layout_right.addWidget(self.boton_simular_fecha)
        layout_right.addWidget(self.info_texto)
        layout_right.addWidget(self.tab_widget)
        main_layout = QHBoxLayout()
        main_layout.addLayout(layout_left)
        main_layout.addLayout(layout_right)
        self.setLayout(main_layout)
        # Boton Bonito
        self.boton_llenar_desde_csv = QPushButton("Llenar desde CSV")
        color_azul_bonito = QColor(50, 100, 200)  # Por ejemplo, un azul bonito
        self.boton_llenar_desde_csv.setStyleSheet("background-color: " + color_azul_bonito.name() + "; color: white; border-radius: 20px;")
        
        self.boton_llenar_desde_csv.setFont(fontA)
        self.boton_llenar_desde_csv.clicked.connect(self.llenar_desde_csv)
        layout_left.addWidget(self.boton_llenar_desde_csv)
        #TAMAÑO
        # Ajustar el tamaño de los elementos de entrada y botones
        self.nombre_equipo.setMaximumWidth(220)
        self.resistencia.setMaximumWidth(220)
        self.fuerza.setMaximumWidth(220)
        self.velocidad.setMaximumWidth(220)
        self.lista_precision.setMaximumWidth(220)
        self.lista_grupo.setMaximumWidth(220)
        # Ajustar el tamaño de los botones
        self.boton_cargar.setMaximumWidth(150)
        self.boton_ingresar.setMaximumWidth(150)
        ##########################################
        self.resistencia.setValidator(QIntValidator(0, 99, self))
        self.fuerza.setValidator(QIntValidator(0, 99, self))
        self.velocidad.setValidator(QIntValidator(0, 99, self))
        self.controller = TournamentController(self.tablas_por_grupo)

    def cargar_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivos CSV (*.csv)")
        if archivo:
            self.plantilla = os.path.basename(archivo)
            self.label_plantilla.setText(f"Plantilla jugadores: {self.plantilla}") 

    def ingresar_datos(self):
        self.equipo += 1 
        # Verificar si todos los campos están completos
        if not self.nombre_equipo.text() or not self.resistencia.text() or not self.fuerza.text() or not self.velocidad.text() or self.plantilla == "*ningun archivo*":
            QMessageBox.warning(self, "Campos incompletos", "Por favor completa todos los campos.")
            self.equipo -= 1
            return
        self.boton_llenar_desde_csv.setEnabled(False)
        
        print(self.equipo)
        if self.equipo > 3:
            self.boton_simular_fecha.setEnabled(True)

        # Continuar con el proceso de ingreso de datos
        self.controller.ingresar_datos(self, self.plantilla)
        self.limpiar_campos()
        
        
    def limpiar_campos(self):
        self.nombre_equipo.clear()
        self.resistencia.clear()
        self.fuerza.clear()
        self.velocidad.clear()
        self.lista_precision.setCurrentIndex(0)
        self.lista_grupo.setCurrentIndex(0)
        self.info_texto.clear()
        self.label_plantilla.setText(f"Plantilla jugadores: *ningun archivo* ")   

    def mostrar_resultados_jornada(self, jornada, resultados):
        texto = f"Jornada {jornada}\n"
        for resultado in resultados:
            equipo1_nombre = resultado['equipo1']
            equipo2_nombre = resultado['equipo2']
            resultado_partido = resultado['resultado']

            texto += f"{equipo1_nombre} vs {equipo2_nombre}: {resultado_partido}\n"

        # Mostrar en el QTextEdit
        self.info_texto.append(texto)

    def simular_fecha(self):
        opciones_criterio = ["Resistencia", "Velocidad", "Fuerza", "Precisión"]
        criterio, ok = QInputDialog.getItem(self, "Seleccionar Criterio", "Selecciona un criterio:", opciones_criterio, editable=False)

        if ok:
            resultados_totales = []

            for grupo, jornada_actual in self.jornadas_por_grupo.items():
                if jornada_actual >= self.max_jornadas:
                    continue  # Si ya se han simulado todas las jornadas para este grupo, pasamos al siguiente

                jornada_actual += 1  # Incrementamos la jornada actual para este grupo
                self.jornadas_por_grupo[grupo] = jornada_actual

                tabla_grupo = self.tablas_por_grupo.get(grupo)
                equipos_grupo = [tabla_grupo.item(fila, 0).text() for fila in range(tabla_grupo.rowCount())]

                if jornada_actual == 1:
                    partidos_jornada = [(equipos_grupo[0], equipos_grupo[1]), (equipos_grupo[2], equipos_grupo[3])]
                elif jornada_actual == 2:
                    partidos_jornada = [(equipos_grupo[0], equipos_grupo[3]), (equipos_grupo[1], equipos_grupo[2])]
                elif jornada_actual == 3:
                    partidos_jornada = [(equipos_grupo[0], equipos_grupo[2]), (equipos_grupo[1], equipos_grupo[3])]
                
                if jornada_actual == self.max_jornadas:  # Comprueba si es la última fecha
                    # Ordenar la tabla después de la última jornada
                    for grupo in self.tablas_por_grupo.values():
                        grupo.sortItems(7, QtCore.Qt.DescendingOrder)
                    self.boton_simular_fecha.setEnabled(False)  # Cambia el texto del botón
                    self.abrir_nueva_interfaz()
                    

                resultados_jornada = []

                for partido_info in partidos_jornada:
                    equipo1_nombre, equipo2_nombre = partido_info
                    equipo1 = self.controller.get_equipo_por_nombre(equipo1_nombre)
                    equipo2 = self.controller.get_equipo_por_nombre(equipo2_nombre)
                    partido = Match(equipo1, equipo2, criterio)
                    partido.jugar_partido()
                    resultado_partido = f"{partido.goles_equipo1} - {partido.goles_equipo2}"
                    resultados_jornada.append({'equipo1': equipo1_nombre, 'equipo2': equipo2_nombre, 'resultado': resultado_partido})
                    self.actualizar_tabla_resultados(partido)

                resultados_totales.extend(resultados_jornada)

            # Mostrar los resultados totales
            self.mostrar_resultados_jornada(jornada_actual, resultados_totales)

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
                #Actualiza PJ, PG, PE y PP
                tabla_grupo.setItem(equipo1_row, 1, QTableWidgetItem(str(partido.equipo1.pj)))  # PJ equipo1
                tabla_grupo.setItem(equipo1_row, 2, QTableWidgetItem(str(partido.equipo1.pg)))  # PG
                tabla_grupo.setItem(equipo1_row, 3, QTableWidgetItem(str(partido.equipo1.pe)))  # PE
                tabla_grupo.setItem(equipo1_row, 4, QTableWidgetItem(str(partido.equipo1.pp)))  # PP

                tabla_grupo.setItem(equipo2_row, 1, QTableWidgetItem(str(partido.equipo2.pj)))  # PJ equipo2
                tabla_grupo.setItem(equipo2_row, 2, QTableWidgetItem(str(partido.equipo2.pg)))  # PG
                tabla_grupo.setItem(equipo2_row, 3, QTableWidgetItem(str(partido.equipo2.pe)))  # PE
                tabla_grupo.setItem(equipo2_row, 4, QTableWidgetItem(str(partido.equipo2.pp)))  # PP
                #Actualiza el GF y GC
                tabla_grupo.setItem(equipo1_row, 5, QTableWidgetItem(str(partido.equipo1.ga)))  # GF equipo1
                tabla_grupo.setItem(equipo1_row, 6, QTableWidgetItem(str(partido.equipo1.ge)))  # GC equipo1
                tabla_grupo.setItem(equipo2_row, 5, QTableWidgetItem(str(partido.equipo2.ga)))  # GF equipo2
                tabla_grupo.setItem(equipo2_row, 6, QTableWidgetItem(str(partido.equipo2.ge)))  # GC equipo2
                #Actualiza Puntos
                tabla_grupo.setItem(equipo1_row, 7, QTableWidgetItem(str(partido.equipo1.puntos)))  # Puntos equipo1
                tabla_grupo.setItem(equipo2_row, 7, QTableWidgetItem(str(partido.equipo2.puntos)))  # Puntos equipo2
                    
    # Dentro del método llenar_desde_csv de tu TournamentView
    def llenar_desde_csv(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivos CSV (*.csv)")
        if archivo:
            self.controller.llenar_grupos_desde_csv(self, archivo)
            self.boton_ingresar.setEnabled(False)
            self.boton_simular_fecha.setEnabled(True)
            
    def abrir_nueva_interfaz(self):
        # Obtener los dos equipos con más puntos de cada grupo
        equipos_calificados = []
        for grupo, tabla_grupo in self.tablas_por_grupo.items():
            # Ordenar la tabla por puntos (columna 7)
            tabla_grupo.sortItems(7, QtCore.Qt.DescendingOrder)
            equipo1_nombre = tabla_grupo.item(0, 0).text()
            equipo2_nombre = tabla_grupo.item(1, 0).text()
            equipos_calificados.append((equipo1_nombre, equipo2_nombre))

        # Crear la interfaz del cuadro de eliminación y pasar los equipos calificados como argumento
        self.arbol_widget = Arbol(equipos_calificados)
        print(equipos_calificados)
        # Agregar el widget Arbol al layout principal de TournamentView
        self.arbol_widget.show()