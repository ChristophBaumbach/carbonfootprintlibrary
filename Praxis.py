# Anzahl Mitarbeiter
# Arbeitstage im Jahr
# Durchschnittliche Anzahl von Patienten im Quartal
# Durchschnittliche Anzahl von Besuchen pro Patient
# Lage/Erreichbarkeit der Praxis (zwei schieberegler?)
#     Großstadt zentral –ländlich
#     Gute Anbindung – schlechte Anbindung
#

#todo:
# tomedo function: average distance traveled by besuchen pro Quartal
class Praxis:
    bus = "bus"
    train = "train"
    bicycle = "bicycle"
    walking = "walking"
    def __init__(self):
        self._num_employees = 0
        self._num_workdays = 0
        self._num_of_visits_per_quarter = 0
        self._amount_of_transport_modes = {
            Praxis.car: 0.5,
            Praxis.bus: 0.2,
            Praxis.train: 0.1,
            Praxis.bicyvle: 0.05,
            Praxis.walking: 0.15
        }



    def calculateWithDistanceAndTransportationmode(self, distance, mode=Praxis.car):

        # CO2 emission values per mode of transportation in kg/km
        emission_values = {
            Praxis.car: 0.2,
            Praxis.bus: 0.03,
            Praxis.train: 0.01,
            Praxis.bicyvle: 0,
            Praxis.walking: 0
        }

        if mode in emission_values:
            emission_factor = emission_values[mode]
            return emission_factor * distance
        else:
            return None

