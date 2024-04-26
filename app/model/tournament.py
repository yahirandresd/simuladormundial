from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from app.model.team import Team

class Tournament:
    def __init__(self, tablas_por_grupo):
        self.tablas_por_grupo = tablas_por_grupo

    def ingresar_equipo(self, nombre, resistencia, fuerza, velocidad, precision, grupo):
        tabla_grupo = self.tablas_por_grupo.get(grupo)
        if not tabla_grupo:
            QMessageBox.warning(None, "Error", "No se ha encontrado la tabla del grupo.")
            return

        equipos_grupo = [tabla_grupo.item(fila, 0).text() for fila in range(tabla_grupo.rowCount())]
        if nombre in equipos_grupo:
            QMessageBox.warning(None, "Error", "Este equipo ya está en el grupo {}.".format(grupo))
            return

        for otro_grupo, otra_tabla in self.tablas_por_grupo.items():
            if otro_grupo != grupo and nombre in [otra_tabla.item(fila, 0).text() for fila in range(otra_tabla.rowCount())]:
                QMessageBox.warning(None, "Error", "Este equipo ya está en el grupo {}.".format(otro_grupo))
                return

        fila = tabla_grupo.rowCount()
        if fila < 4:  # Máximo 4 equipos por grupo
            tabla_grupo.insertRow(fila)
            tabla_grupo.setItem(fila, 0, QTableWidgetItem(nombre))

            equipo = Team(nombre, resistencia, fuerza, velocidad, precision, grupo, pj=0, pg=0, pe=0, pp=0, ga=0, ge=0, puntos=0)
            equipo.guardar_datos_csv()
        else:
            QMessageBox.warning(None, "Error", "Ya hay 4 equipos en el grupo {}.".format(grupo))
