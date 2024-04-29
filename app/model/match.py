import random
from app.model.team import Team

class Match:
    def _init_(self):
        pass

    def jugar_partido(self, eq1, eq2, criterio, i):
        if criterio == 'resistencia':
            if eq1.resistencia > eq2.resistencia:
                while eq1.estadisticas['GF'] <= eq1.estadisticas['GC']:
                    eq1.estadisticas['GF'] = random.randint(1, 5)
                    eq2.estadisticas['GC'] = eq1.estadisticas['GF']
                    eq1.estadisticas['GC'] = random.randint(1, 5)
                    eq2.estadisticas['GF'] = eq1.estadisticas['GC']
                eq1.estadisticas['PG'] += 1
                eq1.estadisticas['PTS'] += 3
                eq2.estadisticas['PP'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
            elif eq1.resistencia < eq2.resistencia:
                while eq2.estadisticas['GF'] <= eq2.estadisticas['GC']:
                    eq2.estadisticas['GF'] = random.randint(1, 5)
                    eq1.estadisticas['GC'] = eq1.estadisticas['GF']
                    eq2.estadisticas['GC'] = random.randint(1, 5)
                    eq1.estadisticas['GF'] = eq1.estadisticas['GC']
                eq2.estadisticas['PG'] += 1
                eq2.estadisticas['PTS'] += 3
                eq1.estadisticas['PP'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
            elif i == 0:
                return self.jugar_partido(eq1, eq2, 'fuerza', 1)
            else:
                eq1.estadisticas['GF'] = random.randint(0, 3)
                eq1.estadisticas['GC'] = eq1.estadisticas['GF']
                eq2.estadisticas['GF'] = eq1.estadisticas['GF']
                eq2.estadisticas['GC'] = eq1.estadisticas['GF']

                eq1.estadisticas['PE'] += 1
                eq2.estadisticas['PE'] += 1
                eq1.estadisticas['PTS'] += 1
                eq2.estadisticas['PTS'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
        elif criterio == 'fuerza':
            if eq1.fuerza > eq2.fuerza:
                while eq1.estadisticas['GF'] <= eq1.estadisticas['GC']:
                    eq1.estadisticas['GF'] = random.randint(1, 5)
                    eq2.estadisticas['GC'] = eq1.estadisticas['GF']
                    eq1.estadisticas['GC'] = random.randint(1, 5)
                    eq2.estadisticas['GF'] = eq1.estadisticas['GC']
                eq1.estadisticas['PG'] += 1
                eq1.estadisticas['PTS'] += 3
                eq2.estadisticas['PP'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
            elif eq1.fuerza < eq2.fuerza:
                while eq2.estadisticas['GF'] <= eq2.estadisticas['GC']:
                    eq2.estadisticas['GF'] = random.randint(1, 5)
                    eq1.estadisticas['GC'] = eq1.estadisticas['GF']
                    eq2.estadisticas['GC'] = random.randint(1, 5)
                    eq1.estadisticas['GF'] = eq1.estadisticas['GC']
                eq2.estadisticas['PG'] += 1
                eq2.estadisticas['PTS'] += 3
                eq1.estadisticas['PP'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
            elif i == 0:
                return self.jugar_partido(eq1, eq2, 'velocidad', 1)
            else:
                eq1.estadisticas['GF'] = random.randint(0, 3)
                eq1.estadisticas['GC'] = eq1.estadisticas['GF']
                eq2.estadisticas['GF'] = eq1.estadisticas['GF']
                eq2.estadisticas['GC'] = eq1.estadisticas['GF']

                eq1.estadisticas['PE'] += 1
                eq2.estadisticas['PE'] += 1
                eq1.estadisticas['PTS'] += 1
                eq2.estadisticas['PTS'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
        elif criterio == 'velocidad':
            if eq1.velocidad > eq2.velocidad:
                while eq1.estadisticas['GF'] <= eq1.estadisticas['GC']:
                    eq1.estadisticas['GF'] = random.randint(1, 5)
                    eq2.estadisticas['GC'] = eq1.estadisticas['GF']
                    eq1.estadisticas['GC'] = random.randint(1, 5)
                    eq2.estadisticas['GF'] = eq1.estadisticas['GC']
                eq1.estadisticas['PG'] += 1
                eq1.estadisticas['PTS'] += 3
                eq2.estadisticas['PP'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
            elif eq1.velocidad < eq2.velocidad:
                while eq2.estadisticas['GF'] <= eq2.estadisticas['GC']:
                    eq2.estadisticas['GF'] = random.randint(1, 5)
                    eq1.estadisticas['GC'] = eq1.estadisticas['GF']
                    eq2.estadisticas['GC'] = random.randint(1, 5)
                    eq1.estadisticas['GF'] = eq1.estadisticas['GC']
                eq2.estadisticas['PG'] += 1
                eq2.estadisticas['PTS'] += 3
                eq1.estadisticas['PP'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
            elif i == 0:
                return self.jugar_partido(eq1, eq2, 'precision', 1)
            else:
                eq1.estadisticas['GF'] = random.randint(0, 3)
                eq1.estadisticas['GC'] = eq1.estadisticas['GF']
                eq2.estadisticas['GF'] = eq1.estadisticas['GF']
                eq2.estadisticas['GC'] = eq1.estadisticas['GF']

                eq1.estadisticas['PE'] += 1
                eq2.estadisticas['PE'] += 1
                eq1.estadisticas['PTS'] += 1
                eq2.estadisticas['PTS'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
        elif criterio == 'precision':
            if eq1.precision > eq2.precision:
                while eq1.estadisticas['GF'] <= eq1.estadisticas['GC']:
                    eq1.estadisticas['GF'] = random.randint(1, 5)
                    eq2.estadisticas['GC'] = eq1.estadisticas['GF']
                    eq1.estadisticas['GC'] = random.randint(1, 5)
                    eq2.estadisticas['GF'] = eq1.estadisticas['GC']
                eq1.estadisticas['PG'] += 1
                eq1.estadisticas['PTS'] += 3
                eq2.estadisticas['PP'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
            elif eq1.precision < eq2.precision:
                while eq2.estadisticas['GF'] <= eq2.estadisticas['GC']:
                    eq2.estadisticas['GF'] = random.randint(1, 5)
                    eq1.estadisticas['GC'] = eq1.estadisticas['GF']
                    eq2.estadisticas['GC'] = random.randint(1, 5)
                    eq1.estadisticas['GF'] = eq1.estadisticas['GC']
                eq2.estadisticas['PG'] += 1
                eq2.estadisticas['PTS'] += 3
                eq1.estadisticas['PP'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
            elif i == 0:
                return self.jugar_partido(eq1, eq2, 'resistencia', 1)
            else:
                eq1.estadisticas['GF'] = random.randint(0, 3)
                eq1.estadisticas['GC'] = eq1.estadisticas['GF']
                eq2.estadisticas['GF'] = eq1.estadisticas['GF']
                eq2.estadisticas['GC'] = eq1.estadisticas['GF']

                eq1.estadisticas['PE'] += 1
                eq2.estadisticas['PE'] += 1
                eq1.estadisticas['PTS'] += 1
                eq2.estadisticas['PTS'] += 1
                return [eq1.estadisticas, eq2.estadisticas]
        else:
            return 'Criterio no válido'
