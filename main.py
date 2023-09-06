from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import CO2eTransportation as Transportation
import json


##todo
#Doctor CO2Quickcheck
    #
    # Fachrichtung
    # Anzahl Mitarbeiter
    # Arbeitstage im Jahr
    # Durchschnittliche Anzahl von Patienten im Quartal
    # Durchschnittliche Anzahl von Besuchen pro Patient
    # Lage/Erreichbarkeit der Praxis (zwei schieberegler?)
    #     Großstadt zentral –ländlich
    #     Gute Anbindung – schlechte Anbindung
    #
    # Praxisfläche
    # Art des Praxisgebäude
    # Baujahr/Standard
    # Art der Heizung (fossil/erneuerbar)
    # Solarthermie?
    # Strombezug (Strommix/Ökostrom/Selbsterzeugung/ Fernwärme)
    #
    # Patientenkommunikation (Rechnungen/Befunde/Terminabsprachen):
    #     Mails
    #     Telefon
    #     Briefversand
    #     OTK
    #     App
    #
    # Praxismaterial (Unterscheiden in Büro/medizinischen Bedarf??)
    #     Wird in großen Mengen geordert
    # Dienstkleidung
    # Verwenden insofern möglich Mehrweg-/ Einwegprodukte (Rating in Form einer Skala)
    # Recyclingpapier: j/n (Druckerpapier und Klopapier und Papierhandtücher)
    # Digitale Praxis
    # Strikte Mülltrennung (1: super wichtig – 5: achten wir eigentlich gar nicht drauf)
    #
    # Anzahl Arbeitsplätze
    # Anzahl Drucker/Kopierer/Scanner
    # Anzahl medizinischer Geräte:
    #     Groß bis 1000kg
    #     Mittel bis ca. 100kg
    #     Klein bis ca. 30kg
    # Server: lokal oder Rechenzentrum?
    #
    # Weitere klimaschonende Maßnahmen:
    #     Förderung&Animation von Mitarbeitern zu klimaschonenenden Verhalten (Erscheinen mit Fahrrad /Öffis/Carsharing/zu Fuß)
    #     Förderung&Animation von Patienten zu klimaschonenenden Verhalten (Erscheinen mit Fahrrad /Öffis/Carsharing/zu Fuß)
    #     Wasser sparen durch…
    #     CO2-Kompensationsmaßnahmen – Bäume pflanzen etc.
    #     Kaufen nachhaltig ein

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello, this is the root page!')
        elif self.path.startswith('/transport'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            sub_path = self.path.split("/")[-1]
           # self.wfile.write(b'hi i am listening')
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            result = Transportation.jsonResultForPathWithParams(sub_path, query_params)
            self.wfile.write(json.dumps(result).encode('utf-8'))
            return
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 - Page not found')
        # Parse query parameters
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        distance = float(query_params.get('distance', ['0'])[0])
        mode = query_params.get('mode', [''])[0]

        # Calculate CO2 footprint
        calculator = Transportation
        footprint = calculator.calculateWithDistanceAndTransportationmode(distance, mode)

        # Prepare response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Generate HTML response
        response = f'''
            <html>
            <body>
                <h1>CO2 Footprint Calculator</h1>
                <form action="/" method="get">
                    <label for="distance">Distance (in km):</label>
                    <input type="text" name="distance" id="distance" value="{distance}">
                    <br>
                    <label for="mode">Mode of transportation:</label>
                    <select name="mode" id="mode">
                        <option value="car" {'selected' if mode == 'car' else ''}>Car</option>
                        <option value="bus" {'selected' if mode == 'bus' else ''}>Bus</option>
                        <option value="train" {'selected' if mode == 'train' else ''}>Train</option>
                        <option value="bicycle" {'selected' if mode == 'bicycle' else ''}>Bicycle</option>
                        <option value="walking" {'selected' if mode == 'walking' else ''}>Walking</option>
                    </select>
                    <br>
                    <input type="submit" value="Calculate">
                </form>
                <br>
                <p>CO2 Footprint: {footprint if footprint is not None else 'N/A'} kg</p>
            </body>
            </html>
        '''

        self.wfile.write(response.encode('utf-8'))


def run_server():
    server_address = ('', 8008)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Server running on port 8008...')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
