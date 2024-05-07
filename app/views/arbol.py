from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem

class Arbol(QWidget):
    def __init__(self, equipos_calificados):
        super().__init__()
        self.setWindowTitle("Cuadro de Eliminatorias")
        self.resize(1920, 1080)  # Establecer el tamaño de la ventana
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Crear una tabla para la etapa de Octavos de Final
        tabla_octavos = QTableWidget()
        tabla_octavos.setColumnCount(1)  # Solo una columna para mostrar los equipos
        tabla_octavos.setRowCount(24)  # 24 filas para la etapa de Octavos de Final
        tabla_octavos.setHorizontalHeaderLabels(["Octavos de Final"])
        self.llenar_tabla(tabla_octavos, equipos_calificados)
        self.layout.addWidget(tabla_octavos)

        # Crear una tabla para la etapa de Cuartos de Final (vacía por ahora)
        tabla_cuartos = QTableWidget()
        tabla_cuartos.setColumnCount(1)  # Solo una columna para mostrar los equipos
        tabla_cuartos.setRowCount(12)  # 8 filas para la etapa de Cuartos de Final
        tabla_cuartos.setHorizontalHeaderLabels(["Cuartos de Final"])
        self.layout.addWidget(tabla_cuartos)

        # Crear una tabla para la etapa de Semifinal (vacía por ahora)
        tabla_semifinal = QTableWidget()
        tabla_semifinal.setColumnCount(1)  # Solo una columna para mostrar los equipos
        tabla_semifinal.setRowCount(8)  # 4 filas para la etapa de Semifinal
        tabla_semifinal.setHorizontalHeaderLabels(["Semifinal"])
        self.layout.addWidget(tabla_semifinal)
        
        # Crear una tabla para la etapa de Semifinal (vacía por ahora)
        tabla_final = QTableWidget()
        tabla_final.setColumnCount(1)  # Solo una columna para mostrar los equipos
        tabla_final.setRowCount(2)  # 4 filas para la etapa de Semifinal
        tabla_final.setHorizontalHeaderLabels(["Final"])
        self.layout.addWidget(tabla_final)

    def llenar_tabla(self, tabla, equipos_calificados):
        for i, equipos_grupo in enumerate(equipos_calificados):
            if i < len(equipos_calificados):  # Asegurar que se muestren todos los equipos calificados
                equipo1 = equipos_grupo[0]
                equipo2 = equipos_grupo[1]
                item1 = QTableWidgetItem(equipo1)
                item2 = QTableWidgetItem(equipo2)
                tabla.setItem(i * 2, 0, item1)  # Colocar equipo1 en fila par
                tabla.setItem(i * 2 + 1, 0, item2)  # Colocar equipo2 en fila impar
