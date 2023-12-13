import dateutil.parser
import requests
import datetime
import tripobj

departure = ('Napoli', 'Italy', '40e096c1-8646-11e6-9066-549f350fcb0c')
arrivals = [
    ('Roma', 'Italy', '40de90ff-8646-11e6-9066-549f350fcb0c'),
    ('Firenze', 'Italy', '40de71c6-8646-11e6-9066-549f350fcb0c'),
    ('Venezia', 'Italy', '40dea03b-8646-11e6-9066-549f350fcb0c'),
    ('Bari', 'Italy', '40df3bba-8646-11e6-9066-549f350fcb0c'),
    ('Milano', 'Italy', '40ddcc6e-8646-11e6-9066-549f350fcb0c'),
    ('Trieste', 'Italy', '40de9f2f-8646-11e6-9066-549f350fcb0c'),

    ('Rijeka', 'Croatia', '40e11860-8646-11e6-9066-549f350fcb0c'),
    ('Zagreb', 'Croatia', '40dea87d-8646-11e6-9066-549f350fcb0c'),
    ('Lyon', 'France', '40df89c1-8646-11e6-9066-549f350fcb0c'),
    ('Budapest', 'Hungary', '40de6527-8646-11e6-9066-549f350fcb0c'),
    ('Geneva Airport', 'Switzerland', '89b7ebc7-cf52-4dac-97fd-b08ef8679623'),
    ('Münich', 'Germany', '40d901a5-8646-11e6-9066-549f350fcb0c'),
    ('Bern', 'Switzerland', '40df4ec8-8646-11e6-9066-549f350fcb0c'),
    ('Innsbrück', 'Austria', '40dd9a2a-8646-11e6-9066-549f350fcb0c'),
    ('Graz', 'Austria', '40de3c97-8646-11e6-9066-549f350fcb0c'),
    ('Cannes', 'France', '40e0010f-8646-11e6-9066-549f350fcb0c')
]

def get_date(offset=0):
    return (datetime.datetime.now() + datetime.timedelta(1)).strftime('%d.%m.%Y')

def search_trips(departure, arrivals):
    trips = []
    for p in arrivals:
        search = requests.get('https://global.api.flixbus.com/search/service/v4/search',
        params={
            'from_city_id': departure[2],
            'to_city_id': p[2],
            'departure_date': get_date(),
            'products': '{"adult":1}',
            'currency': 'EUR',
            'locale': 'it',
            'search_by': 'cities',
            'include_after_midnight_rides': '1'
        }).json()
        for k in search.get('trips')[0]['results']:
            trip = search.get('trips')[0]['results'][k]
            if (price := trip['price']['total']) < tripobj.good_price:
                trips.append(
                    tripobj.Trip(
                        date=dateutil.parser.parse(trip['departure']['date']),
                        departure=departure[0],
                        arrival=p[0],
                        carrier='Flixbus',
                        duration=(trip['duration']['hours'] * 60) + trip['duration']['minutes'],
                        price=price,
                        arrival_country=p[1]
                    ).to_dict()
            )
    return trips