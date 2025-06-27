from django.test import TestCase
from mylist.models import (
    Gebaeude,
    Bauteil,
    Beleuchtung,
    Waermequelle,
    GwpEingabe,
    SonneneintragsParameter,
    SonnenschutzFaktor
)

class GebaeudeModelTest(TestCase):
    """Test the Gebaeude model."""
    
    def setUp(self):
        self.gebaeude = Gebaeude.objects.create(
            name="Testgebäude",
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
    
    def test_gebaeude_creation(self):
        """Test that a Gebaeude instance can be created."""
        self.assertTrue(isinstance(self.gebaeude, Gebaeude))
        self.assertEqual(self.gebaeude.name, "Testgebäude")
    
    def test_gebaeude_str(self):
        """Test the string representation of a Gebaeude instance."""
        self.assertEqual(str(self.gebaeude), f"Gebäude {self.gebaeude.id} – Testgebäude")


class BauteilModelTest(TestCase):
    """Test the Bauteil model."""
    
    def setUp(self):
        self.bauteil = Bauteil.objects.create(
            laenge=20.0,
            breite=15.0,
            geschosshoehe=3.0,
            anz_geschosse=3,
            u_wand_nord=0.24,
            u_wand_sued=0.24,
            u_wand_west=0.24,
            u_wand_ost=0.24,
            u_bodenplatte=0.3,
            u_dach=0.2,
            hoehe=9.0,
            volumen=900.0,
            bgf=300.0,
            nf=240.0,
            lueftungstyp="Zentrale Lüftung",
            luftwechselrate=0.5,
            wrg_wirkungsgrad=80.0,
            raum_temp_soll=20.0,
            laufzeit_hd=12.0,
            laufzeit_da=365.0
        )
    
    def test_bauteil_creation(self):
        """Test that a Bauteil instance can be created."""
        self.assertTrue(isinstance(self.bauteil, Bauteil))
        self.assertEqual(self.bauteil.lueftungstyp, "Zentrale Lüftung")
    
    def test_bauteil_str(self):
        """Test the string representation of a Bauteil instance."""
        expected = f"Bauteil #{self.bauteil.id} – erstellt am {self.bauteil.created_at:%Y-%m-%d}"
        self.assertEqual(str(self.bauteil), expected)


class BeleuchtungModelTest(TestCase):
    """Test the Beleuchtung model."""
    
    def setUp(self):
        self.beleuchtung = Beleuchtung.objects.create(
            bereich="buero",
            beleuchtungsart="LED",
            regelungsart="Präsenzmelder",
            e_soll=500.0,
            laufzeit_hd=10.0,
            laufzeit_da=250.0
        )
    
    def test_beleuchtung_creation(self):
        """Test that a Beleuchtung instance can be created."""
        self.assertTrue(isinstance(self.beleuchtung, Beleuchtung))
        self.assertEqual(self.beleuchtung.beleuchtungsart, "LED")
    
    def test_beleuchtung_str(self):
        """Test the string representation of a Beleuchtung instance."""
        self.assertEqual(str(self.beleuchtung), "Büro – LED")


class WaermequelleModelTest(TestCase):
    """Test the Waermequelle model."""
    
    def setUp(self):
        self.waermequelle = Waermequelle.objects.create(
            name="Wärmepumpe",
            anzahl=1,
            leistung_kw=10.0,
            betrieb_hd=8.0,
            betrieb_da=200.0
        )
    
    def test_waermequelle_creation(self):
        """Test that a Waermequelle instance can be created."""
        self.assertTrue(isinstance(self.waermequelle, Waermequelle))
        self.assertEqual(self.waermequelle.name, "Wärmepumpe")
    
    def test_waermequelle_str(self):
        """Test the string representation of a Waermequelle instance."""
        self.assertEqual(str(self.waermequelle), "Wärmepumpe")


class GwpEingabeModelTest(TestCase):
    """Test the GwpEingabe model."""
    
    def setUp(self):
        self.gebaeude = Gebaeude.objects.create(
            name="Testgebäude",
            laenge_ns=20.0,
            breite_ow=15.0,
            geschosshoehe=3.0,
            geschosse=3
        )
        self.gwp_eingabe = GwpEingabe.objects.create(
            gebaeude=self.gebaeude,
            variante="300",
            menge=100.0,
            spez_co2=20.0
        )
    
    def test_gwp_eingabe_creation(self):
        """Test that a GwpEingabe instance can be created."""
        self.assertTrue(isinstance(self.gwp_eingabe, GwpEingabe))
        self.assertEqual(self.gwp_eingabe.variante, "300")
    
    def test_gwp_eingabe_str(self):
        """Test the string representation of a GwpEingabe instance."""
        self.assertEqual(str(self.gwp_eingabe), f"{self.gebaeude} / Var. {self.gwp_eingabe.variante}")


class SonneneintragsParameterModelTest(TestCase):
    """Test the SonneneintragsParameter model."""
    
    def setUp(self):
        self.gebaeude = Gebaeude.objects.create(
            name="Testgebäude",
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
        self.sonneneintrag = SonneneintragsParameter.objects.create(
            gebaeude=self.gebaeude,
            kritischer_raum=True,
            fassadenorientierung="Sued",
            sonnenschutzart=self.sonnenschutz,
            verglasungsart="zweifach",
            passive_kuehlung=True,
            fensterneigung=30.0
        )
    
    def test_sonneneintrag_creation(self):
        """Test that a SonneneintragsParameter instance can be created."""
        self.assertTrue(isinstance(self.sonneneintrag, SonneneintragsParameter))
        self.assertEqual(self.sonneneintrag.fassadenorientierung, "Sued")
    
    def test_sonneneintrag_str(self):
        """Test the string representation of a SonneneintragsParameter instance."""
        self.assertEqual(str(self.sonneneintrag), f"{self.gebaeude} – {self.sonneneintrag.fassadenorientierung}")