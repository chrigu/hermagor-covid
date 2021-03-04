import os
import requests
import csv
import json
import time
from functools import reduce
from io import StringIO

URL = 'https://covid19-dashboard.ages.at/data/CovidFaelle_Timeline_GKZ.csv'
HERMAGOR_CODE = '203'
DATE_FROM = '01.09.2020'


def fetch_covid_data(local_file=''):
    if local_file:
        csv_data = open(local_file, 'r')
    else:
        r = requests.get(URL)
        csv_data = StringIO(r.text)

    district_series = generate_series_for_district(csv_data)

    if local_file:
        csv_data.close()

    with open('../covid-web/src/assets/data.json', 'w') as outfile:
        json.dump(district_series, outfile)


def generate_series_for_district(csv_data):
    covid_reader = csv.reader(csv_data, delimiter=';', quotechar='|')
    district_all_data = list(filter(lambda row: row[2] == os.environ.get('DISTRICT_CODE', HERMAGOR_CODE), covid_reader))
    latest_data = time.strptime(DATE_FROM, "%d.%m.%Y")
    district_latest_data = list(filter(lambda row: time.strptime(row[0], "%d.%m.%Y 00:00:00") > latest_data, district_all_data))
    initial_series = {
        'cases': [],
        'cases_sum': [],
        'incidence': [],
        'deaths': [],
        'deaths_sum': []
    }
    return reduce(add_data_points, district_latest_data, initial_series)


def add_data_points(data, row):
    row_date = time.strptime(row[0], "%d.%m.%Y 00:00:00")
    timestamp = int(time.mktime(row_date)) * 1000
    incidence = row[7].replace(',', '.')

    data['cases'].append({
        'x': timestamp,
        'y': int(row[4])
    })
    data['cases_sum'].append({
        'x': timestamp,
        'y': int(row[5])
    })
    data['incidence'].append({
        'x': timestamp,
        'y': float(incidence)
    })
    data['deaths'].append({
        'x': timestamp,
        'y': int(row[8])
    })
    data['deaths_sum'].append({
        'x': timestamp,
        'y': int(row[9])
    })

    return data


if __name__ == '__main__':
    # fetch_covid_data(local_file='covid_data.csv')
    fetch_covid_data()
