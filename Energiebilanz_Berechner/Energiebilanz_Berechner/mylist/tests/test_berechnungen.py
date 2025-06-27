from django.test import TestCase
from mylist.berechnungen import (
    berechne_gebaeudedaten,
    berechne_nutzenergiebedarf,
    berechne_strombedarf,
    berechne_waermebedarf,
    berechne_endenergiebedarf
)

class BerechnungenTest(TestCase):
    """Test the calculation functions."""
    
    def test_berechne_gebaeudedaten(self):
        """Test the berechne_gebaeudedaten function."""
        # Test with valid data
        result = berechne_gebaeudedaten(20.0, 15.0, 3.0, 3)
        self.assertEqual(result['hoehe'], 9.0)  # 3.0 * 3
        self.assertEqual(result['volumen'], 900.0)  # 20.0 * 15.0 * 9.0
        self.assertEqual(result['bgf'], 900.0)  # 20.0 * 15.0 * 3
        self.assertEqual(result['nf'], 720.0)  # 900.0 * 0.8
        
        # Test with zero values
        result = berechne_gebaeudedaten(0.0, 0.0, 0.0, 0)
        self.assertEqual(result['hoehe'], 0.0)
        self.assertEqual(result['volumen'], 0.0)
        self.assertEqual(result['bgf'], 0.0)
        self.assertEqual(result['nf'], 0.0)
        
        # Test with negative values (should be handled gracefully)
        result = berechne_gebaeudedaten(-20.0, -15.0, -3.0, -3)
        self.assertEqual(result['hoehe'], -9.0)  # -3.0 * -3
        self.assertEqual(result['volumen'], -900.0)  # -20.0 * -15.0 * -9.0
        self.assertEqual(result['bgf'], 900.0)  # -20.0 * -15.0 * -3
        self.assertEqual(result['nf'], 720.0)  # 900.0 * 0.8
    
    def test_berechne_nutzenergiebedarf(self):
        """Test the berechne_nutzenergiebedarf function."""
        # Test with valid data
        result = berechne_nutzenergiebedarf(
            nf_m2=720.0,
            jahres_heizwaermebedarf_kwh=10000.0,
            trinkwarmwasser_kwh_pro_m2=15.0,
            luftfoerderung_kwh_pro_m2=8.0,
            beleuchtung_kwh_pro_m2=10.0,
            nutzer_pro_m2=5.0
        )
        expected_ne_absolut = 10000.0 + (15.0 + 8.0 + 10.0 + 5.0) * 720.0
        self.assertAlmostEqual(result['ne_absolut'], expected_ne_absolut, delta=0.1)
        self.assertAlmostEqual(result['ne_spezifisch'], expected_ne_absolut / 720.0, delta=0.1)
        
        # Test with zero values
        result = berechne_nutzenergiebedarf(
            nf_m2=0.0,
            jahres_heizwaermebedarf_kwh=0.0,
            trinkwarmwasser_kwh_pro_m2=0.0,
            luftfoerderung_kwh_pro_m2=0.0,
            beleuchtung_kwh_pro_m2=0.0,
            nutzer_pro_m2=0.0
        )
        self.assertEqual(result['ne_absolut'], 0.0)
        self.assertEqual(result['ne_spezifisch'], 0.0)
        
        # Test with negative values (should be handled gracefully)
        result = berechne_nutzenergiebedarf(
            nf_m2=-720.0,
            jahres_heizwaermebedarf_kwh=-10000.0,
            trinkwarmwasser_kwh_pro_m2=-15.0,
            luftfoerderung_kwh_pro_m2=-8.0,
            beleuchtung_kwh_pro_m2=-10.0,
            nutzer_pro_m2=-5.0
        )
        expected_ne_absolut = -10000.0 + (-15.0 + -8.0 + -10.0 + -5.0) * -720.0
        self.assertAlmostEqual(result['ne_absolut'], expected_ne_absolut, delta=0.1)
        self.assertAlmostEqual(result['ne_spezifisch'], expected_ne_absolut / -720.0, delta=0.1)
    
    def test_berechne_strombedarf(self):
        """Test the berechne_strombedarf function."""
        # Test with valid data
        result = berechne_strombedarf(
            nf_m2=720.0,
            trinkwarmwasser_kwh_pro_m2=15.0,
            luftfoerderung_kwh_pro_m2=8.0,
            beleuchtung_kwh_pro_m2=10.0,
            nutzer_pro_m2=5.0
        )
        expected_sb_absolut = (15.0 + 8.0 + 10.0 + 5.0) * 720.0
        self.assertAlmostEqual(result['sb_absolut'], expected_sb_absolut, delta=0.1)
        self.assertAlmostEqual(result['sb_spezifisch'], expected_sb_absolut / 720.0, delta=0.1)
        
        # Test with zero values
        result = berechne_strombedarf(
            nf_m2=0.0,
            trinkwarmwasser_kwh_pro_m2=0.0,
            luftfoerderung_kwh_pro_m2=0.0,
            beleuchtung_kwh_pro_m2=0.0,
            nutzer_pro_m2=0.0
        )
        self.assertEqual(result['sb_absolut'], 0.0)
        self.assertEqual(result['sb_spezifisch'], 0.0)
        
        # Test with negative values (should be handled gracefully)
        result = berechne_strombedarf(
            nf_m2=-720.0,
            trinkwarmwasser_kwh_pro_m2=-15.0,
            luftfoerderung_kwh_pro_m2=-8.0,
            beleuchtung_kwh_pro_m2=-10.0,
            nutzer_pro_m2=-5.0
        )
        expected_sb_absolut = (-15.0 + -8.0 + -10.0 + -5.0) * -720.0
        self.assertAlmostEqual(result['sb_absolut'], expected_sb_absolut, delta=0.1)
        self.assertAlmostEqual(result['sb_spezifisch'], expected_sb_absolut / -720.0, delta=0.1)
    
    def test_berechne_waermebedarf(self):
        """Test the berechne_waermebedarf function."""
        # Test with valid data
        result = berechne_waermebedarf(
            jahres_heizwaermebedarf_kwh=10000.0,
            verteilungsverlust_kwh=500.0,
            speicherverlust_kwh=300.0,
            warmwasserbedarf_kwh=2000.0
        )
        expected_wb_absolut = 10000.0 + 500.0 + 300.0 + 2000.0
        self.assertEqual(result['wb_absolut'], expected_wb_absolut)
        
        # Test with zero values
        result = berechne_waermebedarf(
            jahres_heizwaermebedarf_kwh=0.0,
            verteilungsverlust_kwh=0.0,
            speicherverlust_kwh=0.0,
            warmwasserbedarf_kwh=0.0
        )
        self.assertEqual(result['wb_absolut'], 0.0)
        
        # Test with negative values (should be handled gracefully)
        result = berechne_waermebedarf(
            jahres_heizwaermebedarf_kwh=-10000.0,
            verteilungsverlust_kwh=-500.0,
            speicherverlust_kwh=-300.0,
            warmwasserbedarf_kwh=-2000.0
        )
        expected_wb_absolut = -10000.0 + -500.0 + -300.0 + -2000.0
        self.assertEqual(result['wb_absolut'], expected_wb_absolut)
    
    def test_berechne_endenergiebedarf(self):
        """Test the berechne_endenergiebedarf function."""
        # Test with valid data
        sb = {'sb_absolut': 27360.0, 'sb_spezifisch': 38.0}
        wb = {'wb_absolut': 12800.0}
        result = berechne_endenergiebedarf(720.0, sb, wb)
        expected_ee_absolut = 27360.0 + 12800.0
        self.assertEqual(result['ee_absolut'], expected_ee_absolut)
        self.assertEqual(result['ee_spezifisch'], expected_ee_absolut / 720.0)
        
        # Test with zero values
        sb = {'sb_absolut': 0.0, 'sb_spezifisch': 0.0}
        wb = {'wb_absolut': 0.0}
        result = berechne_endenergiebedarf(0.0, sb, wb)
        self.assertEqual(result['ee_absolut'], 0.0)
        self.assertEqual(result['ee_spezifisch'], 0.0)
        
        # Test with negative values (should be handled gracefully)
        sb = {'sb_absolut': -27360.0, 'sb_spezifisch': -38.0}
        wb = {'wb_absolut': -12800.0}
        result = berechne_endenergiebedarf(-720.0, sb, wb)
        expected_ee_absolut = -27360.0 + -12800.0
        self.assertEqual(result['ee_absolut'], expected_ee_absolut)
        self.assertEqual(result['ee_spezifisch'], expected_ee_absolut / -720.0)