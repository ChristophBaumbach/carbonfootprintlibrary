import CO2eTransportation as Transport
class MitarbeiterCO2Transportation:
    def __int__(self, numberOfFullWorkingEquivalents, modeOfTransport = Transport.modeEstimate, name = "", mean_distance_to_work = 0, num_work_days = 0):
        self._anzahl = numberOfFullWorkingEquivalents;

        self._modeOfTransport = modeOfTransport
        self._name = name;
        self._mean_distance_to_work = mean_distance_to_work;
        self.replaceMissingDataWithEstimates()

    def co2FromTransportation:
        return self._anzahl * Transport.transportEmission(car)
    def replaceMissingDataWithEstimates(self):

