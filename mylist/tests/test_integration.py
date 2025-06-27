from django.test import TestCase, Client
from django.urls import reverse
from mylist.models import (
    Gebaeude,
    Bauteil,
    Beleuchtung,
    Waermequelle,
    GwpEingabe,
    SonneneintragsParameter,
    SonnenschutzFaktor
)

class LiveApiIntegrationTest(TestCase):
    """Integration test for the live API functionality."""
    
    def setUp(self):
        self.client = Client()
    
    def test_api_calculation_flow(self):
        """Test the API calculation flow with different parameter sets."""
        # Test with basic building parameters
        params = {
            'laenge': 20.0,
            'breite': 15.0,
            'geschosshoehe': 3.0,
            'anz_geschosse': 3
        }
        response = self.client.get('/api/berechnung/', params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['gebaeudedaten']['hoehe'], 9.0)
        self.assertEqual(data['gebaeudedaten']['volumen'], 900.0)
        self.assertEqual(data['gebaeudedaten']['bgf'], 900.0)
        self.assertEqual(data['gebaeudedaten']['nf'], 720.0)
        
        # Test with added energy parameters
        params.update({
            'jahres_heizbedarf': 10000.0,
            'tw_pro_m2': 15.0,
            'lwt_pro_m2': 8.0,
            'bel_pro_m2': 10.0,
            'nutzer_pro_m2': 5.0
        })
        response = self.client.get('/api/berechnung/', params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        expected_ne_absolut = 10000.0 + (15.0 + 8.0 + 10.0 + 5.0) * 720.0
        self.assertAlmostEqual(data['nutzenergie']['ne_absolut'], expected_ne_absolut, delta=0.1)
        self.assertAlmostEqual(data['nutzenergie']['ne_spezifisch'], expected_ne_absolut / 720.0, delta=0.1)
        
        expected_sb_absolut = (15.0 + 8.0 + 10.0 + 5.0) * 720.0
        self.assertAlmostEqual(data['strombedarf']['sb_absolut'], expected_sb_absolut, delta=0.1)
        self.assertAlmostEqual(data['strombedarf']['sb_spezifisch'], expected_sb_absolut / 720.0, delta=0.1)
        
        # Test with added loss parameters
        params.update({
            'verlust_verteilung': 500.0,
            'verlust_speicher': 300.0,
            'ww_warmwasser': 2000.0
        })
        response = self.client.get('/api/berechnung/', params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        expected_wb_absolut = 10000.0 + 500.0 + 300.0 + 2000.0
        self.assertAlmostEqual(data['waermebedarf']['wb_absolut'], expected_wb_absolut, delta=0.1)
        
        expected_ee_absolut = expected_sb_absolut + expected_wb_absolut
        self.assertAlmostEqual(data['endenergie']['ee_absolut'], expected_ee_absolut, delta=0.1)
        self.assertAlmostEqual(data['endenergie']['ee_spezifisch'], expected_ee_absolut / 720.0, delta=0.1)