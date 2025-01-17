import json
from django.test import TestCase


class WeatherTest(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_search_geo(self):
        response = self.client.get('/api/search-geo/')
        self.assertEqual(response.status_code, 200)

        result = [{'id': 2643743, 'name': 'London', 'latitude': 51.50853, 'longitude': -0.12574, 'elevation': 25.0, 'feature_code': 'PPLC', 'country_code': 'GB', 'admin1_id': 6269131, 'admin2_id': 2648110, 'timezone': 'Europe/London', 'population': 7556900, 'country_id': 2635167, 'country': 'United Kingdom', 'admin1': 'England', 'admin2': 'Greater London'}, {'id': 6058560, 'name': 'London', 'latitude': 42.98339, 'longitude': -81.23304, 'elevation': 252.0, 'feature_code': 'PPL', 'country_code': 'CA', 'admin1_id': 6093943, 'timezone': 'America/Toronto', 'population': 346765, 'country_id': 6251999, 'country': 'Canada', 'admin1': 'Ontario'}, {'id': 4517009, 'name': 'London', 'latitude': 39.88645, 'longitude': -83.44825, 'elevation': 321.0, 'feature_code': 'PPLA2', 'country_code': 'US', 'admin1_id': 5165418, 'admin2_id': 4517365, 'admin3_id': 4517024, 'timezone': 'America/New_York', 'population': 10060, 'postcodes': ['43140'], 'country_id': 6252001, 'country': 'United States', 'admin1': 'Ohio', 'admin2': 'Madison', 'admin3': 'City of London'}, {'id': 4298960, 'name': 'London', 'latitude': 37.12898, 'longitude': -84.08326, 'elevation': 378.0, 'feature_code': 'PPLA2', 'country_code': 'US', 'admin1_id': 6254925, 'admin2_id': 4297480, 'timezone': 'America/New_York', 'population': 8126, 'postcodes': ['40741', '40742', '40743', '40744', '40745'], 'country_id': 6252001, 'country': 'United States', 'admin1': 'Kentucky', 'admin2': 'Laurel'}, {'id': 4119617, 'name': 'London', 'latitude': 35.32897, 'longitude': -93.25296, 'elevation': 116.0, 'feature_code': 'PPL', 'country_code': 'US', 'admin1_id': 4099753, 'admin2_id': 4127100, 'admin3_id': 4105863, 'timezone': 'America/Chicago', 'population': 1046, 'postcodes': ['72847'], 'country_id': 6252001, 'country': 'United States', 'admin1': 'Arkansas', 'admin2': 'Pope', 'admin3': 'Clark Township'}, {'id': 4707414, 'name': 'London', 'latitude': 30.67685, 'longitude': -99.57645, 'elevation': 519.0, 'feature_code': 'PPL', 'country_code': 'US', 'admin1_id': 4736286, 'admin2_id': 4703256, 'timezone': 'America/Chicago', 'population': 180, 'postcodes': ['76854'], 'country_id': 6252001, 'country': 'United States', 'admin1': 'Texas', 'admin2': 'Kimble'}, {'id': 4812926, 'name': 'London', 'latitude': 38.19455, 'longitude': -81.36872, 'elevation': 196.0, 'feature_code': 'PPL', 'country_code': 'US', 'admin1_id': 4826850, 'admin2_id': 4810630, 'timezone': 'America/New_York', 'postcodes': ['25126'], 'country_id': 6252001, 'country': 'United States', 'admin1': 'West Virginia', 'admin2': 'Kanawha'}, {'id': 5367815, 'name': 'London', 'latitude': 36.47606, 'longitude': -119.44318, 'elevation': 91.0, 'feature_code': 'PPL', 'country_code': 'US', 'admin1_id': 5332921, 'admin2_id': 5403789, 'timezone': 'America/Los_Angeles', 'population': 1869, 'country_id': 6252001, 'country': 'United States', 'admin1': 'California', 'admin2': 'Tulare'}, {'id': 4030939, 'name': 'London Village', 'latitude': 1.98487, 'longitude': -157.47502, 'elevation': 8.0, 'feature_code': 'PPL', 'country_code': 'KI', 'admin1_id': 4030940, 'admin2_id': 7521593, 'timezone': 'Pacific/Kiritimati', 'population': 1829, 'country_id': 4030945, 'country': 'Kiribati', 'admin1': 'Line Islands', 'admin2': 'Kiritimati'}, {'id': 982298, 'name': 'London', 'latitude': -24.81927, 'longitude': 31.04765, 'elevation': 698.0, 'feature_code': 'PPL', 'country_code': 'ZA', 'admin1_id': 1085595, 'admin2_id': 8299316, 'admin3_id': 8347523, 'timezone': 'Africa/Johannesburg', 'country_id': 953987, 'country': 'South Africa', 'admin1': 'Mpumalanga', 'admin2': 'Ehlanzeni District', 'admin3': 'Bushbuckridge'}]
        response = self.client.get('/api/search-geo/?name=London')
        self.assertEqual(
            response.json()['results'],
            result
        )

    def test_get_weather(self):
        london = json.dumps({
            "id": 2643743,
            "name": "London",
            "latitude": 51.50853,
            "longitude": -0.12574,
            "elevation": 25,
            "feature_code": "PPLC",
            "country_code": "GB",
            "admin1_id": 6269131,
            "admin2_id": 2648110,
            "timezone": "Europe/London",
            "population": 7556900,
            "country_id": 2635167,
            "country": "United Kingdom",
            "admin1": "England",
            "admin2": "Greater London"
        })
        response = self.client.get('/api/get-weather/?city=' + london)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/get-weather/')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/api/get-weather/?city=')
        self.assertEqual(response.status_code, 400)

    def test_get_stats(self):
        london = json.dumps({
            "id": 2643743,
            "name": "London",
            "latitude": 51.50853,
            "longitude": -0.12574,
            "elevation": 25,
            "feature_code": "PPLC",
            "country_code": "GB",
            "admin1_id": 6269131,
            "admin2_id": 2648110,
            "timezone": "Europe/London",
            "population": 7556900,
            "country_id": 2635167,
            "country": "United Kingdom",
            "admin1": "England",
            "admin2": "Greater London"
        })
        for _ in range(5):
            response = self.client.get('/api/get-weather/?city=' + london)

        result = [{'name': 'London', 'searchs': 5}]
        response = self.client.get('/api/get-stats/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), result)
