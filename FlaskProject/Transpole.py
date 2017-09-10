from datetime import datetime

import flask_restful as restful
import requests
from bs4 import BeautifulSoup


class Transpole(restful.Resource):
    def get(self, line, direction, start_station):
        if not ((line == 'ME1' or line == 'ME2') and (direction == line or direction == line + '_R')):
            return {'error': 'bad parameters'}
        r = requests.get('https://www.transpole.fr/cms/institutionnel/fr/se-deplacer/#horaires')
        soup = BeautifulSoup(r.text)
        url_base = soup.find(id='iframe-horaire').attrs['src']
        options = "schedule/line/result/?lineSchedule[network]=network:TRANSPOLE"
        options += "&lineSchedule[line]=line:TRA:{line}".format(line=line)
        options += "&lineSchedule[route]=route:TRA:{route}".format(route=direction)
        # options += "&lineSchedule[route]=route:TRA:ME1_R"
        now = datetime.now()
        options += "&lineSchedule[from_datetime]={date}".format(date=now.strftime("%d/%m/%Y"))
        options += "&lineSchedule[line_daypart]=4-7"
        r = requests.get(url_base + options)
        soup = BeautifulSoup(r.text)
        stations_data = soup.tbody.find_all('tr')
        stations = []
        routes = []
        if len(stations_data) <= start_station:
            return {'error': 'bad parameters'}
        index_of_start_time = 0
        for station in stations_data[start_station:]:
            timetable = []
            for idx, item_of_timetable in enumerate(station.find_all('td')[index_of_start_time:]):
                time = item_of_timetable.get_text().strip()
                [hour, minute] = time.split('h')
                if (not timetable) and (int(hour) < now.hour or (int(hour) == now.hour and int(minute) < now.minute)):
                    index_of_start_time = idx + 1
                    continue
                timetable.append(time)
            stations.append({'name': station.th.get_text().strip(), 'timetable': timetable})
        for i in range(len(stations[0]['timetable'])):
            route = []
            for station in stations:
                route.append(station['timetable'][i])
            routes.append(route)
        return {'routes': routes, 'stations': stations}
