from functools import reduce

import requests
import csv
import json
from io import StringIO
from datetime import datetime

URL = 'https://covid19-dashboard.ages.at/data/CovidFaelle_Timeline_GKZ.csv'
HERMAGOR_CODE = '203'


def fetch_covid_data(local_file=''):
    if local_file:
        csv_data = open(local_file, 'r')
    else:
        r = requests.get(URL)
        csv_data = StringIO(r.text)

    hermagor_data = generate_data_for_hermagor(csv_data)

    if local_file:
        csv_data.close()

    with open('../covid-web/src/assets/data.json', 'w') as outfile:
        json.dump(hermagor_data, outfile)


def generate_data_for_hermagor(csv_data):
    covid_reader = csv.reader(csv_data, delimiter=';', quotechar='|')
    hermagor_data = list(filter(lambda row: row[2] == HERMAGOR_CODE, covid_reader))
    initial_data = {
        'cases': [],
        'cases_sum': [],
        'incidence': [],
        'deaths': [],
        'deaths_sum': []
    }
    return reduce(add_data_points, hermagor_data, initial_data)


def add_data_points(data, row):
    item_date = datetime.strptime(row[0], "%d.%m.%Y 00:00:00")
    incidence = row[7].replace(',', '.')

    data['cases'].append((item_date.isoformat(), int(row[4])))
    data['cases_sum'].append((item_date.isoformat(), int(row[5])))
    data['incidence'].append((item_date.isoformat(), float(incidence)))
    data['deaths'].append((item_date.isoformat(), int(row[8])))
    data['deaths_sum'].append((item_date.isoformat(), int(row[9])))

    return data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fetch_covid_data(local_file='covid_data.csv')
    # fetch_covid_data()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
