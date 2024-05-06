import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, \
    QFileDialog, QTextEdit, QTableWidgetItem, QMessageBox, QTabWidget, QInputDialog
import  os
from PyQt5.QtGui import QFont, QIntValidator
from app.model.match import Match
from app.controllers.tournament_controller import TournamentController
from app.model.team import Team


class TournamentView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Copa Mundial de la FIFA 2026")
        self.tablas_por_grupo = {}
        self.jornada_actual = 0
        self.nombre_equipo = QLineEdit()
        self.resistencia = QLineEdit()
        self.fuerza = QLineEdit()
        self.velocidad = QLineEdit()
        self.plantilla = "*ningun archivo*"
        self.font = QFont()
        self.font.setPointSize(14)
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
        self.boton_simular_fecha.setEnabled(True)
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
        # Dentro del método __init__ de tu TournamentView
        self.boton_llenar_desde_csv = QPushButton("Llenar desde CSV")
        self.boton_llenar_desde_csv.clicked.connect(self.llenar_desde_csv)
        layout_left.addWidget(self.boton_llenar_desde_csv)
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
        # Verificar si todos los campos están completos
        if not self.nombre_equipo.text() or not self.resistencia.text() or not self.fuerza.text() or not self.velocidad.text():
            QMessageBox.warning(self, "Campos incompletos", "Por favor completa todos los campos.")
            return

        try:
            # Convertir los valores de resistencia, fuerza y velocidad a enteros
            resistencia = int(self.resistencia.text())
            fuerza = int(self.fuerza.text())
            velocidad = int(self.velocidad.text())
        except ValueError:
            QMessageBox.warning(self, "Formato inválido", "Por favor ingresa valores numéricos válidos para resistencia, fuerza y velocidad.")
            return

        # Continuar con el proceso de ingreso de datos
        self.controller.ingresar_datos(self, self.plantilla)
        self.limpiar_campos()

        # Verificar si se alcanzó el límite de 4 equipos en el grupo seleccionado
        grupo_seleccionado = self.lista_grupo.currentText()
        tabla_grupo = self.tablas_por_grupo.get(grupo_seleccionado)
        """if tabla_grupo and tabla_grupo.rowCount() < 4:
            self.boton_simular_fecha.setEnabled(True)  # Activar el botón si hay 4 equipos en el grupo
        else:
            self.boton_simular_fecha.setEnabled(True)"""
        

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
            # Incrementamos la jornada actual
            self.jornada_actual += 1

            # Obtener el grupo seleccionado
            grupo_seleccionado = self.lista_grupo.currentText()

            # Obtener la tabla del grupo seleccionado
            tabla_grupo = self.tablas_por_grupo.get(grupo_seleccionado)

            if not tabla_grupo or tabla_grupo.rowCount() < 2:
                self.jornada_actual -= 1
                QMessageBox.warning(self, "Grupo incompleto", "El grupo seleccionado no tiene suficientes equipos para simular una fecha.")
                return

            # Obtener equipos del grupo seleccionado
            equipos_grupo = [tabla_grupo.item(fila, 0).text() for fila in range(tabla_grupo.rowCount())]

            # Definir los emparejamientos de esta jornada según el patrón que has mencionado
            if self.jornada_actual == 1:
                partidos_jornada = [(equipos_grupo[0], equipos_grupo[1]), (equipos_grupo[2], equipos_grupo[3])]
            elif self.jornada_actual == 2:
                partidos_jornada = [(equipos_grupo[0], equipos_grupo[3]), (equipos_grupo[1], equipos_grupo[2])]
            elif self.jornada_actual == 3:
                partidos_jornada = [(equipos_grupo[0], equipos_grupo[2]), (equipos_grupo[1], equipos_grupo[3])]
            else:
                QMessageBox.warning(self, "Fin de las jornadas", "Se han simulado todas las jornadas.")
                return

            resultados_jornada = []

            # Jugar los partidos de la jornada
            for partido_info in partidos_jornada:
                equipo1_nombre, equipo2_nombre = partido_info
                equipo1 = self.controller.get_equipo_por_nombre(equipo1_nombre)
                equipo2 = self.controller.get_equipo_por_nombre(equipo2_nombre)
                partido = Match(equipo1, equipo2, criterio)
                partido.jugar_partido()
                resultado_partido = f"{partido.goles_equipo1} - {partido.goles_equipo2}"
                resultados_jornada.append({'equipo1': equipo1_nombre, 'equipo2': equipo2_nombre, 'resultado': resultado_partido})
                self.actualizar_tabla_resultados(partido)

            # Mostrar los resultados de la jornada en el QTextEdit
            self.mostrar_resultados_jornada(self.jornada_actual, resultados_jornada)


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