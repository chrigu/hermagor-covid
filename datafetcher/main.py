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

    hermagor_json = generate_json_with_reader(csv_data)

    if local_file:
        csv_data.close()

    return hermagor_json


def generate_json_with_reader(csv_data):
    covid_reader = csv.reader(csv_data, delimiter=';', quotechar='|')
    hermagor_data = [strip_data(row) for row in covid_reader if row[2] == HERMAGOR_CODE]
    return json.dumps(hermagor_data)


def strip_data(row):
    # 0: datetime, 4: cases, 5: cases sum, 7: 7 day incidence, 8: deaths, 9: deaths sum
    item_date = datetime.strptime(row[0], "%d.%m.%Y 00:00:00")
    incidence = row[7].replace(',', '.')
    return [item_date.isoformat(), int(row[4]), int(row[5]), float(incidence), int(row[8]), int(row[9])]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fetch_covid_data(local_file='covid_data.csv')
    # fetch_covid_data()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
