from django.test import TestCase, Client
from django.urls import reverse
import json

class ApiTest(TestCase):
    """Test the API endpoints."""
    
    def setUp(self):
        self.client = Client()
    
    def test_api_berechnung_with_valid_data(self):
        """Test the api_berechnung view with valid data."""
        # Prepare query parameters
        params = {
            'laenge': 20.0,
            'breite': 15.0,
            'geschosshoehe': 3.0,
            'anz_geschosse': 3,
            'jahres_heizbedarf': 10000.0,
            'tw_pro_m2': 15.0,
            'lwt_pro_m2': 8.0,
            'bel_pro_m2': 10.0,
            'nutzer_pro_m2': 5.0,
            'verlust_verteilung': 500.0,
            'verlust_speicher': 300.0,
            'ww_warmwasser': 2000.0
        }
        
        # Make the API request
        response = self.client.get('/api/berechnung/', params)
        
        # Check response status and content type
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Parse the JSON response
        data = json.loads(response.content)
        
        # Check that the response contains all expected keys
        self.assertIn('gebaeudedaten', data)
        self.assertIn('nutzenergie', data)
        self.assertIn('strombedarf', data)
        self.assertIn('waermebedarf', data)
        self.assertIn('endenergie', data)
        
        # Check gebaeudedaten
        gebaeudedaten = data['gebaeudedaten']
        self.assertIn('hoehe', gebaeudedaten)
        self.assertIn('volumen', gebaeudedaten)
        self.assertIn('bgf', gebaeudedaten)
        self.assertIn('nf', gebaeudedaten)
        
        # Check calculated values
        self.assertEqual(gebaeudedaten['hoehe'], 9.0)  # 3.0 * 3
        self.assertEqual(gebaeudedaten['volumen'], 900.0)  # 20.0 * 15.0 * 9.0
        self.assertEqual(gebaeudedaten['bgf'], 900.0)  # 20.0 * 15.0 * 3
        self.assertEqual(gebaeudedaten['nf'], 720.0)  # 900.0 * 0.8
        
        # Check nutzenergie
        nutzenergie = data['nutzenergie']
        self.assertIn('ne_absolut', nutzenergie)
        self.assertIn('ne_spezifisch', nutzenergie)
        
        # Check strombedarf
        strombedarf = data['strombedarf']
        self.assertIn('sb_absolut', strombedarf)
        self.assertIn('sb_spezifisch', strombedarf)
        
        # Check waermebedarf
        waermebedarf = data['waermebedarf']
        self.assertIn('wb_absolut', waermebedarf)
        
        # Check endenergie
        endenergie = data['endenergie']
        self.assertIn('ee_absolut', endenergie)
        self.assertIn('ee_spezifisch', endenergie)
        
        # Check calculated values
        expected_ne_absolut = 10000.0 + (15.0 + 8.0 + 10.0 + 5.0) * 720.0
        self.assertAlmostEqual(nutzenergie['ne_absolut'], expected_ne_absolut, delta=0.1)
        self.assertAlmostEqual(nutzenergie['ne_spezifisch'], expected_ne_absolut / 720.0, delta=0.1)
        
        expected_sb_absolut = (15.0 + 8.0 + 10.0 + 5.0) * 720.0
        self.assertAlmostEqual(strombedarf['sb_absolut'], expected_sb_absolut, delta=0.1)
        self.assertAlmostEqual(strombedarf['sb_spezifisch'], expected_sb_absolut / 720.0, delta=0.1)
        
        expected_wb_absolut = 10000.0 + 500.0 + 300.0 + 2000.0
        self.assertAlmostEqual(waermebedarf['wb_absolut'], expected_wb_absolut, delta=0.1)
        
        expected_ee_absolut = expected_sb_absolut + expected_wb_absolut
        self.assertAlmostEqual(endenergie['ee_absolut'], expected_ee_absolut, delta=0.1)
        self.assertAlmostEqual(endenergie['ee_spezifisch'], expected_ee_absolut / 720.0, delta=0.1)
    
    def test_api_berechnung_with_invalid_data(self):
        """Test the api_berechnung view with invalid data."""
        # Prepare query parameters with invalid values
        params = {
            'laenge': 'abc',  # Non-numeric
            'breite': -15.0,  # Negative value
            'geschosshoehe': 0,  # Zero height
            'anz_geschosse': 'invalid',  # Non-numeric
            'jahres_heizbedarf': 'xyz',  # Non-numeric
            'tw_pro_m2': -15.0,  # Negative value
            'lwt_pro_m2': 'invalid',  # Non-numeric
            'bel_pro_m2': -10.0,  # Negative value
            'nutzer_pro_m2': 'abc',  # Non-numeric
            'verlust_verteilung': 'invalid',  # Non-numeric
            'verlust_speicher': -300.0,  # Negative value
            'ww_warmwasser': 'xyz'  # Non-numeric
        }
        
        # Make the API request
        response = self.client.get('/api/berechnung/', params)
        
        # Check response status and content type
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Parse the JSON response
        data = json.loads(response.content)
        
        # Check that the response contains all expected keys
        self.assertIn('gebaeudedaten', data)
        self.assertIn('nutzenergie', data)
        self.assertIn('strombedarf', data)
        self.assertIn('waermebedarf', data)
        self.assertIn('endenergie', data)
        
        # Check that the calculated values are all 0 or close to 0
        gebaeudedaten = data['gebaeudedaten']
        self.assertAlmostEqual(gebaeudedaten['hoehe'], 0.0, delta=0.1)
        self.assertAlmostEqual(gebaeudedaten['volumen'], 0.0, delta=0.1)
        self.assertAlmostEqual(gebaeudedaten['bgf'], 0.0, delta=0.1)
        self.assertAlmostEqual(gebaeudedaten['nf'], 0.0, delta=0.1)
        
        nutzenergie = data['nutzenergie']
        self.assertAlmostEqual(nutzenergie['ne_absolut'], 0.0, delta=0.1)
        
        strombedarf = data['strombedarf']
        self.assertAlmostEqual(strombedarf['sb_absolut'], 0.0, delta=0.1)
        
        waermebedarf = data['waermebedarf']
        self.assertAlmostEqual(waermebedarf['wb_absolut'], 0.0, delta=0.1)
        
        endenergie = data['endenergie']
        self.assertAlmostEqual(endenergie['ee_absolut'], 0.0, delta=0.1)