from PyQt5.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView
from app.model.team import Team
import csv

class TournamentController:
    def __init__(self, tablas_por_grupo):
        self.tablas_por_grupo = tablas_por_grupo
        self.equipos = {} 

    def get_equipo_por_nombre(self, nombre):
        return self.equipos.get(nombre)
    

    def ingresar_datos(self, view, plantilla):
        nombre = view.nombre_equipo.text()
        resistencia = int(view.resistencia.text())
        fuerza = int(view.fuerza.text())
        velocidad = int(view.velocidad.text())
        grupo = view.lista_grupo.currentText()

        tabla_grupo = self.tablas_por_grupo.get(grupo)
        if not tabla_grupo:
            tabla_grupo = QTableWidget()
            tabla_grupo.setColumnCount(8)
            tabla_grupo.setHorizontalHeaderLabels(["Equipo", "PJ", "PG", "PE", "PP", "GF", "GC", "Puntos"])
            tabla_grupo.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Esta línea deshabilita la edición de las celdas
            self.tablas_por_grupo[grupo] = tabla_grupo
            view.tab_widget.addTab(tabla_grupo, grupo)

        equipos_grupo = [tabla_grupo.item(fila, 0).text() for fila in range(tabla_grupo.rowCount())]
        if nombre in equipos_grupo:
            QMessageBox.warning(view, "Equipo duplicado", "Este equipo ya está en el grupo {}.".format(grupo))
            return

        for otro_grupo, otra_tabla in self.tablas_por_grupo.items():
            if otro_grupo != grupo and nombre in [otra_tabla.item(fila, 0).text() for fila in range(otra_tabla.rowCount())]:
                QMessageBox.warning(view, "Equipo duplicado", "Este equipo ya está en el grupo {}.".format(otro_grupo))
                return

        fila = tabla_grupo.rowCount()
        if fila < 4:
            tabla_grupo.insertRow(fila)
            tabla_grupo.setItem(fila, 0, QTableWidgetItem(nombre))
            for col in range(1, 8):
                tabla_grupo.setItem(fila, col, QTableWidgetItem("0"))
            equipo = Team(nombre, resistencia, fuerza, velocidad, view.lista_precision.currentText(), grupo, pj=0, pg=0, pe=0, pp=0, ga=0, ge=0, puntos=0, plantilla=plantilla)
            self.equipos[nombre] = equipo
            equipo.guardar_datos_csv()
        else:
            QMessageBox.warning(view, "Límite de equipos", "Ya hay 4 equipos en el grupo {}.".format(grupo))
    
    def llenar_grupos_desde_csv(self, view, archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    nombre = row['nombre']
                    resistencia = int(row['resistencia'])
                    fuerza = int(row['fuerza'])
                    velocidad = int(row['velocidad'])
                    precision = row['precision']
                    grupo = row['grupo']
                    pj = int(row['pj'])
                    pg = int(row['pg'])
                    pe = int(row['pe'])
                    pp = int(row['pp'])
                    ga = int(row['ga'])
                    ge = int(row['ge'])
                    puntos = int(row['puntos'])
                    plantilla = row['plantilla']

                    equipo = Team(nombre, resistencia, fuerza, velocidad, precision, grupo, pj, pg, pe, pp, ga, ge, puntos, plantilla)
                    self.equipos[nombre] = equipo

                    tabla_grupo = self.tablas_por_grupo.get(grupo)
                    if not tabla_grupo:
                        tabla_grupo = QTableWidget()
                        tabla_grupo.setColumnCount(8)
                        tabla_grupo.setHorizontalHeaderLabels(["Equipo", "PJ", "PG", "PE", "PP", "GF", "GC", "Puntos"])
                        tabla_grupo.setEditTriggers(QAbstractItemView.NoEditTriggers)
                        self.tablas_por_grupo[grupo] = tabla_grupo
                        view.tab_widget.addTab(tabla_grupo, grupo)

                    fila = tabla_grupo.rowCount()
                    if fila < 4:
                        tabla_grupo.insertRow(fila)
                        tabla_grupo.setItem(fila, 0, QTableWidgetItem(nombre))
                        for col, value in enumerate([pj, pg, pe, pp, ga, ge, puntos]):
                            tabla_grupo.setItem(fila, col + 1, QTableWidgetItem(str(value)))
                    else:
                        QMessageBox.warning(view, "Límite de equipos", "Ya hay 4 equipos en el grupo {}.".format(grupo))

        except FileNotFoundError:
            QMessageBox.warning(view, "Archivo no encontrado", "El archivo CSV no pudo ser encontrado.")
        except Exception as e:
            QMessageBox.warning(view, "Error", "Ocurrió un error al procesar el archivo CSV: {}".format(str(e)))