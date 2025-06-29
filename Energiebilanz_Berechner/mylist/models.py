from django.db import models
from datetime import date 

class BuildingProject(models.Model):
    standort        = models.CharField("Standort", max_length=100)
    laenge_ns       = models.FloatField("Länge Nord/Süd (m)")
    breite_ow       = models.FloatField("Breite Ost/West (m)")
    geschosshoehe   = models.FloatField("Geschosshoehe (m)")
    geschosse       = models.IntegerField("Anzahl Geschosse")
    fenster_nord    = models.FloatField("Fenster Nord (%)", default=0)
    fenster_sued    = models.FloatField("Fenster Süd (%)", default=0)
    fenster_ost     = models.FloatField("Fenster Ost (%)", default=0)
    fenster_west    = models.FloatField("Fenster West (%)", default=0)
    fenster_dach    = models.FloatField("Fenster Dach (%)", default=0)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Projekt {self.pk} – {self.standort}"
    
class Gebaeude(models.Model):
    # 1) Geometrie (Wizard‐Schritt „allg. Angaben")
    name = models.CharField(max_length=200, blank=True)
    laenge_ns = models.FloatField(help_text="Länge Nord/Süd in m")
    breite_ow = models.FloatField(help_text="Breite Ost/West in m")
    geschosshoehe = models.FloatField(help_text="Geschosshöhe in m")
    geschosse = models.IntegerField(help_text="Anzahl Geschosse")

    # 2) Primäre Energiekennzahlen (Wizard-Schritt „Wärme" / „Bauteile")
    jahres_heizwert = models.FloatField(
        help_text="Heizwärmebedarf absolut (kWh/Jahr)", default=0
    )
    tw_kwh_m2 = models.FloatField(
        help_text="Warmwasserbedarf in kWh/m² (spezifisch)", default=0
    )
    luft_kwh_m2 = models.FloatField(
        help_text="Lüftungsenergiebedarf in kWh/m² (spezifisch)", default=0
    )
    bel_kwh_m2 = models.FloatField(
        help_text="Beleuchtungsenergiebedarf in kWh/m² (spezifisch)", default=0
    )
    nutz_kwh_m2 = models.FloatField(
        help_text="Nutzer/Prozessenergie in kWh/m² (spezifisch)", default=0
    )

    # 3) Verluste (aus Bauteil-Berechnung oder Wizard-Schritt „Bauteile")
    verteilungsverlust_kwh = models.FloatField(
        help_text="Verteilungsverluste (kWh/Jahr)", default=0
    )
    speicherverlust_kwh = models.FloatField(
        help_text="Speicherverluste (kWh/Jahr)", default=0
    )

    # 4) Platzhalter für thermischen Warmwasserbedarf (falls gesondert berechnet)
    warmwasserbedarf_kwh = models.FloatField(
        help_text="Thermischer Warmwasserbedarf (kWh/Jahr)", default=0
    )

    # 5) (Später könnten noch Felder für Bauteil-GWP, GWP_Betrieb etc. dazukommen.)

    def __str__(self):
        return f"Gebäude {self.id} – {self.name or 'ohne Namen'}"
    
    class TrinkwarmwasserKennwert(models.Model):

        nutzung = models.CharField(
            max_length=100,
            help_text="z. B. 'Bürogebäude', 'Schule mit Duschen' usw."
        )
        nutzungsbezogen_kwh_pro_einheit_und_tag = models.FloatField(
            help_text="z. B. 0,4 kWh je Person/Tag oder 6 kWh je Bett/Tag"
        )
        flaechenbezogen_wh_m2_pro_tag = models.FloatField(
            help_text="z. B. 30 Wh/(m²·d), 500 Wh/(m²·d) etc."
        )
        bezugsflaeche = models.CharField(
            max_length=100,
            help_text="z. B. 'Bürofläche', 'Klassenräume', 'Hotelzimmer' etc."
        )
        spitzenzapfungen_pro_tag = models.PositiveSmallIntegerField(
            help_text="Anzahl der Spitzenzapfungen pro Tag (n_SP)"
        )

        class Meta:
            verbose_name = "Trinkwarmwasser-Richtwert"
            verbose_name_plural = "Trinkwarmwasser-Richtwerte"

        def __str__(self):
            return f"{self.nutzung} – {self.flaechenbezogen_wh_m2_pro_tag} Wh/(m²·d)"



#
# 2) Tabelle A14 – Richtwerte für Bauteildruckverluste in Lüftungssystemen (DIN EN 13779)
#
class DruckverlustLueftung(models.Model):
    """
    Bauteil-Druckverluste (Tabelle A14).
    Spalten:
      - bauteil:
      - druckverlust_niedrig  (Float, Pa)
      - druckverlust_normal   (Float, Pa)
      - druckverlust_hoch     (Float, Pa)
    """

    bauteil = models.CharField(
        max_length=100,
        help_text="z. B. 'Zulufkanalsystem', 'Erhitzer', 'Kühler', 'WRG-Einheit Klasse H3' etc."
    )
    druckverlust_niedrig = models.FloatField(
        help_text="Druckverlust (niedrig) in Pa"
    )
    druckverlust_normal = models.FloatField(
        help_text="Druckverlust (normal) in Pa"
    )
    druckverlust_hoch = models.FloatField(
        help_text="Druckverlust (hoch) in Pa"
    )

    class Meta:
        verbose_name = "Druckverlust Lüftung"
        verbose_name_plural = "Druckverluste Lüftung"

    def __str__(self):
        return f"{self.bauteil} – Normal: {self.druckverlust_normal} Pa"



#
# 3) Tabelle E.1 – Mittlere Außenlufttemperaturen der Referenzorte
#
class KlimaregionTemperatur(models.Model):
    """
    Mittlere monatliche Außentemperaturen (Tabelle E.1).
    Spalten:
      - region:      Klimaregion (z. B. 1,2,3...)
      - referenzort: z. B. 'Bremerhaven', 'Hamburg', 'Mannheim' usw.
      - jan – dez:   mittlere Temperatur (Float) für jeden Monat (°C)
      - jahreswert:  Jahresmitteltemperatur (°C)
    """

    region = models.PositiveSmallIntegerField(
        help_text="Zahlenwert der Klimaregion (1 bis 15)"
    )
    referenzort = models.CharField(
        max_length=50,
        help_text="Name des Wetter-Referenzorts (z. B. 'Bremen', 'Mannheim' etc.)"
    )
    jan = models.FloatField(help_text="Mittlere Temperatur Jan (°C)")
    feb = models.FloatField(help_text="Mittlere Temperatur Feb (°C)")
    maer = models.FloatField(help_text="Mittlere Temperatur Mär (°C)")
    apr = models.FloatField(help_text="Mittlere Temperatur Apr (°C)")
    mai = models.FloatField(help_text="Mittlere Temperatur Mai (°C)")
    jun = models.FloatField(help_text="Mittlere Temperatur Jun (°C)")
    jul = models.FloatField(help_text="Mittlere Temperatur Jul (°C)")
    aug = models.FloatField(help_text="Mittlere Temperatur Aug (°C)")
    sep = models.FloatField(help_text="Mittlere Temperatur Sep (°C)")
    okt = models.FloatField(help_text="Mittlere Temperatur Okt (°C)")
    nov = models.FloatField(help_text="Mittlere Temperatur Nov (°C)")
    dez = models.FloatField(help_text="Mittlere Temperatur Dez (°C)")
    jahreswert = models.FloatField(
        help_text="Jahresmitteltemperatur θₑ (°C), Jan bis Dez"
    )

    class Meta:
        verbose_name = "Klimaregion-Temperatur"
        verbose_name_plural = "Klimaregion-Temperaturen"
        unique_together = ("region", "referenzort")

    def __str__(self):
        return f"Reg. {self.region} – {self.referenzort}"



#
# 4) Tabelle E.13 – Mittlere monatliche Strahlungsintensitäten pro Referenzort
#
class SolarStrahlungMonat(models.Model):
    """
    Mittlere Strahlungsintensität (Tabelle E.13) für eine Referenzregion.
    Spalten:
      - region_id:   Integer (z. B. 11=Fichtelberg, 12=Mannheim, …)
      - orientierung: String (z. B. 'Horizontal', 'Süd', 'Ost', …)
      - neigung:     Integer (Neigungswinkel in °, z. B. 0, 30, 45, 60, 90)
      - jan – dez:   mittlere Strahlungsintensität (W/m²) pro Monat
      - jahreswert:  Jahresstrahlung (kWh/(m²·a))
    """

    region_id = models.PositiveSmallIntegerField(
        help_text="Numerische Kennung der Region (z. B. 11 für Fichtelberg)"
    )
    orientierung = models.CharField(
        max_length=20,
        help_text="z. B. 'Horizontal', 'Süd', 'Süd-Ost', 'Ost', 'West' etc."
    )
    neigung = models.PositiveSmallIntegerField(
        help_text="Neigungswinkel gegenüber der Horizontalen (z. B. 0, 30, 45, 60, 90)"
    )

    jan = models.FloatField(help_text="Strahlungsintensität Jan (W/m²)")
    feb = models.FloatField(help_text="Strahlungsintensität Feb (W/m²)")
    maer = models.FloatField(help_text="Strahlungsintensität Mär (W/m²)")
    apr = models.FloatField(help_text="Strahlungsintensität Apr (W/m²)")
    mai = models.FloatField(help_text="Strahlungsintensität Mai (W/m²)")
    jun = models.FloatField(help_text="Strahlungsintensität Jun (W/m²)")
    jul = models.FloatField(help_text="Strahlungsintensität Jul (W/m²)")
    aug = models.FloatField(help_text="Strahlungsintensität Aug (W/m²)")
    sep = models.FloatField(help_text="Strahlungsintensität Sep (W/m²)")
    okt = models.FloatField(help_text="Strahlungsintensität Okt (W/m²)")
    nov = models.FloatField(help_text="Strahlungsintensität Nov (W/m²)")
    dez = models.FloatField(help_text="Strahlungsintensität Dez (W/m²)")
    jahreswert = models.FloatField(
        help_text="Jahresstrahlung in kWh/(m²·a) für die gesamte Orientierung/Neigung"
    )

    class Meta:
        verbose_name = "Monatliche Solar-Strahlung"
        verbose_name_plural = "Monatliche Solar-Strahlungsdaten"
        unique_together = ("region_id", "orientierung", "neigung")

    def __str__(self):
        return f"Region {self.region_id} – {self.orientierung} {self.neigung}°"



#
# 5) Tabelle 7 (Anhang) – Anhaltswerte Abminderungsfaktoren Fc für Sonnenschutzvorrichtungen
#
class SonnenschutzFaktor(models.Model):
    """
    Anhaltswerte Abminderungsfaktoren Fc (Tabelle 7, Sonnenschutz, Anhang).
    Spalten:
      - zeilennr:                z. B. '2.1', '3.1.2' etc. (CharField)
      - beschreibung:            z. B. 'Jalousie, 45° Lamellenstellung' etc.
      - fc_g_le0_4_dreifach:     Float (Fc bei g ≤ 0,4 und Dreifachverglasung)
      - fc_g_le0_4_zweifach:     Float (Fc bei g ≤ 0,4 und Zweifachverglasung)
      - fc_g_gt0_4_dreifach:     Float (Fc bei g > 0,4 und Dreifachverglasung)
      - fc_g_gt0_4_zweifach:     Float (Fc bei g > 0,4 und Zweifachverglasung)
    """

    zeilennr = models.CharField(
        max_length=10,
        help_text="z. B. '3.2.1' (Jalousie 45°), '3.1.2' (Rollladen geschlossen) etc."
    )
    beschreibung = models.CharField(
        max_length=100,
        help_text="Beschreibung der Sonnenschutzvorrichtung"
    )
    fc_g_le0_4_dreifach = models.FloatField(
        default=1.0,
        help_text="Fc-Wert für g ≤ 0,4 bei Dreifachverglasung"
    )
    fc_g_le0_4_zweifach = models.FloatField(
        default=1.0,
        help_text="Fc-Wert für g ≤ 0,4 bei Zweifachverglasung"
    )
    fc_g_gt0_4_dreifach = models.FloatField(
        default=1.0,
        help_text="Fc-Wert für g > 0,4 bei Dreifachverglasung"
    )
    fc_g_gt0_4_zweifach = models.FloatField(
        default=1.0,
        help_text="Fc-Wert für g > 0,4 bei Zweifachverglasung"
    )

    class Meta:
        verbose_name = "Sonnenschutz-Faktor"
        verbose_name_plural = "Sonnenschutz-Faktoren"
        unique_together = ("zeilennr", "beschreibung")

    def __str__(self):
        return f"{self.zeilennr} – {self.beschreibung}"



#
# 6) (Optional) Tabelle 8 – Anteilige Sonneneintragskennwerte (Si) nach Region und Bauart
#
#    Diese Tabelle ist sehr komplex aufgebaut (mehrstufige Untertabellen S1–S6).
#    Im einfachsten Fall legen wir ein Modell an, das pro „Si-Gruppe" alle Klimaregionen für Wohnen/Nichtwohnen verwaltet.
#
class AnteiligeSonneneintragskennwerte(models.Model):
    """
    Tabelle 8 – Anhaltswerte S_i (anteilige Sonneneintragskennwerte) 
    für Wohn- und Nichtwohngebäude. 
    Felder:
      - si_gruppe: z. B. 'S1', 'S2', 'S3', 'S4', 'S5', 'S6'
      - beschreibung: z. B. 'ohne Nachtlüftung, leichte Bauart'
      - klimaregion:  z. B. 'A', 'B', 'C'
      - typ_gebaeude: 'Wohngebäude' oder 'Nichtwohngebäude'
      - wert:         Float (z. B. 0.071, 0.13 etc.)
    """
    SI_CHOICES = [
        ('S1', 'Nachtlüftung und Bauart'),
        ('S2', 'Grundflächenbezogener Fensterflächenanteil'),
        ('S3', 'Sonnenschutzglas'),
        ('S4', 'Fensterneigung'),
        ('S5', 'Orientierung'),
        ('S6', 'Einsatz passiver Kühlung'),
    ]
    TYP_CHOICES = [
        ('W', 'Wohngebäude'),
        ('N', 'Nichtwohngebäude'),
    ]
    KLIMAREGION_CHOICES = [
        ('A', 'KlimaRegion A'),
        ('B', 'KlimaRegion B'),
        ('C', 'KlimaRegion C'),
    ]

    si_gruppe = models.CharField(
        max_length=2,
        choices=SI_CHOICES,
        help_text="Z.B. 'S1', 'S2', ... 'S6'"
    )
    beschreibung = models.CharField(
        max_length=100,
        help_text="z. B. 'ohne Nachtlüftung, leichte Bauart' oder 'hoch Nachtlüftung, schwere Bauart' etc."
    )
    klimaregion = models.CharField(
        max_length=1,
        choices=KLIMAREGION_CHOICES,
        help_text="KlimaRegion: 'A', 'B' oder 'C'"
    )
    typ_gebaeude = models.CharField(
        max_length=1,
        choices=TYP_CHOICES,
        help_text="Gebäudetyp: 'W' = Wohngebäude, 'N' = Nichtwohngebäude"
    )
    wert = models.FloatField(
        help_text="Anteiliges Sonneneintragskennwert S₁ … S₆"
    )

    class Meta:
        verbose_name = "Anteiliger Sonneneintragskennwert"
        verbose_name_plural = "Anteilige Sonneneintragskennwerte"
        unique_together = ("si_gruppe", "beschreibung", "klimaregion", "typ_gebaeude")

    def __str__(self):
        return f"{self.si_gruppe} | {self.beschreibung[:20]}… | {self.klimaregion} | {self.typ_gebaeude} → {self.wert}"
    # mylist/models.py


class KlimaregionTemperatur(models.Model):
    region = models.PositiveSmallIntegerField(
        unique=True,
        help_text="Nummer der Klimaregion (z. B. 1 für Bremerhaven, 2 für Rostock, …)."
    )
    referenzort = models.CharField(
        max_length=100,
        help_text="Name des Referenzortes, z. B. 'Bremerhaven', 'Rostock' usw."
    )
    jan = models.FloatField(help_text="Mittlere Temperatur im Januar (°C)")
    feb = models.FloatField(help_text="Mittlere Temperatur im Februar (°C)")
    maer = models.FloatField(verbose_name="März", help_text="Mittlere Temperatur im März (°C)")
    apr = models.FloatField(help_text="Mittlere Temperatur im April (°C)")
    mai = models.FloatField(help_text="Mittlere Temperatur im Mai (°C)")
    jun = models.FloatField(help_text="Mittlere Temperatur im Juni (°C)")
    jul = models.FloatField(help_text="Mittlere Temperatur im Juli (°C)")
    aug = models.FloatField(help_text="Mittlere Temperatur im August (°C)")
    sep = models.FloatField(help_text="Mittlere Temperatur im September (°C)")
    okt = models.FloatField(help_text="Mittlere Temperatur im Oktober (°C)")
    nov = models.FloatField(help_text="Mittlere Temperatur im November (°C)")
    dez = models.FloatField(help_text="Mittlere Temperatur im Dezember (°C)")
    jahreswert = models.FloatField(help_text="Jahresmitteltemperatur (°C)")

    def __str__(self):
        return f"{self.region} – {self.referenzort}"

class DruckverlustBauteil(models.Model):
    bauteil = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name des Bauteils (z. B. 'Erhitzer', 'Kühler' usw.)"
    )
    druckverlust_pa = models.PositiveIntegerField(
        help_text="Druckverlust (Pa) bei Normalzustand"
    )

    def __str__(self):
        return f"{self.bauteil} – {self.druckverlust_pa} Pa"
    
class SonnenschutzFaktor(models.Model):
    zeile = models.CharField(
        max_length=10,
        unique=True,
        help_text="Zeilennummer (z. B. '2.1', '3.1.2' …)",
        default=""      # einfacher Default für neue und bereits vorhandene Zeilen
    )
    sonnenschutzvorrichtung = models.CharField(
        max_length=200,
        help_text="Beschreibung der Sonnenschutzeinrichtung",
        default=""      # Default‐Text, falls altes Objekt keinen Wert hat
    )
    f_c_g_le_0_40_zweifach = models.FloatField(
        help_text="Abminderungsfaktor bei g ≤ 0,40 (zweifach)",
        default=1.0     # Default, falls alte Zeilen keinen Wert haben
    )
    f_c_g_le_0_40_dreifach = models.FloatField(
        help_text="Abminderungsfaktor bei g ≤ 0,40 (dreifach)",
        default=1.0     # Default, falls alte Zeilen keinen Wert haben
    )
    f_c_g_gt_0_40_zweifach = models.FloatField(
        help_text="Abminderungsfaktor bei g > 0,40 (zweifach)",
        default=1.0     # Default, falls alte Zeilen keinen Wert haben
    )

    def __str__(self):
        return f"{self.zeile} – {self.sonnenschutzvorrichtung}"
    


class Temperaturkorrekturfaktor(models.Model):
    """
    Beinhaltet pro Bauteil den Temperatur-Korrekturfaktor Fx.
    """
    bauteil = models.CharField(
        max_length=200,
        unique=True,
        help_text="Name des Bauteils (z. B. 'Außenwand, Fenster, Decke über Außenluft')."
    )
    fx = models.FloatField(
        help_text="Temperaturkorrekturfaktor Fx (z. B. 1.0, 0.8, 0.35 …)."
    )

    def __str__(self):
        return f"{self.bauteil} → Fx = {self.fx}",


class SolarStrahlungMonat(models.Model):
    orientierung = models.CharField(max_length=50)   # z.B. "Süd", "Ost" …
    neigung      = models.CharField(max_length=10)   # z.B. "30°", "45°" …
    jan          = models.FloatField(null=True, blank=True)
    feb          = models.FloatField(null=True, blank=True)
    maerz        = models.FloatField(null=True, blank=True)
    apr          = models.FloatField(null=True, blank=True)
    mai          = models.FloatField(null=True, blank=True)
    jun          = models.FloatField(null=True, blank=True)
    jul          = models.FloatField(null=True, blank=True)
    aug          = models.FloatField(null=True, blank=True)
    sep          = models.FloatField(null=True, blank=True)
    okt          = models.FloatField(null=True, blank=True)
    nov          = models.FloatField(null=True, blank=True)
    dez          = models.FloatField(null=True, blank=True)
    jahreswert   = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.orientierung} / {self.neigung}"

    class Meta:
        verbose_name = "Solare Strahlung pro Monat"
        verbose_name_plural = "Solare Strahlung"
        # Hier stellen wir sicher, dass pro (orientierung, neigung) nur ein Eintrag existiert:
        unique_together = (('orientierung', 'neigung'),)

class SonneneintragsKennwert(models.Model):
    # Beispiel-Felder entsprechend den Spalten eurer CSV
    typ           = models.CharField(max_length=10)      # z.B. "S1", "S2" etc.
    kennwert_key  = models.CharField(max_length=50, unique=True)
    beschreibung  = models.CharField(max_length=200, null=True, blank=True)
    bauart        = models.CharField(max_length=50, null=True, blank=True)

    wohng_A       = models.FloatField(null=True, blank=True)
    wohng_B       = models.FloatField(null=True, blank=True)
    wohng_C       = models.FloatField(null=True, blank=True)
    nw_A          = models.FloatField(null=True, blank=True)
    nw_B          = models.FloatField(null=True, blank=True)
    nw_C          = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Sonneneintragskennwert"
        verbose_name_plural = "Sonneneintragskennwerte"
        ordering = ['typ', 'bauart', 'kennwert_key']

    def __str__(self):
        # Damit im Admin und in Dropdowns eine aussagekräftige Beschriftung erscheint:
        if self.bauart:
            return f"{self.typ} – {self.bauart} – {self.beschreibung}"
        return f"{self.typ} – {self.beschreibung}"

class Bauteil(models.Model):
    # — Eingabefelder —
    laenge         = models.FloatField(null=True, blank=True)
    breite         = models.FloatField(null=True, blank=True)
    geschosshoehe  = models.FloatField(null=True, blank=True)
    anz_geschosse  = models.IntegerField(null=True, blank=True)

    # … (Deine Fenster- und U-Werte-Felder) …
    u_wand_nord    = models.FloatField(null=True, blank=True)
    u_wand_sued    = models.FloatField(null=True, blank=True)
    u_wand_west    = models.FloatField(null=True, blank=True)
    u_wand_ost     = models.FloatField(null=True, blank=True)
    u_bodenplatte  = models.FloatField(null=True, blank=True)
    u_dach         = models.FloatField(null=True, blank=True)

    # — Berechnungsergebnisse —
    hoehe          = models.FloatField(null=True, blank=True)
    volumen        = models.FloatField(null=True, blank=True)
    bgf            = models.FloatField(null=True, blank=True)
    nf             = models.FloatField(null=True, blank=True)

    ne_absolut     = models.FloatField(null=True, blank=True)
    ne_spez        = models.FloatField(null=True, blank=True)

    sb_absolut     = models.FloatField(null=True, blank=True)
    sb_spez        = models.FloatField(null=True, blank=True)

    wb_absolut     = models.FloatField(null=True, blank=True)

    ee_absolut     = models.FloatField(null=True, blank=True)
    ee_spez        = models.FloatField(null=True, blank=True)

    created_at     = models.DateTimeField(auto_now_add=True)

    lb_absolut     = models.FloatField("Lüftungswärmebedarf (kWh)", null=True, blank=True)
    lb_spezifisch  = models.FloatField("Lüftungsbedarf spezifisch (kWh/m²)", null=True, blank=True)
    
    lueftungstyp       = models.CharField("Lüftungstyp", max_length=100, null=True, blank=True)
    luftwechselrate    = models.FloatField("Luftwechselrate (1/h)", null=True, blank=True)
    wrg_wirkungsgrad   = models.FloatField("WRG-Wirkungsgrad (%)", null=True, blank=True)
    raum_temp_soll     = models.FloatField("Raum-Soll-Temperatur (°C)", null=True, blank=True)
    laufzeit_hd        = models.FloatField("Betriebsstunden h/d", null=True, blank=True)
    laufzeit_da        = models.FloatField("Betriebstage d/a", null=True, blank=True)

    # — schon vorhandene Eingabefelder —
    laenge         = models.FloatField(null=True, blank=True)
    breite         = models.FloatField(null=True, blank=True)
    geschosshoehe  = models.FloatField(null=True, blank=True)
    anz_geschosse  = models.IntegerField(null=True, blank=True)

    # … (deine U-Wert-Felder) …

    # — LUFTUNGSEINGABEN — neu hinzufügen:
    lueftungstyp       = models.CharField(
        max_length=100,
        help_text="Art der Lüftung (z.B. dezentral, zentral)",
        null=True, blank=True
    )
    luftwechselrate   = models.FloatField(
        help_text="Luftwechselrate (1/h)",
        null=True, blank=True
    )
    wrg_wirkungsgrad   = models.FloatField(
        help_text="Wirkungsgrad der Wärmerückgewinnung (%)",
        null=True, blank=True
    )
    raum_temp_soll     = models.FloatField(
        help_text="Soll-Temperatur im Raum (°C)",
        null=True, blank=True
    )
    laufzeit_hd        = models.FloatField(
        help_text="Betriebszeit pro Tag (h/d)",
        null=True, blank=True
    )
    laufzeit_da        = models.FloatField(
        help_text="Betriebszeit pro Jahr (d/a)",
        null=True, blank=True
    )

    # — schon vorhandene Ergebnis-Felder —
    hoehe          = models.FloatField(null=True, blank=True)
    volumen        = models.FloatField(null=True, blank=True)
    bgf            = models.FloatField(null=True, blank=True)
    nf             = models.FloatField(null=True, blank=True)
    ne_absolut     = models.FloatField(null=True, blank=True)
    ne_spez        = models.FloatField(null=True, blank=True)
    sb_absolut     = models.FloatField(null=True, blank=True)
    sb_spez        = models.FloatField(null=True, blank=True)
    wb_absolut     = models.FloatField(null=True, blank=True)
    ee_absolut     = models.FloatField(null=True, blank=True)
    ee_spez        = models.FloatField(null=True, blank=True)

    created_at     = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Bauteil #{self.id} – erstellt am {self.created_at:%Y-%m-%d}"

class Beleuchtung(models.Model):
    BEREICH_CHOICES = [
        ('buero',     'Büro'),
        ('wohnen',    'Wohnen'),
        ('sanitaer',  'Sanitär'),
        ('verkehr',   'Verkehr'),
    ]

    bereich = models.CharField(
        max_length=10,
        choices=BEREICH_CHOICES,
        help_text="Nutzungsbereich"
    )
    beleuchtungsart = models.CharField(max_length=100)
    regelungsart    = models.CharField(max_length=100)
    e_soll          = models.FloatField(help_text="Soll-Beleuchtungsstärke in W/m²")
    laufzeit_hd     = models.FloatField(help_text="Betriebsstunden pro Tag")
    laufzeit_da     = models.FloatField(help_text="Betriebstage pro Jahr")

    def __str__(self):
        return f"{self.get_bereich_display()} – {self.beleuchtungsart}"
    
class Waermequelle(models.Model):
    name        = models.CharField(max_length=50, help_text="z. B. ‚Quelle 1'")
    anzahl      = models.IntegerField()
    leistung_kw = models.FloatField(help_text="Nennleistung in kW")
    betrieb_hd  = models.FloatField(help_text="Betriebsstunden pro Tag")
    betrieb_da  = models.FloatField(help_text="Betriebstage pro Jahr")

    def __str__(self):
        return self.name

class SonneneintragsParameter(models.Model):
    ORIENTIERUNG_CHOICES = [
        ('Nord',  'Nord'),
        ('Ost',   'Ost'),
        ('Sued',  'Süd'),
        ('West',  'West'),
    ]
    VERGLASUNG_CHOICES = [
        ('zweifach', 'Zweifachverglasung'),
        ('dreifach', 'Dreifachverglasung'),
    ]

    gebaeude           = models.ForeignKey(Gebaeude, on_delete=models.CASCADE)
    kritischer_raum    = models.BooleanField(
        default=False,
        help_text="Ist ein kritischer Raum definiert?"
    )
    fassadenorientierung = models.CharField(
        max_length=5,
        choices=ORIENTIERUNG_CHOICES
    )
    sonnenschutzart    = models.ForeignKey(
        SonnenschutzFaktor,
        on_delete=models.PROTECT,
        help_text="Aus Tabelle Sonnenschutz-Faktoren"
    )
    verglasungsart     = models.CharField(
        max_length=10,
        choices=VERGLASUNG_CHOICES
    )
    passive_kuehlung   = models.BooleanField(
        default=False,
        help_text="Passive Kühlung vorhanden?"
    )
    fensterneigung     = models.FloatField(
        help_text="Neigungswinkel der Fenster (°)"
    )

    def __str__(self):
        return f"{self.gebaeude} – {self.fassadenorientierung}"
    

class GwpEingabe(models.Model):
    VARIANTE_CHOICES = [
        ('300', 'Bauteile 300'),
        ('400', 'Bauteile 400'),
    ]

    gebaeude    = models.ForeignKey(Gebaeude, on_delete=models.CASCADE)
    variante    = models.CharField(max_length=3, choices=VARIANTE_CHOICES)
    menge       = models.FloatField(help_text="Menge in m² oder m³")
    spez_co2    = models.FloatField(help_text="spezifische CO₂-Emissionen")

    def __str__(self):
        return f"{self.gebaeude} / Var. {self.variante}"