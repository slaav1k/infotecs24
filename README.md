#Тестовое задание для стажера на позицию «Программист на языке Python»
Реализовать HTTP-сервер для предоставления информации по географическим объектам.
Данные взять из географической базы данных GeoNames, по [ссылке](http://download.geonames.org/export/dump/RU.zip)
Описание формата данных можно найти по [ссылке](http://download.geonames.org/export/dump/readme.txt)
Реализованный сервер должен предоставлять REST API сервис со следующими методами:
1. <b>Метод принимает идентификатор geonameid и возвращает информацию о городе.</b>
`GET /city/geonameid`
Данный метод вернет информацию о городе, по <i>geonameid</i>
Например, при
`GET /city/451877` 
Получаем в ответ
`"GET /city/451877 HTTP/1.1" 200 -`
и тело 
```json
{
    "geonameid":451877,
    "name":"Red’kino",
    "asciiname":"Red'kino",
    "alternatenames":"Red'kino,Red’kino,Редькино",
    "latitude":56.78098,
    "longitude":34.53424,
    "feature class":"P",
    "feature code":"PPL",
    "country code":"RU",
    "cc2":NaN,"admin1 code":77,
    "admin2 code":NaN,
    "admin3 code":NaN,
    "admin4 code":NaN,
    "population":0,
    "elevation":NaN,
    "dem":224,
    "timezone":"Europe/Moscow",
    "modification date":"2012-01-16"
}
```
2. <b>Метод принимает страницу и количество отображаемых на странице городов и
возвращает список городов с их информацией.</b>
`GET /cities`
Данный метод вернет список с информацией о городах, согласно следующим параметрам:
* `page` - какую страницу вывести
* `per_page` - количество записей на странице
Например:
`GET /cities?page=4&per_page=3`
Вернет
`"GET /cities?page=4&per_page=3 HTTP/1.1" 200 -`
```json
[
    {
        "geonameid":451756,
        "name":"Zarech’ye",
        "asciiname":"Zarech'ye",
        "alternatenames":NaN,
        "latitude":56.68265,
        "longitude":34.70984,
        "feature class":"P",
        "feature code":"PPL",
        "country code":"RU",
        "cc2":NaN,
        "admin1 code":77,
        "admin2 code":NaN,
        "admin3 code":NaN,
        "admin4 code":NaN,
        "population":0,
        "elevation":NaN,
        "dem":178,
        "timezone":"Europe/Moscow",
        "modification date":"2011-07-09"
    },
    {
        "geonameid":451757,
        "name":"Zamush’ye",
        "asciiname":"Zamush'ye",
        "alternatenames":NaN,
        "latitude":57.22984,
        "longitude":34.77983,
        "feature class":"P",
        "feature code":"PPL",
        "country code":"RU",
        "cc2":NaN,
        "admin1 code":77,
        "admin2 code":NaN,
        "admin3 code":NaN,
        "admin4 code":NaN,
        "population":0,
        "elevation":NaN,
        "dem":182,
        "timezone":"Europe/Moscow",
        "modification date":"2011-07-09"
    },
    {
        "geonameid":451758,
        "name":"Zaleden’ye",
        "asciiname":"Zaleden'ye",
        "alternatenames":NaN,
        "latitude":57.12851,
        "longitude":34.26788,
        "feature class":"P",
        "feature code":"PPLQ",
        "country code":"RU",
        "cc2":NaN,
        "admin1 code":77,
        "admin2 code":NaN,
        "admin3 code":NaN,
        "admin4 code":NaN,
        "population":0,
        "elevation":NaN,
        "dem":278,
        "timezone":"Europe/Moscow",
        "modification date":"2011-07-09"
    }
]
```
3. <b>Метод принимает названия двух городов (на русском языке) и получает информацию
о найденных городах, а также дополнительно: какой из них расположен севернее и
одинаковая ли у них временная зона (когда несколько городов имеют одно и то же
название, разрешать неоднозначность выбирая город с большим населением; если
население совпадает, брать первый попавшийся)</b>
`GET /compare_cities`
Этот метод выводит информацию о двух городах и говорит, какой из них северней и есть ли разница в часовых зонах у них.
Параметры:
* `city1` - первый город
* `city2` - второй город
Например:
`GET /compare_cities?city1=Тимошкино&city2=Патраково`
В ответ получаем `"GET /compare_cities?city1=Тимошкино&city2=Патраково HTTP/1.1" 200 -` 
```json
[
    {
        "city1_info":
        {
            "geonameid":451811,
            "name":"Timoshkino",
            "asciiname":"Timoshkino",
            "alternatenames":NaN,
            "latitude":57.19533,
            "longitude":34.87121,
            "feature class":"P",
            "feature code":"PPL",
            "country code":"RU",
            "cc2":NaN,
            "admin1 code":77,
            "admin2 code":NaN,
            "admin3 code":NaN,
            "admin4 code":NaN,
            "population":0,
            "elevation":NaN,
            "dem":176,"timezone":"Europe/Moscow",
            "modification date":"2011-07-09"
        }
    },
    {
        "city2_info":
        {
            "geonameid":451907,
            "name":"Patrakovo",
            "asciiname":"Patrakovo",
            "alternatenames":"Patrakovo,Патраково",
            "latitude":56.75165,
            "longitude":34.69534,
            "feature class":"P",
            "feature code":"PPL",
            "country code":"RU",
            "cc2":NaN,
            "admin1 code":77,
            "admin2 code":NaN,
            "admin3 code":NaN,
            "admin4 code":NaN,
            "population":0,
            "elevation":NaN,
            "dem":202,
            "timezone":"Europe/Moscow",
            "modification date":"2012-01-16"
        }
    },
    {
        "northern_city":"Timoshkino"
    },
    {
        "timezone_is_difference":"timezone matches"
    }
]
```
После информации о городах, также есть дополнительная информация о том, какой город располагается ближе к серверу и совпдает ли временная зона.

<b>Дополнительные задания:</b>

* <b>Для 3-его метода показывать пользователю не только факт различия временных зон,
но и на сколько часов они различаются.</b>
`GET /compare_cities?city1=Клин&city2=Магадан`
В ответ получаем `"GET /compare_cities?city1=Клин&city2=Магадан HTTP/1.1" 200 -`
```json
[
    {
        "city1_info":
        {
            "geonameid":547523,
            "name":"Klin",
            "asciiname":"Klin",
            "alternatenames":"Klin,Klina,Kline,Kļina,Ulin,ke lin,keullin,kln,klyn,kurin,Клин,Клин балһсн,Клін,كلين,کلن,کلین,クリン,克林,클린",
            "latitude":56.33342,
            "longitude":36.73195,
            "feature class":"P",
            "feature code":"PPLA2",
            "country code":"RU",
            "cc2":NaN,
            "admin1 code":47,
            "admin2 code":NaN,
            "admin3 code":NaN,
            "admin4 code":NaN,
            "population":80778,
            "elevation":NaN,
            "dem":160,
            "timezone":"Europe/Moscow",
            "modification date":"2023-07-11"
        }
    },
    {
        "city2_info":
        {
            "geonameid":2123628,
            "name":"Magadan",
            "asciiname":"Magadan",
            "alternatenames":"GDX,Magadaan,Magadan,Magadana,Magadanas,Magadán,Mankantan,Maqadan,ma jia dan,magadan,magadana,maghadan,majadan,mgdn,Μαγκαντάν,Магадаан,Магадан,Մագադան,מגדן,ماجادان,ماغادان,ماگادان,मागादान,マガダン,马加丹,마가단",
            "latitude":59.5638,
            "longitude":150.80347,
            "feature class":"P",
            "feature code":"PPLA",
            "country code":"RU",
            "cc2":NaN,
            "admin1 code":"44",
            "admin2 code":NaN,
            "admin3 code":NaN,
            "admin4 code":NaN,
            "population":92782,
            "elevation":NaN,
            "dem":65,
            "timezone":"Asia/Magadan",
            "modification date":"2022-08-18"
        }
    },
    {
        "northern_city":"Magadan"
    },
    {
        "timezone_is_difference":"timezone doesnt match"
    },
    {
        "timezone_difference":8
    }
]
```
Теперь после информации о городах, есть дополнительная информация не только о том, какой город располагается ближе к серверу и совпдает ли временная зона, но и насколько отличаются эти временные зоны в случае их несовпадения.
* <b>Реализовать метод, в котором пользователь вводит часть названия города и
возвращает ему подсказку с возможными вариантами продолжений.</b>
`/city_by_name/name` 
Данный метод вернет названия городов, по <i>name</i> - части названия.
Можно делать запрос и латиницей, и кириллицей. 
`GET /city_by_name/Ряз`
либо
`GET /city_by_name/Ryaz` 
Ответ будет одинаков
`"GET /city_by_name/Ряз HTTP/1.1" 200 -`
и
`"GET /city_by_name/Ryaz HTTP/1.1" 200 -`
```json
[
    {
        "index": 1,
        "name": "Urochishche Ryazanovo"
    },
    {
        "index": 2,
        "name": "Ryazanovka"
    },
    {
        "index": 3,
        "name": "Vostochnaya Ryazanovka"
    },
    // часть ответа пропущена
    {
        "index": 152,
        "name": "Urochishche Pole Ryazanovo"
    },
    {
        "index": 153,
        "name": "Gorodskoy Okrug Ryazan'"
    },
    {
        "index": 154,
        "name": "Ryazanovskiy Khrebet"
    },
    {
        "index": 155,
        "name": "Urochishche Pustosh Ryazov'ye"
    }
]
```

<b>Список внешних зависимостей:</b>
* pandas~=2.2.0
* flask~=3.0.2
* pytils~=0.4.1
* pytz~=2024.1
* python-dateutil~=2.8.2

<b>Процесс устновки/запуска приложения:</b>
1. Установить внешние зависимости из файла:
`pip install -r requirements.txt`
2. Запустить <i>main.py</i>