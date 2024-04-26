import csv

class Team:
    def __init__(self, nombre, resistencia, fuerza, velocidad, precision, grupo):
        self.nombre = nombre
        self.resistencia = resistencia
        self.fuerza = fuerza
        self.velocidad = velocidad
        self.precision = precision
        self.grupo = grupo

    def guardar_datos_csv(self):
        # Nombre del archivo CSV
        archivo_csv = "equipos.csv"

        # Encabezados del archivo CSV
        encabezados = ["Nombre", "Resistencia", "Fuerza", "Velocidad", "Precision", "Grupo"]

        # Datos de este equipo
        datos_equipo = [self.nombre, self.resistencia, self.fuerza, self.velocidad, self.precision, self.grupo]

        # Escribir los datos en el archivo CSV
        with open(archivo_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Verificar si es el primer equipo y agregar los encabezados
            if file.tell() == 0:
                writer.writerow(encabezados)
            writer.writerow(datos_equipo)
