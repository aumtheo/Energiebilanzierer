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

class WizardViewsTest(TestCase):
    """Test the wizard flow views."""
    
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
    
    def test_startseite_view(self):
        """Test the startseite view."""
        response = self.client.get(reverse('startseite'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'startseite.html')
    
    def test_allg_angaben_get(self):
        """Test GET request to allg_angaben view."""
        response = self.client.get(reverse('allg_angaben'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'allg_angaben.html')
        self.assertIn('orte', response.context)
    
    def test_baukrper_view(self):
        """Test the baukrper view."""
        response = self.client.get(reverse('baukrper'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'baukrper.html')
    
    def test_bauteil_view(self):
        """Test the bauteil view."""
        response = self.client.get(reverse('bauteil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bauteil.html')
    
    def test_pv_view(self):
        """Test the pv view."""
        response = self.client.get(reverse('pv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pv.html')
    
    def test_lftung_view(self):
        """Test the lftung view."""
        response = self.client.get(reverse('lftung'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lftung.html')
    
    def test_beleuchtung_view(self):
        """Test the beleuchtung view."""
        response = self.client.get(reverse('beleuchtung'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'beleuchtung.html')
    
    def test_beleuchtung_2_view(self):
        """Test the beleuchtung_2 view."""
        response = self.client.get(reverse('beleuchtung_2'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'beleuchtung_2.html')
    
    def test_waermequellen_view(self):
        """Test the waermequellen view."""
        response = self.client.get(reverse('waermequellen'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wrmequellen.html')
    
    def test_sdf_view(self):
        """Test the sdf view."""
        response = self.client.get(reverse('sdf'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sdf.html')
    
    def test_gwp_view(self):
        """Test the gwp view."""
        response = self.client.get(reverse('gwp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gwp.html')
    
    def test_ergebnis_view(self):
        """Test the ergebnis view."""
        response = self.client.get(reverse('ergebnis'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ergebnis.html')
    
    def test_baukoerper_kp_view(self):
        """Test the baukoerper_kp view."""
        response = self.client.get(reverse('baukoerper_kp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'baukrper_kp.html')
    
    def test_baukrper_kp_2_view(self):
        """Test the baukrper_kp_2 view."""
        response = self.client.get(reverse('baukrper_kp_2'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'baukrper_kp_2.html')
    
    def test_bauteil_kp_view(self):
        """Test the bauteil_kp view."""
        response = self.client.get(reverse('bauteil_kp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bauteil_kp.html')
    
    def test_uber_tool_view(self):
        """Test the uber_tool view."""
        response = self.client.get(reverse('uber_tool'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uber_tool.html')
    
    def test_entwicklerteam_view(self):
        """Test the entwicklerteam view."""
        response = self.client.get(reverse('entwicklerteam'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entwicklerteam.html')
    
    def test_kontakt_view(self):
        """Test the kontakt view."""
        response = self.client.get(reverse('kontakt'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kontakt.html')
    
    def test_hilfe_view(self):
        """Test the hilfe view."""
        response = self.client.get(reverse('hilfe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hilfe.html')