from backend.discovery import multidiscovery
from backend.discovery import trip
import dateutil.parser

class Main(multidiscovery.Multidiscovery):
    def __init__(self):
        format = ('name', 'country', 'identifiers.easyjet')
        super().__init__(self.config.get_departure_city().get('identifiers').get('easyjet'), self.config.get_formatted_cities(format))

    def get_date(self, offset=0):
        return super().get_date('%Y-%m-%d', offset)

    def search_location(self, p, offset=0):
        trips = []
        print(p[2])
        print(self.get_date(offset))
        try:
            search = self.session.get('https://www.easyjet.com/ejavailability/api/v78/availability/query',
            params={
                'AdditionalSeats': 0,
                'AdultSeats': 1,
                'ArrivalIata': p[2],
                'ChildSeats': 0,
                'DepartureIata': self.departure,
                'IncludeFlexiFares': 'false',
                'IncludeLowestFareSeats': 'true',
                'IncludePrices': 'true',
                'Infants': 0,
                'IsTransfer': 'false',
                'LanguageCode': 'EN',
                'MaxDepartureDate': self.get_date(offset),
                'MinDepartureDate': self.get_date(offset)
            }).json()
            print("Search Result:", search)
            for k in search['AvailableFlights']:
                flight = k['FlightFares']
                if (price := flight['Prices']['Adult']['Price']) <= trip.good_price and price > 0:
                    trips.append(
                        trip.Trip(
                            date=dateutil.parser.parse(k['LocalDepartureTime']),
                            departure='Lyon',
                            arrival=k['ArrivalIata'],
                            carrier=self.base_name(__name__),
                            duration=(dateutil.parser.parse(k['LocalArrivalTime'])-dateutil.parser.parse(k['LocalDepartureTime'])).seconds/60,
                            price=price,
                            arrival_country=flight['ArrivalIata']
                        ).to_dict()
                    )
        except: 
            pass
        return trips