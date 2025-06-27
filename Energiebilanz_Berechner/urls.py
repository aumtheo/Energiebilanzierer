from django.contrib import admin
from django.urls import path
from mylist import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Startseite
    path('', views.startseite, name='startseite'),

    # Einfache / ausführliche Bilanzierung (legacy)
    path('einfach/ergebnis/', views.einfach_ergebnis, name='einfach_ergebnis'),
    path('ausfuehrlich/',        views.ausfuehrlich,       name='ausfuehrlich'),

    # Wizard‐Flow: allgemeine Angaben → Bauteile → Wärme → GWP → Ergebnis
    path('allg/',                views.allg_angaben,               name='allg_angaben'),

    # Bauteile‐Unterwizard
    path('bauteile/bezugsgroessen/', views.bauteile_bezugsgroessen,   name='bauteile_bezugsgroessen'),
    path('bauteile/aufbau/',         views.bauteile_aufbau,           name='bauteile_aufbau'),
    path('bauteile/luftfoerderung/', views.bauteile_luftfoerderung,   name='bauteile_luftfoerderung'),
    path('bauteile/photovoltaik/',   views.bauteile_photovoltaik,     name='bauteile_photovoltaik'),

    # Wärme‐Unterwizard:
    path('waerme/heizwaerme/',     views.waerme_heizwaerme,    name='waerme_heizwaerme'),
    path('waerme/waermequellen/',  views.waerme_waermequellen, name='waerme_waermequellen'),
    path('waerme/waermeschutz/',   views.waerme_waermeschutz,  name='waerme_waermeschutz'),
    path('waerme/lichtwasser/',    views.waerme_lichtwasser,   name='waerme_lichtwasser'),

    # GWP‐Unterwizard:
    path('gwp/herstellung/',      views.gwp_herstellung,      name='gwp_herstellung'),
    path('gwp/waermequellen/',    views.gwp_waermequellen,    name='gwp_waermequellen'),

    path('konfigurator/grundriss/', views.grundriss, name='grundriss'),
    path('konfigurator/raum/', views.raumkonfigurator, name='raumkonfigurator'),
    path('konfigurator/floorplanner/', views.floorplanner, name='konfigurator_floorplanner'),
    path('konfigurator/wandaufbau/', views.wandaufbau, name='wandaufbau'),
    
    path('uber/', views.uber_tool, name='uber_tool'),
    path('entwicklerteam/', views.entwicklerteam, name='entwicklerteam'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('hilfe/', views.hilfe, name='hilfe'),
    path('ergebnis/pdf/', views.einfach_ergebnis_pdf, name='ergebnis_pdf'),

    path('baukoerper/',    views.baukrper,     name='baukrper'),
    path('bauteil/', views.bauteil, name='bauteil'),
    path('pv/', views.pv, name='pv'),
    path('lftung/', views.lftung, name='lftung'),
    path('beleuchtung/', views.beleuchtung, name='beleuchtung'),
    path('beleuchtung_2/', views.beleuchtung_2, name='beleuchtung_2'),
    path('waermequellen/', views.waermequellen, name='waermequellen'),
    path('sdf/',           views.sdf,                name='sdf'),
    path('gwp/',           views.gwp,                name='gwp'),
    path('ergebnis/', views.ergebnis, name='ergebnis'),
    path(
        'baukoerper/komplex/',
        views.baukoerper_kp,
        name='baukoerper_kp'    
    ),
    path('baukoerper/komplex/2/', views.baukrper_kp_2, name='baukrper_kp_2'),
    path('bauteil/komplex/', views.bauteil_kp, name='bauteil_kp'),

    path("api/berechnung/", views.api_berechnung, name="api_berechnung"),

    # Wizard flow
    path('wizard/allg/', views.allg_angaben, name='wizard_allg'),
    path('wizard/energie/', views.energie_angaben, name='wizard_energie'),
    path('wizard/verluste/', views.verluste_angaben, name='wizard_verluste'),
    path('wizard/bauteile/', views.bauteile_angaben, name='wizard_bauteile'),
    path('wizard/lueftung/', views.lueftung_angaben, name='wizard_lueftung'),
    path('wizard/beleuchtung/', views.beleuchtung_angaben, name='wizard_beleuchtung'),
    path('wizard/waermequelle/', views.waermequelle_angaben, name='wizard_waermequelle'),
    path('wizard/gwp/', views.gwp_angaben, name='wizard_gwp'),
    path('wizard/sonneneintrag/', views.sonneneintrag_angaben, name='wizard_sonneneintrag'),
    path('wizard/ergebnis/', views.wizard_ergebnis, name='wizard_ergebnis'),

    # Gebäude-Detailseiten
    path('gebaeude/allg/', views.gebaeude_allg, name='gebaeude_allg'),
    path('kennzahlen/<int:gebaeude_id>/', views.gebaeude_kennzahlen, name='gebaeude_kennzahlen'),
    path('verluste/<int:gebaeude_id>/', views.gebaeude_verluste, name='gebaeude_verluste'),
    path('lueftung/<int:gebaeude_id>/', views.lueftung, name='lueftung'),
    path('beleuchtung/<int:gebaeude_id>/', views.beleuchtung, name='beleuchtung'),
    path('waermequelle/<int:gebaeude_id>/', views.waermequelle, name='waermequelle'),
    path('gwp/<int:gebaeude_id>/', views.gwp_eingabe, name='gwp'),
    path('sonneneintrag/<int:gebaeude_id>/', views.sonneneintrag, name='sonneneintrag'),
]