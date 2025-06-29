# mylist/berechnungen.py

import math

def berechne_gebaeudedaten(laenge, breite, geschosshoehe, anz_geschosse):
    """
    Berechnet aus den Basisparametern eines Gebäudes:
      - Höhe (m)
      - Volumen (m³)
      - Bruttogrundfläche (BGF) (m²)
      - Nutzfläche (NF) (m²) als ein Anteil der BGF

    Argumente:
    - laenge: Länge des Gebäudes in m (z. B. Nord-Süd-Ausdehnung)
    - breite: Breite des Gebäudes in m (z. B. Ost-West-Ausdehnung)
    - geschosshoehe: Höhe eines Geschosses in m
    - anz_geschosse: Anzahl der Geschosse (Ganzzahl)

    Rückgabe (Dictionary):
    {
      "hoehe":   Gebäudehöhe in m (gerundet auf 2 Nachkommastellen),
      "volumen": Gebäudevolumen in m³ (gerundet auf 2 Nachkommastellen),
      "bgf":     Bruttogrundfläche in m² (gerundet auf 2 Nachkommastellen),
      "nf":      Nutzfläche in m² (gerundet auf 2 Nachkommastellen)
    }
    """
    # 1) Gebäudehöhe
    hoehe = anz_geschosse * geschosshoehe

    # 2) Volumen
    volumen = laenge * breite * hoehe

    # 3) Bruttogrundfläche (BGF)
    bgf = laenge * breite * anz_geschosse

    # 4) Nutzfläche (NF) – hier als 80 % der BGF als Beispiel-Faktor
    nf = bgf * 0.8

    return {
        "hoehe":   round(hoehe, 2),
        "volumen": round(volumen, 2),
        "bgf":     round(bgf, 2),
        "nf":      round(nf, 2),
    }


def berechne_nutzenergiebedarf(nf_m2,
                                jahres_heizwaermebedarf_kwh,
                                trinkwarmwasser_kwh_pro_m2,
                                luftfoerderung_kwh_pro_m2,
                                beleuchtung_kwh_pro_m2,
                                nutzer_pro_m2):
    """
    Berechnet den absoluten und spezifischen Nutzenergiebedarf (NE) eines Gebäudes.

    Argumente:
    - nf_m2: Nutzfläche in m²
    - jahres_heizwaermebedarf_kwh: Heizwärmebedarf des Jahres in kWh (gesamt für's Gebäude)
    - trinkwarmwasser_kwh_pro_m2: spezifischer Warmwasserbedarf in kWh/m²
    - luftfoerderung_kwh_pro_m2: spezifischer Lüftungsenergiebedarf in kWh/m²
    - beleuchtung_kwh_pro_m2: spezifischer Beleuchtungsenergiebedarf in kWh/m²
    - nutzer_pro_m2: spezifischer Prozess-/Nutzerenergiebedarf in kWh/m²

    Rückgabe (Dictionary):
    {
      "ne_absolut":      Gesamt-Nutzenergiebedarf in kWh (gerundet auf 2 Nachkommastellen),
      "ne_spezifisch":   spezifischer Nutzenergiebedarf in kWh/m² (gerundet auf 2 Nachkommastellen),
    }
    """
    # 1) Heizwärmebedarf (kWh-Wert liegt bereits absolut vor)
    heizwaerme_kwh = jahres_heizwaermebedarf_kwh

    # 2) Verbrauch pro m² multipliziert mit NF
    tw_kwh   = trinkwarmwasser_kwh_pro_m2 * nf_m2
    lwt_kwh  = luftfoerderung_kwh_pro_m2 * nf_m2
    bel_kwh  = beleuchtung_kwh_pro_m2 * nf_m2
    nutz_kwh = nutzer_pro_m2 * nf_m2

    # 3) Summe aller Anteile
    ne_abs = heizwaerme_kwh + tw_kwh + lwt_kwh + bel_kwh + nutz_kwh

    # 4) Spezifische Nutzenergie (kWh/m²)
    ne_spez = ne_abs / nf_m2 if nf_m2 > 0 else 0

    return {
        "ne_absolut":      round(ne_abs, 2),
        "ne_spezifisch":   round(ne_spez, 2),
    }


def berechne_strombedarf(nf_m2,
                         trinkwarmwasser_kwh_pro_m2,
                         luftfoerderung_kwh_pro_m2,
                         beleuchtung_kwh_pro_m2,
                         nutzer_pro_m2):
    """
    Berechnet den elektrischen Endenergiebedarf (Strombedarf) eines Gebäudes.

    Argumente:
    - nf_m2: Nutzfläche in m²
    - trinkwarmwasser_kwh_pro_m2: spezifischer Warmwasserbedarf in kWh/m² (falls elektrisch betrieben)
    - luftfoerderung_kwh_pro_m2: spezifischer Lüftungsenergiebedarf in kWh/m² (elektrische Ventilatoren, etc.)
    - beleuchtung_kwh_pro_m2: spezifischer Beleuchtungsenergiebedarf in kWh/m²
    - nutzer_pro_m2: spezifischer Prozess-/Nutzerenergiebedarf in kWh/m²

    Rückgabe (Dictionary):
    {
      "sb_absolut":     Gesamt-Strombedarf in kWh (gerundet auf 2 Nachkommastellen),
      "sb_spezifisch":  spezifischer Strombedarf in kWh/m² (gerundet auf 2 Nachkommastellen),
    }
    """
    # 1) Einzelne Bausteine (kWh/m² × NF)
    sb_tw_abs    = trinkwarmwasser_kwh_pro_m2 * nf_m2
    sb_luft_abs  = luftfoerderung_kwh_pro_m2 * nf_m2
    sb_bel_abs   = beleuchtung_kwh_pro_m2 * nf_m2
    sb_nutz_abs  = nutzer_pro_m2 * nf_m2

    # 2) Summe der elektrischen Endenergie
    sb_sum_abs   = sb_tw_abs + sb_luft_abs + sb_bel_abs + sb_nutz_abs

    # 3) Spezifischer Strombedarf in kWh/m²
    sb_sum_spec  = sb_sum_abs / nf_m2 if nf_m2 > 0 else 0

    return {
        "sb_absolut":    round(sb_sum_abs, 2),
        "sb_spezifisch": round(sb_sum_spec, 2),
    }


def berechne_waermebedarf(jahres_heizwaermebedarf_kwh,
                          verteilungsverlust_kwh=0,
                          speicherverlust_kwh=0,
                          warmwasserbedarf_kwh=0):
    """
    Berechnet den thermischen Endenergiebedarf (Wärmebedarf) eines Gebäudes.

    Argumente:
    - jahres_heizwaermebedarf_kwh: Heizwärmebedarf des Jahres in kWh (gesamt fürs Gebäude)
    - verteilungsverlust_kwh: jährliche Verteilverluste in kWh (Wärmeverteilung)
    - speicherverlust_kwh: jährliche Speicherverluste in kWh (z. B. Wärmespeicher)
    - warmwasserbedarf_kwh: jährlicher thermischer Warmwasserbedarf in kWh

    Rückgabe (Dictionary):
    {
      "wb_absolut":  Gesamt-Wärmebedarf in kWh (gerundet auf 2 Nachkommastellen),
    }
    """
    # 1) Summe aller thermischen Endenergieanteile
    wb_sum_abs = (
        jahres_heizwaermebedarf_kwh +
        verteilungsverlust_kwh +
        speicherverlust_kwh +
        warmwasserbedarf_kwh
    )

    return {
        "wb_absolut": round(wb_sum_abs, 2)
    }


def berechne_endenergiebedarf(nf_m2,
                              ergebnis_strom: dict,
                              ergebnis_waerme: dict):
    """
    Berechnet den Gesamt-Endenergiebedarf (Strom + Wärme) eines Gebäudes.

    Argumente:
    - nf_m2: Nutzfläche in m²
    - ergebnis_strom: Dictionary aus `berechne_strombedarf(...)` mit Schlüsseln "sb_absolut", "sb_spezifisch"
    - ergebnis_waerme: Dictionary aus `berechne_waermebedarf(...)` mit dem Schlüssel "wb_absolut"

    Rückgabe (Dictionary):
    {
      "ee_absolut":     Gesamt-Endenergiebedarf in kWh (gerundet auf 2 Nachkommastellen),
      "ee_spezifisch":  spezifischer Endenergiebedarf in kWh/m² (gerundet auf 2 Nachkommastellen),
    }
    """
    # 1) Absolute Werte aus den Teilergebnissen entnehmen
    sb_abs = ergebnis_strom.get("sb_absolut", 0)
    wb_abs = ergebnis_waerme.get("wb_absolut", 0)

    # 2) Summe aller Endenergie (kWh)
    ee_sum_abs = sb_abs + wb_abs

    # 3) Spezifischer Endenergiebedarf (kWh/m²)
    ee_sum_spec = ee_sum_abs / nf_m2 if nf_m2 > 0 else 0

    return {
        "ee_absolut":    round(ee_sum_abs, 2),
        "ee_spezifisch": round(ee_sum_spec, 2),
    }