from PyQt5.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView
from app.model.team import Team

class Tournament:
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

        if not nombre or not resistencia or not fuerza or not velocidad or not plantilla:
            QMessageBox.warning(view, "Campos incompletos", "Por favor, complete todos los campos.")
            return

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