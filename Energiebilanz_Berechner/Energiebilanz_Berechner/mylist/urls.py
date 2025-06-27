from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.startseite,               name='startseite'),
    path('wizard/',                 views.allg_angaben,             name='wizard_allg'),
    path('wizard/energie/',         views.energie_angaben,          name='wizard_energie'),
    path('wizard/verluste/',        views.verluste_angaben,         name='wizard_verluste'),
    path('wizard/bauteile/',        views.bauteile_angaben,         name='wizard_bauteile'),
    path('wizard/lueftung/',        views.lueftung_angaben,         name='wizard_lueftung'),
    path('wizard/beleuchtung/',     views.beleuchtung_angaben,      name='wizard_beleuchtung'),
    path('wizard/waermequelle/',    views.waermequelle_angaben,     name='wizard_waermequelle'),
    path('wizard/gwp/',             views.gwp_angaben,              name='wizard_gwp'),
    path('wizard/sonneneintrag/',   views.sonneneintrag_angaben,    name='wizard_sonneneintrag'),
    path('wizard/ergebnis/',        views.wizard_ergebnis,          name='wizard_ergebnis'),
]