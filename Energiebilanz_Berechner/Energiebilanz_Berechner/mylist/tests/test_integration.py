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

class WizardFlowIntegrationTest(TestCase):
    """Integration test for the complete wizard flow."""
    
    def setUp(self):
        self.client = Client()
        
        # Create a test sonnenschutz for later use
        self.sonnenschutz = SonnenschutzFaktor.objects.create(
            zeile="2.1",
            sonnenschutzvorrichtung="Jalousie",
            f_c_g_le_0_40_zweifach=0.65,
            f_c_g_le_0_40_dreifach=0.7,
            f_c_g_gt_0_40_zweifach=0.65
        )
    
    def test_complete_wizard_flow(self):
        """Test the complete wizard flow from start to finish."""
        # Step 1: Allgemeine Angaben
        response = self.client.post(reverse('wizard_allg'), {
            'name': 'Testgebäude',
            'laenge_ns': 20.0,
            'breite_ow': 15.0,
            'geschosshoehe': 3.0,
            'geschosse': 3
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('wizard_energie'))
        
        # Check that the gebaeude was created
        self.assertEqual(Gebaeude.objects.count(), 1)
        gebaeude = Gebaeude.objects.first()
        
        # Step 2: Energiekennzahlen
        response = self.client.post(reverse('wizard_energie'), {
            'jahres_heizwert': 10000.0,
            'tw_kwh_m2': 15.0,
            'luft_kwh_m2': 8.0,
            'bel_kwh_m2': 10.0,
            'nutz_kwh_m2': 5.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('wizard_verluste'))
        
        # Step 3: Verluste & WW-Bedarf
        response = self.client.post(reverse('wizard_verluste'), {
            'verteilungsverlust_kwh': 500.0,
            'speicherverlust_kwh': 300.0,
            'warmwasserbedarf_kwh': 2000.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('wizard_bauteile'))
        
        # Step 4: Bauteil-Daten
        response = self.client.post(reverse('wizard_bauteile'), {
            'laenge': 20.0,
            'breite': 15.0,
            'geschosshoehe': 3.0,
            'anz_geschosse': 3,
            'u_wand_nord': 0.24,
            'u_wand_sued': 0.24,
            'u_wand_west': 0.24,
            'u_wand_ost': 0.24,
            'u_bodenplatte': 0.3,
            'u_dach': 0.2
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('wizard_lueftung'))
        
        # Check that the bauteil was created
        self.assertEqual(Bauteil.objects.count(), 1)
        bauteil = Bauteil.objects.first()
        
        # Step 5: Lüftung
        response = self.client.post(reverse('wizard_lueftung'), {
            'lueftungstyp': 'Zentrale Lüftung',
            'luftwechselrate': 0.5,
            'wrg_wirkungsgrad': 80.0,
            'raum_temp_soll': 20.0,
            'laufzeit_hd': 12.0,
            'laufzeit_da': 365.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('wizard_beleuchtung'))
        
        # Step 6: Beleuchtung
        response = self.client.post(reverse('wizard_beleuchtung'), {
            'bereich': 'buero',
            'beleuchtungsart': 'LED',
            'regelungsart': 'Präsenzmelder',
            'e_soll': 500.0,
            'laufzeit_hd': 10.0,
            'laufzeit_da': 250.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('wizard_gwp'))
        
        # Check that the beleuchtung was created
        self.assertEqual(Beleuchtung.objects.count(), 1)
        
        # Step 7: GWP
        response = self.client.post(reverse('wizard_gwp'), {
            'gebaeude': gebaeude.pk,
            'variante': '300',
            'menge': 100.0,
            'spez_co2': 20.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('wizard_ergebnis'))
        
        # Check that the gwp_eingabe was created
        self.assertEqual(GwpEingabe.objects.count(), 1)
        
        # Step 8: Ergebnis
        response = self.client.get(reverse('wizard_ergebnis'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ergebnis.html')
        
        # Check that the bauteil was updated with calculation results
        bauteil.refresh_from_db()
        self.assertIsNotNone(bauteil.ne_absolut)
        self.assertIsNotNone(bauteil.ne_spez)
        self.assertIsNotNone(bauteil.sb_absolut)
        self.assertIsNotNone(bauteil.sb_spez)
        self.assertIsNotNone(bauteil.wb_absolut)
        self.assertIsNotNone(bauteil.ee_absolut)
        self.assertIsNotNone(bauteil.ee_spez)
        
        # Check that the calculated values are correct
        expected_ne_absolut = 10000.0 + (15.0 + 8.0 + 10.0 + 5.0) * 720.0
        self.assertAlmostEqual(bauteil.ne_absolut, expected_ne_absolut, delta=0.1)
        self.assertAlmostEqual(bauteil.ne_spez, expected_ne_absolut / 720.0, delta=0.1)
        
        expected_sb_absolut = (15.0 + 8.0 + 10.0 + 5.0) * 720.0
        self.assertAlmostEqual(bauteil.sb_absolut, expected_sb_absolut, delta=0.1)
        self.assertAlmostEqual(bauteil.sb_spez, expected_sb_absolut / 720.0, delta=0.1)
        
        expected_wb_absolut = 10000.0 + 500.0 + 300.0 + 2000.0
        self.assertAlmostEqual(bauteil.wb_absolut, expected_wb_absolut, delta=0.1)
        
        expected_ee_absolut = expected_sb_absolut + expected_wb_absolut
        self.assertAlmostEqual(bauteil.ee_absolut, expected_ee_absolut, delta=0.1)
        self.assertAlmostEqual(bauteil.ee_spez, expected_ee_absolut / 720.0, delta=0.1)


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