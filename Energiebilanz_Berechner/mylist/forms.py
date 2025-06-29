# mylist/forms.py

from django import forms
from .models import (
    Gebaeude,
    Bauteil,
    Beleuchtung,
    Waermequelle,
    GwpEingabe,
    SonneneintragsParameter,
)

class GebaeudeAllgForm(forms.ModelForm):
    """
    Formular für den ersten Wizard-Schritt: Allgemeine Gebäudedaten.
    """
    class Meta:
        model = Gebaeude
        fields = [
            'name',
            'laenge_ns',
            'breite_ow',
            'geschosshoehe',
            'geschosse',
        ]
        widgets = {
            'laenge_ns':      forms.NumberInput(attrs={'step': '0.01'}),
            'breite_ow':      forms.NumberInput(attrs={'step': '0.01'}),
            'geschosshoehe':  forms.NumberInput(attrs={'step': '0.01'}),
            'geschosse':      forms.NumberInput(),
        }


class GebaeudeEnergieKennzahlenForm(forms.ModelForm):
    """
    Formular für den zweiten Wizard-Schritt:
    Eingabe der spezifischen kWh/m²-Werte und Heizwärmebedarf.
    """
    class Meta:
        model = Gebaeude
        fields = [
            'jahres_heizwert',
            'tw_kwh_m2',
            'luft_kwh_m2',
            'bel_kwh_m2',
            'nutz_kwh_m2',
        ]
        widgets = {
            'jahres_heizwert': forms.NumberInput(attrs={'step': '0.1'}),
            'tw_kwh_m2':       forms.NumberInput(attrs={'step': '0.1'}),
            'luft_kwh_m2':     forms.NumberInput(attrs={'step': '0.1'}),
            'bel_kwh_m2':      forms.NumberInput(attrs={'step': '0.1'}),
            'nutz_kwh_m2':     forms.NumberInput(attrs={'step': '0.1'}),
        }


class GebaeudeVerlusteForm(forms.ModelForm):
    """
    Formular für den dritten Wizard-Schritt:
    Verteilungs- und Speicherverluste, thermischer WW-Bedarf.
    """
    class Meta:
        model = Gebaeude
        fields = [
            'verteilungsverlust_kwh',
            'speicherverlust_kwh',
            'warmwasserbedarf_kwh',
        ]
        widgets = {
            'verteilungsverlust_kwh': forms.NumberInput(attrs={'step': '0.1'}),
            'speicherverlust_kwh':    forms.NumberInput(attrs={'step': '0.1'}),
            'warmwasserbedarf_kwh':   forms.NumberInput(attrs={'step': '0.1'}),
        }


class BauteilForm(forms.ModelForm):
    """
    Allgemeines Formular für Bauteil-Eingaben (U-Werte etc.).
    """
    class Meta:
        model = Bauteil
        fields = [
            'laenge',
            'breite',
            'geschosshoehe',
            'anz_geschosse',
            # folgende Felder je nach Bedarf aktivieren
            # 'u_wand_nord', 'u_wand_sued', 'u_wand_ost', 'u_wand_west',
            # 'u_bodenplatte', 'u_dach',
        ]
        widgets = {
            'laenge':         forms.NumberInput(attrs={'step': '0.01'}),
            'breite':         forms.NumberInput(attrs={'step': '0.01'}),
            'geschosshoehe':  forms.NumberInput(attrs={'step': '0.01'}),
            'anz_geschosse':  forms.NumberInput(),
        }


class LueftungForm(forms.ModelForm):
    """
    Formular für den Wizard-Schritt Lüftung.
    """
    class Meta:
        model = Bauteil
        fields = [
            'lueftungstyp',
            'luftwechselrate',
            'wrg_wirkungsgrad',
            'raum_temp_soll',
            'laufzeit_hd',
            'laufzeit_da',
        ]
        widgets = {
            'lueftungstyp':      forms.TextInput(),
            'luftwechselrate':   forms.NumberInput(attrs={'step': '0.01'}),
            'wrg_wirkungsgrad':  forms.NumberInput(attrs={'step': '0.1'}),
            'raum_temp_soll':    forms.NumberInput(attrs={'step': '0.1'}),
            'laufzeit_hd':       forms.NumberInput(attrs={'step': '0.1'}),
            'laufzeit_da':       forms.NumberInput(),
        }


class BeleuchtungForm(forms.ModelForm):
    """
    Formular für den Wizard-Schritt Beleuchtung.
    """
    class Meta:
        model = Beleuchtung
        fields = [
            'bereich',
            'beleuchtungsart',
            'regelungsart',
            'e_soll',
            'laufzeit_hd',
            'laufzeit_da',
        ]
        widgets = {
            'bereich':         forms.Select(),
            'beleuchtungsart': forms.TextInput(),
            'regelungsart':    forms.TextInput(),
            'e_soll':          forms.NumberInput(attrs={'step': '0.1'}),
            'laufzeit_hd':     forms.NumberInput(attrs={'step': '0.1'}),
            'laufzeit_da':     forms.NumberInput(),
        }


class WaermequelleForm(forms.ModelForm):
    """
    Formular für den Wizard-Schritt Wärmequellen.
    """
    class Meta:
        model = Waermequelle
        fields = [
            'name',
            'anzahl',
            'leistung_kw',
            'betrieb_hd',
            'betrieb_da',
        ]
        widgets = {
            'name':        forms.TextInput(),
            'anzahl':      forms.NumberInput(),
            'leistung_kw': forms.NumberInput(attrs={'step': '0.01'}),
            'betrieb_hd':  forms.NumberInput(attrs={'step': '0.1'}),
            'betrieb_da':  forms.NumberInput(),
        }


class GwpEingabeForm(forms.ModelForm):
    """
    Formular für den GWP-Schritt.
    """
    class Meta:
        model = GwpEingabe
        fields = [
            'gebaeude',
            'variante',
            'menge',
            'spez_co2',
        ]
        widgets = {
            'gebaeude': forms.Select(),
            'variante': forms.Select(),
            'menge':    forms.NumberInput(attrs={'step': '0.01'}),
            'spez_co2': forms.NumberInput(attrs={'step': '0.1'}),
        }


class SonneneintragsParameterForm(forms.ModelForm):
    """
    Formular für den Sonneneintrags-Schritt.
    """
    class Meta:
        model = SonneneintragsParameter
        fields = [
            'gebaeude',
            'kritischer_raum',
            'fassadenorientierung',
            'sonnenschutzart',
            'verglasungsart',
            'passive_kuehlung',
            'fensterneigung',
        ]
        widgets = {
            'gebaeude':           forms.Select(),
            'kritischer_raum':    forms.CheckboxInput(),
            'fassadenorientierung': forms.Select(),
            'sonnenschutzart':    forms.Select(),
            'verglasungsart':     forms.Select(),
            'passive_kuehlung':   forms.CheckboxInput(),
            'fensterneigung':     forms.NumberInput(attrs={'step': '1'}),
        }