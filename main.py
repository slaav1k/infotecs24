# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, json
import pandas as pd
from pytils import translit
from pytz import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.json.sort_keys = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
json.provider.DefaultJSONProvider.ensure_ascii = False

data_path = "RU.txt"
columns = [
    "geonameid",
    "name",
    "asciiname",
    "alternatenames",
    "latitude",
    "longitude",
    "feature class",
    "feature code",
    "country code",
    "cc2",
    "admin1 code",
    "admin2 code",
    "admin3 code",
    "admin4 code",
    "population",
    "elevation",
    "dem",
    "timezone",
    "modification date",
]
df = pd.read_csv(data_path, sep='\t', names=columns, encoding='utf-8')


@app.route('/city/<int:geonameid>', methods=['GET'])
def get_city_by_geonameid(geonameid):
    """
    Метод для получения информации о городе по его идентификатору geonameid
    :param geonameid:
    :return: json c информацией
    """
    city_info = df[df['geonameid'] == geonameid].to_dict(orient='records')[0]
    return jsonify(city_info)


@app.route('/cities', methods=['GET'])
def get_cities():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    cities_info = df[start_index:end_index].to_dict(orient='records')
    return jsonify(cities_info)


@app.route('/compare_cities')
def compare_cities():
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    transliterated_city1 = translit.translify(city1)
    transliterated_city2 = translit.translify(city2)

    city1_info = df[df['name'] == transliterated_city1].sort_values(by='population', ascending=False).iloc[0]
    city2_info = df[df['name'] == transliterated_city2].sort_values(by='population', ascending=False).iloc[0]

    # Определение разницы во временных зонах
    timezone_1 = city1_info['timezone']
    timezone_2 = city2_info['timezone']
    timezone_difference = 0
    if timezone_1 == timezone_2:
        timezone_is_difference = "timezone matches"

    else:
        timezone_is_difference = "timezone doesnt match"
        timezone_difference = _tz_diff(timezone_1, timezone_2)

    # Определение, какой город севернее
    if city1_info['latitude'] > city2_info['latitude']:
        northern_city = transliterated_city1
    elif city1_info['latitude'] < city2_info['latitude']:
        northern_city = transliterated_city2
    else:
        northern_city = "Both cities are at the same latitude"

    result = [
        {'city1_info': city1_info.to_dict()},
        {'city2_info': city2_info.to_dict()},
        {'northern_city': northern_city},
        {'timezone_is_difference': timezone_is_difference}
    ]
    if timezone_is_difference != "timezone matches":
        result.append({"timezone_difference": abs(timezone_difference)})
    return jsonify(*result)


@app.route('/city_by_name/<string:name>', methods=['GET'])
def city_by_name(name):
    # Получаем часть названия города, введенную пользователем
    name = translit.translify(name)
    filtered_cities = df[df['name'].str.contains(name, na=False)]

    suggestions = [{"index": index + 1, "name": name} for index, name in enumerate(filtered_cities['name'].tolist())]
    return jsonify(*suggestions)


@app.route('/')
def get_list():
    return '''Index page'''


def _tz_diff(home, away):
    utcnow = timezone('utc').localize(datetime.utcnow())  # generic time
    here = utcnow.astimezone(timezone(home)).replace(tzinfo=None)
    there = utcnow.astimezone(timezone(away)).replace(tzinfo=None)

    offset = relativedelta(here, there)
    return offset.hours


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
