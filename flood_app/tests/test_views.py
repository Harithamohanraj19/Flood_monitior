from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch


class HomeViewTestCase(TestCase):
    def test_home_view(self):
       
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'items': [
                    {'@id': 'station_1', 'label': 'Station 1', 'stationReference': 'ref_1'},
                    {'@id': 'station_2', 'label': 'Station 2', 'stationReference': 'ref_2'}
                ]
            }

            response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('measure_values', response.context)
        measure_values = response.context['measure_values']
        self.assertEqual(len(measure_values), 2)
       

class GetStationDetailsViewTestCase(TestCase):
    def test_get_station_details_view(self):
        
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'items': [
                    {'@id': 'reading_1', 'dateTime': '2023-11-13T12:00:00Z', 'value': 10},
                    {'@id': 'reading_2', 'dateTime': '2023-11-13T13:00:00Z', 'value': 15}
                ]
            }

            response = self.client.get(reverse('get_station_details'), {'station': 'station_id'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'graph.html')
        self.assertIn('data', response.context)
        self.assertIn('graph_image', response.context)
        


