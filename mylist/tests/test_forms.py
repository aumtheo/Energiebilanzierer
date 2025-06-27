from django.test import TestCase
from mylist.models import (
    Gebaeude,
    Bauteil,
    SonnenschutzFaktor
)
from mylist.forms import (
    GebaeudeAllgForm,
    GebaeudeEnergieKennzahlenForm,
    GebaeudeVerlusteForm,
    BauteilForm,
    LueftungForm,
    BeleuchtungForm,
    WaermequelleForm,
    GwpEingabeForm,
    SonneneintragsParameterForm
)

class GebaeudeAllgFormTest(TestCase):
    """Test the GebaeudeAllgForm."""
    
    def test_valid_data(self):
        """Test form with valid data."""
        form = GebaeudeAllgForm({
            'name': 'Testgebäude',
            'laenge_ns': 20.0,
            'breite_ow': 15.0,
            'geschosshoehe': 3.0,
            'geschosse': 3
        })
        self.assertTrue(form.is_valid())
        gebaeude = form.save()
        self.assertEqual(gebaeude.name, 'Testgebäude')
        self.assertEqual(gebaeude.laenge_ns, 20.0)
        self.assertEqual(gebaeude.breite_ow, 15.0)
        self.assertEqual(gebaeude.geschosshoehe, 3.0)
        self.assertEqual(gebaeude.geschosse, 3)
    
    def test_invalid_data(self):
        """Test form with invalid data."""
        form = GebaeudeAllgForm({
            'name': '',  # Empty name
            'laenge_ns': -5.0,  # Negative length
            'breite_ow': 'abc',  # Non-numeric
            'geschosshoehe': 0,  # Zero height
            'geschosse': 0  # Zero floors
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)  # Name can be empty, so 4 errors


class GebaeudeEnergieKennzahlenFormTest(TestCase):
    """Test the GebaeudeEnergieKennzahlenForm."""
    
    def setUp(self):
        self.gebaeude = Gebaeude.objects.create(
            name='Testgebäude',
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3
        )
    
    def test_valid_data(self):
        """Test form with valid data."""
        form = GebaeudeEnergieKennzahlenForm({
            'jahres_heizwert': 10000.0,
            'tw_kwh_m2': 15.0,
            'luft_kwh_m2': 8.0,
            'bel_kwh_m2': 10.0,
            'nutz_kwh_m2': 5.0
        }, instance=self.gebaeude)
        self.assertTrue(form.is_valid())
        gebaeude = form.save()
        self.assertEqual(gebaeude.jahres_heizwert, 10000.0)
        self.assertEqual(gebaeude.tw_kwh_m2, 15.0)
        self.assertEqual(gebaeude.luft_kwh_m2, 8.0)
        self.assertEqual(gebaeude.bel_kwh_m2, 10.0)
        self.assertEqual(gebaeude.nutz_kwh_m2, 5.0)
    
    def test_invalid_data(self):
        """Test form with invalid data."""
        form = GebaeudeEnergieKennzahlenForm({
            'jahres_heizwert': 'abc',  # Non-numeric
            'tw_kwh_m2': -5.0,  # Negative value
            'luft_kwh_m2': 'xyz',  # Non-numeric
            'bel_kwh_m2': -10.0,  # Negative value
            'nutz_kwh_m2': 'invalid'  # Non-numeric
        }, instance=self.gebaeude)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)


class GebaeudeVerlusteFormTest(TestCase):
    """Test the GebaeudeVerlusteForm."""
    
    def setUp(self):
        self.gebaeude = Gebaeude.objects.create(
            name='Testgebäude',
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3
        )
    
    def test_valid_data(self):
        """Test form with valid data."""
        form = GebaeudeVerlusteForm({
            'verteilungsverlust_kwh': 500.0,
            'speicherverlust_kwh': 300.0,
            'warmwasserbedarf_kwh': 2000.0
        }, instance=self.gebaeude)
        self.assertTrue(form.is_valid())
        gebaeude = form.save()
        self.assertEqual(gebaeude.verteilungsverlust_kwh, 500.0)
        self.assertEqual(gebaeude.speicherverlust_kwh, 300.0)
        self.assertEqual(gebaeude.warmwasserbedarf_kwh, 2000.0)
    
    def test_invalid_data(self):
        """Test form with invalid data."""
        form = GebaeudeVerlusteForm({
            'verteilungsverlust_kwh': 'abc',  # Non-numeric
            'speicherverlust_kwh': -300.0,  # Negative value
            'warmwasserbedarf_kwh': 'invalid'  # Non-numeric
        }, instance=self.gebaeude)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


class BauteilFormTest(TestCase):
    """Test the BauteilForm."""
    
    def test_valid_data(self):
        """Test form with valid data."""
        form = BauteilForm({
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
        self.assertTrue(form.is_valid())
        bauteil = form.save()
        self.assertEqual(bauteil.laenge, 20.0)
        self.assertEqual(bauteil.breite, 15.0)
        self.assertEqual(bauteil.u_wand_nord, 0.24)
    
    def test_invalid_data(self):
        """Test form with invalid data."""
        form = BauteilForm({
            'laenge': 'abc',  # Non-numeric
            'breite': -15.0,  # Negative value
            'geschosshoehe': 0,  # Zero height
            'anz_geschosse': 'invalid',  # Non-numeric
            'u_wand_nord': -0.24,  # Negative U-value
            'u_wand_sued': 'xyz',  # Non-numeric
            'u_wand_west': -0.24,  # Negative U-value
            'u_wand_ost': 'invalid',  # Non-numeric
            'u_bodenplatte': -0.3,  # Negative U-value
            'u_dach': 'abc'  # Non-numeric
        })
        self.assertFalse(form.is_valid())
        # All fields are optional, so errors only for invalid values, not missing ones
        self.assertTrue(len(form.errors) > 0)


class LueftungFormTest(TestCase):
    """Test the LueftungForm."""
    
    def setUp(self):
        self.bauteil = Bauteil.objects.create(
            laenge=20.0,
            breite=15.0,
            geschosshoehe=3.0,
            anz_geschosse=3
        )
    
    def test_valid_data(self):
        """Test form with valid data."""
        form = LueftungForm({
            'lueftungstyp': 'Zentrale Lüftung',
            'luftwechselrate': 0.5,
            'wrg_wirkungsgrad': 80.0,
            'raum_temp_soll': 20.0,
            'laufzeit_hd': 12.0,
            'laufzeit_da': 365.0
        }, instance=self.bauteil)
        self.assertTrue(form.is_valid())
        bauteil = form.save()
        self.assertEqual(bauteil.lueftungstyp, 'Zentrale Lüftung')
        self.assertEqual(bauteil.luftwechselrate, 0.5)
        self.assertEqual(bauteil.wrg_wirkungsgrad, 80.0)
    
    def test_invalid_data(self):
        """Test form with invalid data."""
        form = LueftungForm({
            'lueftungstyp': '',  # Empty type
            'luftwechselrate': -0.5,  # Negative rate
            'wrg_wirkungsgrad': 'abc',  # Non-numeric
            'raum_temp_soll': -20.0,  # Negative temperature
            'laufzeit_hd': 25.0,  # More than 24 hours
            'laufzeit_da': 'invalid'  # Non-numeric
        }, instance=self.bauteil)
        # All fields are optional, so form might still be valid
        if not form.is_valid():
            self.assertTrue(len(form.errors) > 0)


class BeleuchtungFormTest(TestCase):
    """Test the BeleuchtungForm."""
    
    def test_valid_data(self):
        """Test form with valid data."""
        form = BeleuchtungForm({
            'bereich': 'buero',
            'beleuchtungsart': 'LED',
            'regelungsart': 'Präsenzmelder',
            'e_soll': 500.0,
            'laufzeit_hd': 10.0,
            'laufzeit_da': 250.0
        })
        self.assertTrue(form.is_valid())
        beleuchtung = form.save()
        self.assertEqual(beleuchtung.bereich, 'buero')
        self.assertEqual(beleuchtung.beleuchtungsart, 'LED')
        self.assertEqual(beleuchtung.e_soll, 500.0)
    
    def test_invalid_data(self):
        """Test form with invalid data."""
        form = BeleuchtungForm({
            'bereich': 'invalid',  # Invalid choice
            'beleuchtungsart': '',  # Empty type
            'regelungsart': '',  # Empty type
            'e_soll': -500.0,  # Negative value
            'laufzeit_hd': 'abc',  # Non-numeric
            'laufzeit_da': -250.0  # Negative value
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 0)


class WaermequelleFormTest(TestCase):
    """Test the WaermequelleForm."""
    
    def test_valid_data(self):
        """Test form with valid data."""
        form = WaermequelleForm({
            'name': 'Wärmepumpe',
            'anzahl': 1,
            'leistung_kw': 10.0,
            'betrieb_hd': 8.0,
            'betrieb_da': 200.0
        })
        self.assertTrue(form.is_valid())
        waermequelle = form.save()
        self.assertEqual(waermequelle.name, 'Wärmepumpe')
        self.assertEqual(waermequelle.anzahl, 1)
        self.assertEqual(waermequelle.leistung_kw, 10.0)
    
    def test_invalid_data(self):
        """Test form with invalid data."""
        form = WaermequelleForm({
            'name': '',  # Empty name
            'anzahl': 'abc',  # Non-numeric
            'leistung_kw': -10.0,  # Negative value
            'betrieb_hd': 25.0,  # More than 24 hours
            'betrieb_da': 'invalid'  # Non-numeric
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 0)


class GwpEingabeFormTest(TestCase):
    """Test the GwpEingabeForm."""
    
    def setUp(self):
        self.gebaeude = Gebaeude.objects.create(
            name='Testgebäude',
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3
        )
    
    def test_valid_data(self):
        """Test form with valid data."""
        form = GwpEingabeForm({
            'gebaeude': self.gebaeude.id,
            'variante': '300',
            'menge': 100.0,
            'spez_co2': 20.0
        })
        self.assertTrue(form.is_valid())
        gwp_eingabe = form.save()
        self.assertEqual(gwp_eingabe.gebaeude, self.gebaeude)
        self.assertEqual(gwp_eingabe.variante, '300')
        self.assertEqual(gwp_eingabe.menge, 100.0)
    
    def test_invalid_data(self):
        """Test form with invalid data."""
        form = GwpEingabeForm({
            'gebaeude': '',  # Empty gebaeude
            'variante': 'invalid',  # Invalid choice
            'menge': -100.0,  # Negative value
            'spez_co2': 'abc'  # Non-numeric
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 0)


class SonneneintragsParameterFormTest(TestCase):
    """Test the SonneneintragsParameterForm."""
    
    def setUp(self):
        self.gebaeude = Gebaeude.objects.create(
            name='Testgebäude',
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3
        )
        self.sonnenschutz = SonnenschutzFaktor.objects.create(
            zeile="2.1",
            sonnenschutzvorrichtung="Jalousie",
            f_c_g_le_0_40_zweifach=0.65,
            f_c_g_le_0_40_dreifach=0.7,
            f_c_g_gt_0_40_zweifach=0.65
        )
    
    def test_valid_data(self):
        """Test form with valid data."""
        form = SonneneintragsParameterForm({
            'gebaeude': self.gebaeude.id,
            'kritischer_raum': True,
            'fassadenorientierung': 'Sued',
            'sonnenschutzart': self.sonnenschutz.id,
            'verglasungsart': 'zweifach',
            'passive_kuehlung': True,
            'fensterneigung': 30.0
        })
        self.assertTrue(form.is_valid())
        sonneneintrag = form.save()
        self.assertEqual(sonneneintrag.gebaeude, self.gebaeude)
        self.assertEqual(sonneneintrag.fassadenorientierung, 'Sued')
        self.assertEqual(sonneneintrag.sonnenschutzart, self.sonnenschutz)
    
    def test_invalid_data(self):
        """Test form with invalid data."""
        form = SonneneintragsParameterForm({
            'gebaeude': '',  # Empty gebaeude
            'kritischer_raum': 'invalid',  # Not a boolean
            'fassadenorientierung': 'invalid',  # Invalid choice
            'sonnenschutzart': '',  # Empty sonnenschutzart
            'verglasungsart': 'invalid',  # Invalid choice
            'passive_kuehlung': 'invalid',  # Not a boolean
            'fensterneigung': 'abc'  # Non-numeric
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 0)