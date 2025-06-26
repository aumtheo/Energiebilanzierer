from django.contrib import admin
from .models import (
    BuildingProject,
    Gebaeude,
    KlimaregionTemperatur,
    DruckverlustBauteil,
    SonnenschutzFaktor,
    Temperaturkorrekturfaktor,
    SolarStrahlungMonat,
    SonneneintragsKennwert,
    Bauteil,
    Beleuchtung,
    Waermequelle,
    SonneneintragsParameter,
    GwpEingabe,
)

@admin.register(BuildingProject)
class BuildingProjectAdmin(admin.ModelAdmin):
    list_display   = ('pk', 'standort', 'created')
    list_filter    = ('created',)
    search_fields  = ('standort',)
    ordering       = ('-created',)

@admin.register(Gebaeude)
class GebaeudeAdmin(admin.ModelAdmin):
    list_display   = ('pk', 'name', 'laenge_ns', 'breite_ow', 'geschosse')
    search_fields  = ('name',)
    list_filter    = ('geschosse',)

@admin.register(KlimaregionTemperatur)
class KlimaregionTemperaturAdmin(admin.ModelAdmin):
    list_display   = ('region', 'referenzort', 'jahreswert')
    list_filter    = ('region',)
    search_fields  = ('referenzort',)

@admin.register(DruckverlustBauteil)
class DruckverlustBauteilAdmin(admin.ModelAdmin):
    list_display   = ('bauteil', 'druckverlust_pa')
    search_fields  = ('bauteil',)

@admin.register(SonnenschutzFaktor)
class SonnenschutzFaktorAdmin(admin.ModelAdmin):
    list_display   = ('zeile', 'sonnenschutzvorrichtung')
    search_fields  = ('zeile', 'sonnenschutzvorrichtung')

@admin.register(Temperaturkorrekturfaktor)
class TemperaturkorrekturfaktorAdmin(admin.ModelAdmin):
    list_display   = ('bauteil', 'fx')
    search_fields  = ('bauteil',)

@admin.register(SolarStrahlungMonat)
class SolarStrahlungMonatAdmin(admin.ModelAdmin):
    list_display   = ('orientierung', 'neigung', 'jahreswert')
    list_filter    = ('orientierung', 'neigung')

@admin.register(SonneneintragsKennwert)
class SonneneintragsKennwertAdmin(admin.ModelAdmin):
    list_display   = ('typ', 'bauart', 'beschreibung')
    list_filter    = ('typ', 'bauart')
    search_fields  = ('beschreibung',)

@admin.register(Bauteil)
class BauteilAdmin(admin.ModelAdmin):
    list_display   = ('id', 'created_at', 'lueftungstyp', 'laufzeit_hd', 'laufzeit_da')
    list_filter    = ('lueftungstyp',)
    search_fields  = ('lueftungstyp',)

@admin.register(Beleuchtung)
class BeleuchtungAdmin(admin.ModelAdmin):
    list_display   = ('bereich', 'beleuchtungsart', 'regelungsart', 'e_soll')
    list_filter    = ('bereich',)
    search_fields  = ('beleuchtungsart',)

@admin.register(Waermequelle)
class WaermequelleAdmin(admin.ModelAdmin):
    list_display   = ('name', 'anzahl', 'leistung_kw')
    search_fields  = ('name',)

@admin.register(SonneneintragsParameter)
class SonneneintragsParameterAdmin(admin.ModelAdmin):
    list_display   = ('gebaeude', 'fassadenorientierung', 'verglasungsart', 'passive_kuehlung')
    list_filter    = ('fassadenorientierung', 'passive_kuehlung')

@admin.register(GwpEingabe)
class GwpEingabeAdmin(admin.ModelAdmin):
    list_display   = ('gebaeude', 'variante', 'menge', 'spez_co2')
    list_filter    = ('variante',)
