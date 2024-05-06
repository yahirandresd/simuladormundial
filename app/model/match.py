import random
from  app.model.team import *
class Match:
    def __init__(self, equipo1, equipo2, criterio):
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.criterio = criterio
        self.goles_equipo1 = 0
        self.goles_equipo2 = 0

    def jugar_partido(self):
        resultado = self.aplicar_criterio()
        self.actualizar_estadisticas(resultado)

    def aplicar_criterio(self):

        if self.criterio == "Resistencia":
            if self.equipo1.resistencia > self.equipo2.resistencia:
                self.goles_equipo1 = random.randint(2, 5)
                self.goles_equipo2 = random.randint(1, self.goles_equipo1-1)
                self.equipo1.ga += self.goles_equipo1
                self.equipo2.ge += self.goles_equipo1
                return self.equipo1
            elif self.equipo2.resistencia > self.equipo1.resistencia:
                self.equipo2.ga += self.goles_equipo2
                self.equipo1.ge += self.goles_equipo2
                return self.equipo2
            else:
                # Empate, segunda consideración
                if self.equipo1.fuerza > self.equipo2.fuerza:
                    self.equipo1.ga += self.goles_equipo1
                    self.equipo2.ge += self.goles_equipo1
                    return self.equipo1
                elif self.equipo2.fuerza > self.equipo1.fuerza:
                    self.equipo2.ga += self.goles_equipo2
                    self.equipo1.ge += self.goles_equipo2
                    return self.equipo2
                else:
                    return None  # Empate
        elif self.criterio == "Fuerza":
            # Implementar el criterio de fuerza y segunda consideración
            pass
        elif self.criterio == "Velocidad":
            # Implementar el criterio de velocidad y segunda consideración
            pass
        elif self.criterio == "Precisión":
            # Implementar el criterio de precisión y segunda consideración
            pass

    def actualizar_estadisticas(self, equipo_ganador):
        self.equipo1.pj += 1
        self.equipo2.pj += 1

        # Asegurar que el equipo ganador tenga más goles y que no excedan 5 goles
        if equipo_ganador == self.equipo1:
            self.goles_equipo1 = random.randint(2, 5)
            self.goles_equipo2 = random.randint(1, self.goles_equipo1-1)  # Limitar los goles del equipo 2 a 5
        elif equipo_ganador == self.equipo2:
            self.goles_equipo2 = random.randint(2, 5)
            self.goles_equipo1 = random.randint(1, self.goles_equipo2-1)  # Limitar los goles del equipo 1 a 5

        self.equipo1.ga += self.goles_equipo1
        self.equipo2.ga += self.goles_equipo2
        self.equipo1.ge += self.goles_equipo2  # Los goles recibidos por el equipo 1 son los goles que anotó el equipo 2
        self.equipo2.ge += self.goles_equipo1  # Los goles recibidos por el equipo 2 son los goles que anotó el equipo 1

        if equipo_ganador:
            equipo_ganador.pg += 1
            equipo_ganador.puntos += 3
            if equipo_ganador == self.equipo1:
                self.equipo2.pp += 1
            else:
                self.equipo1.pp += 1
        else:
            self.equipo1.pe += 1
            self.equipo2.pe += 1
            self.equipo1.puntos += 1
            self.equipo2.puntos += 1