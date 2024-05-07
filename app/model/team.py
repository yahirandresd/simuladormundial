import csv

class Team:
    def __init__(self, nombre, resistencia, fuerza, velocidad, precision, grupo, pj, pg, pe, pp, ga, ge, puntos, plantilla):
        self.nombre = nombre
        self.resistencia = resistencia
        self.fuerza = fuerza
        self.velocidad = velocidad
        self.precision = precision
        self.grupo = grupo
        self.pj = pj
        self.pg = pg
        self.pe = pe
        self.pp = pp
        self.ga = ga
        self.ge = ge
        self.puntos = puntos
        self.plantilla = plantilla

    def obtener_numero_precision(self):
        if self.precision == "Bajo":
            return 1
        elif self.precision == "Medio":
            return 2
        elif self.precision == "Alto":
            return 3

    def guardar_datos_csv(self):
        # Nombre del archivo CSV
        archivo_csv = "xyzRESERVA.csv"

        numero_precision = self.obtener_numero_precision()

        # Datos de este equipo como un diccionario
        datos_equipo = {
            "Nombre": self.nombre,
            "Resistencia": self.resistencia,
            "Fuerza": self.fuerza,
            "Velocidad": self.velocidad,
            "Precision": numero_precision,
            "Grupo": self.grupo,
            "PJ": self.pj,
            "PG": self.pg,
            "PE": self.pe,
            "PP": self.pp,
            "GA": self.ga,
            "GE": self.ge,
            "Puntos": self.puntos,
            "Plantilla": self.plantilla
        }
        print(datos_equipo)

        # Escribir los datos en el archivo CSV
        with open(archivo_csv, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=datos_equipo.keys())
            writer.writeheader()
            writer.writerow(datos_equipo)