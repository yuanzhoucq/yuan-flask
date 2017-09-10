import flask_restful as restful
import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)
api = restful.Api(app)


class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}


class Transpole(restful.Resource):
    def get(self):
        r = requests.get('https://www.transpole.fr/cms/institutionnel/fr/se-deplacer/#horaires')
        soup = BeautifulSoup(r.text)
        url_base = soup.find(id='iframe-horaire').attrs['src']
        options = "schedule/line/result/?lineSchedule[network]=network:TRANSPOLE"
        options += "&lineSchedule[line]=line:TRA:ME1"
        options += "&lineSchedule[route]=route:TRA:ME1"
        # options += "&lineSchedule[route]=route:TRA:ME1_R"
        options += "&lineSchedule[from_datetime]=10/09/2017"
        options += "&lineSchedule[line_daypart]=4-7"
        r = requests.get(url_base + options)
        soup = BeautifulSoup(r.text)
        stations = []
        for station in soup.tbody.find_all('tr'):
            timetable = []
            for item_of_timetable in station.find_all('td'):
                timetable.append(item_of_timetable.get_text().strip())
            stations.append({'name': station.th.get_text().strip(), 'timetable': timetable})
        return stations

api.add_resource(HelloWorld, '/api/')
api.add_resource(Transpole, '/api/transpole')

if __name__ == '__main__':
    app.run(debug=True)
