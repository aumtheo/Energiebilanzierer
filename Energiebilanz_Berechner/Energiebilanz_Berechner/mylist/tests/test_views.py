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
        response = self.client.get(reverse('wizard_allg'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'allg_angaben.html')
        self.assertIn('form', response.context)
        self.assertIn('orte', response.context)
    
    def test_allg_angaben_post_valid(self):
        """Test POST request with valid data to allg_angaben view."""
        data = {
            'name': 'Testgebäude',
            'laenge_ns': 20.0,
            'breite_ow': 15.0,
            'geschosshoehe': 3.0,
            'geschosse': 3
        }
        response = self.client.post(reverse('wizard_allg'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('wizard_energie'))
        
        # Check that the gebaeude was created
        self.assertEqual(Gebaeude.objects.count(), 1)
        gebaeude = Gebaeude.objects.first()
        self.assertEqual(gebaeude.name, 'Testgebäude')
        
        # Check that the gebaeude_id was stored in the session
        self.assertIn('geb_pk', self.client.session)
        self.assertEqual(self.client.session['geb_pk'], gebaeude.pk)
    
    def test_allg_angaben_post_invalid(self):
        """Test POST request with invalid data to allg_angaben view."""
        data = {
            'name': 'Testgebäude',
            'laenge_ns': -20.0,  # Negative value
            'breite_ow': 'abc',  # Non-numeric
            'geschosshoehe': 0,  # Zero height
            'geschosse': 0  # Zero floors
        }
        response = self.client.post(reverse('wizard_allg'), data)
        self.assertEqual(response.status_code, 200)  # Form redisplay
        self.assertTemplateUsed(response, 'allg_angaben.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        
        # Check that no gebaeude was created
        self.assertEqual(Gebaeude.objects.count(), 0)
    
    def test_energie_angaben_get_without_session(self):
        """Test GET request to energie_angaben view without session data."""
        response = self.client.get(reverse('wizard_energie'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('wizard_allg'))
    
    def test_energie_angaben_get_with_session(self):
        """Test GET request to energie_angaben view with session data."""
        # Create a gebaeude and store its ID in the session
        gebaeude = Gebaeude.objects.create(
            name='Testgebäude',
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3
        )
        session = self.client.session
        session['geb_pk'] = gebaeude.pk
        session.save()
        
        response = self.client.get(reverse('wizard_energie'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'energie_angaben.html')
        self.assertIn('form', response.context)
        self.assertIn('gebaeude', response.context)
        self.assertEqual(response.context['gebaeude'], gebaeude)
    
    def test_energie_angaben_post_valid(self):
        """Test POST request with valid data to energie_angaben view."""
        # Create a gebaeude and store its ID in the session
        gebaeude = Gebaeude.objects.create(
            name='Testgebäude',
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3
        )
        session = self.client.session
        session['geb_pk'] = gebaeude.pk
        session.save()
        
        data = {
            'jahres_heizwert': 10000.0,
            'tw_kwh_m2': 15.0,
            'luft_kwh_m2': 8.0,
            'bel_kwh_m2': 10.0,
            'nutz_kwh_m2': 5.0
        }
        response = self.client.post(reverse('wizard_energie'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('wizard_verluste'))
        
        # Check that the gebaeude was updated
        gebaeude.refresh_from_db()
        self.assertEqual(gebaeude.jahres_heizwert, 10000.0)
        self.assertEqual(gebaeude.tw_kwh_m2, 15.0)
        self.assertEqual(gebaeude.luft_kwh_m2, 8.0)
        self.assertEqual(gebaeude.bel_kwh_m2, 10.0)
        self.assertEqual(gebaeude.nutz_kwh_m2, 5.0)
    
    def test_verluste_angaben_post_valid(self):
        """Test POST request with valid data to verluste_angaben view."""
        # Create a gebaeude and store its ID in the session
        gebaeude = Gebaeude.objects.create(
            name='Testgebäude',
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3
        )
        session = self.client.session
        session['geb_pk'] = gebaeude.pk
        session.save()
        
        data = {
            'verteilungsverlust_kwh': 500.0,
            'speicherverlust_kwh': 300.0,
            'warmwasserbedarf_kwh': 2000.0
        }
        response = self.client.post(reverse('wizard_verluste'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('wizard_bauteile'))
        
        # Check that the gebaeude was updated
        gebaeude.refresh_from_db()
        self.assertEqual(gebaeude.verteilungsverlust_kwh, 500.0)
        self.assertEqual(gebaeude.speicherverlust_kwh, 300.0)
        self.assertEqual(gebaeude.warmwasserbedarf_kwh, 2000.0)
    
    def test_bauteile_angaben_post_valid(self):
        """Test POST request with valid data to bauteile_angaben view."""
        # Create a gebaeude and store its ID in the session
        gebaeude = Gebaeude.objects.create(
            name='Testgebäude',
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3
        )
        session = self.client.session
        session['geb_pk'] = gebaeude.pk
        session.save()
        
        data = {
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
        }
        response = self.client.post(reverse('wizard_bauteile'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('wizard_lueftung'))
        
        # Check that the bauteil was created
        self.assertEqual(Bauteil.objects.count(), 1)
        bauteil = Bauteil.objects.first()
        self.assertEqual(bauteil.laenge, 20.0)
        self.assertEqual(bauteil.breite, 15.0)
        self.assertEqual(bauteil.u_wand_nord, 0.24)
        
        # Check that the bauteil_id was stored in the session
        self.assertIn('teil_pk', self.client.session)
        self.assertEqual(self.client.session['teil_pk'], bauteil.pk)
        
        # Check that the calculated values were set
        self.assertEqual(bauteil.hoehe, 9.0)  # 3.0 * 3
        self.assertEqual(bauteil.volumen, 900.0)  # 20.0 * 15.0 * 3.0
        self.assertEqual(bauteil.bgf, 900.0)  # 20.0 * 15.0 * 3
        self.assertEqual(bauteil.nf, 720.0)  # 900.0 * 0.8
    
    def test_lueftung_angaben_post_valid(self):
        """Test POST request with valid data to lueftung_angaben view."""
        # Create a bauteil and store its ID in the session
        bauteil = Bauteil.objects.create(
            laenge=20.0,
            breite=15.0,
            geschosshoehe=3.0,
            anz_geschosse=3
        )
        session = self.client.session
        session['teil_pk'] = bauteil.pk
        session.save()
        
        data = {
            'lueftungstyp': 'Zentrale Lüftung',
            'luftwechselrate': 0.5,
            'wrg_wirkungsgrad': 80.0,
            'raum_temp_soll': 20.0,
            'laufzeit_hd': 12.0,
            'laufzeit_da': 365.0
        }
        response = self.client.post(reverse('wizard_lueftung'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('wizard_beleuchtung'))
        
        # Check that the bauteil was updated
        bauteil.refresh_from_db()
        self.assertEqual(bauteil.lueftungstyp, 'Zentrale Lüftung')
        self.assertEqual(bauteil.luftwechselrate, 0.5)
        self.assertEqual(bauteil.wrg_wirkungsgrad, 80.0)
        self.assertEqual(bauteil.raum_temp_soll, 20.0)
        self.assertEqual(bauteil.laufzeit_hd, 12.0)
        self.assertEqual(bauteil.laufzeit_da, 365.0)
    
    def test_beleuchtung_angaben_post_valid(self):
        """Test POST request with valid data to beleuchtung_angaben view."""
        # Create a gebaeude and store its ID in the session
        gebaeude = Gebaeude.objects.create(
            name='Testgebäude',
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3
        )
        session = self.client.session
        session['geb_pk'] = gebaeude.pk
        session.save()
        
        data = {
            'bereich': 'buero',
            'beleuchtungsart': 'LED',
            'regelungsart': 'Präsenzmelder',
            'e_soll': 500.0,
            'laufzeit_hd': 10.0,
            'laufzeit_da': 250.0
        }
        response = self.client.post(reverse('wizard_beleuchtung'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('wizard_gwp'))
        
        # Check that the beleuchtung was created
        self.assertEqual(Beleuchtung.objects.count(), 1)
        beleuchtung = Beleuchtung.objects.first()
        self.assertEqual(beleuchtung.bereich, 'buero')
        self.assertEqual(beleuchtung.beleuchtungsart, 'LED')
        self.assertEqual(beleuchtung.regelungsart, 'Präsenzmelder')
        self.assertEqual(beleuchtung.e_soll, 500.0)
        self.assertEqual(beleuchtung.laufzeit_hd, 10.0)
        self.assertEqual(beleuchtung.laufzeit_da, 250.0)
    
    def test_gwp_angaben_post_valid(self):
        """Test POST request with valid data to gwp_angaben view."""
        # Create a gebaeude and store its ID in the session
        gebaeude = Gebaeude.objects.create(
            name='Testgebäude',
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3
        )
        session = self.client.session
        session['geb_pk'] = gebaeude.pk
        session.save()
        
        data = {
            'gebaeude': gebaeude.pk,
            'variante': '300',
            'menge': 100.0,
            'spez_co2': 20.0
        }
        response = self.client.post(reverse('wizard_gwp'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('wizard_ergebnis'))
        
        # Check that the gwp_eingabe was created
        self.assertEqual(GwpEingabe.objects.count(), 1)
        gwp_eingabe = GwpEingabe.objects.first()
        self.assertEqual(gwp_eingabe.gebaeude, gebaeude)
        self.assertEqual(gwp_eingabe.variante, '300')
        self.assertEqual(gwp_eingabe.menge, 100.0)
        self.assertEqual(gwp_eingabe.spez_co2, 20.0)
    
    def test_wizard_ergebnis_without_session(self):
        """Test wizard_ergebnis view without session data."""
        response = self.client.get(reverse('wizard_ergebnis'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('wizard_allg'))
    
    def test_wizard_ergebnis_with_session(self):
        """Test wizard_ergebnis view with session data."""
        # Create a gebaeude and bauteil and store their IDs in the session
        gebaeude = Gebaeude.objects.create(
            name='Testgebäude',
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3,
            jahres_heizwert=10000.0,
            tw_kwh_m2=15.0,
            luft_kwh_m2=8.0,
            bel_kwh_m2=10.0,
            nutz_kwh_m2=5.0,
            verteilungsverlust_kwh=500.0,
            speicherverlust_kwh=300.0,
            warmwasserbedarf_kwh=2000.0
        )
        bauteil = Bauteil.objects.create(
            laenge=20.0,
            breite=15.0,
            geschosshoehe=3.0,
            anz_geschosse=3,
            hoehe=9.0,
            volumen=900.0,
            bgf=900.0,
            nf=720.0
        )
        session = self.client.session
        session['geb_pk'] = gebaeude.pk
        session['teil_pk'] = bauteil.pk
        session.save()
        
        response = self.client.get(reverse('wizard_ergebnis'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ergebnis.html')
        self.assertIn('gebaeude', response.context)
        self.assertIn('bauteil', response.context)
        self.assertIn('nutzenergie', response.context)
        self.assertIn('strombedarf', response.context)
        self.assertIn('waermebedarf', response.context)
        self.assertIn('endenergie', response.context)
        
        # Check that the bauteil was updated with calculation results
        bauteil.refresh_from_db()
        self.assertIsNotNone(bauteil.ne_absolut)
        self.assertIsNotNone(bauteil.ne_spez)
        self.assertIsNotNone(bauteil.sb_absolut)
        self.assertIsNotNone(bauteil.sb_spez)
        self.assertIsNotNone(bauteil.wb_absolut)
        self.assertIsNotNone(bauteil.ee_absolut)
        self.assertIsNotNone(bauteil.ee_spez)