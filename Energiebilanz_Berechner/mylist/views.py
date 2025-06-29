# mylist/views.py

from io import BytesIO
import csv, os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import (
    Gebaeude,
    Bauteil,
    Beleuchtung,
    Waermequelle,
    GwpEingabe,
    SonneneintragsParameter,
)
from .forms import (
    GebaeudeAllgForm,
    GebaeudeEnergieKennzahlenForm,
    GebaeudeVerlusteForm,
    BauteilForm,
    LueftungForm,
    BeleuchtungForm,
    WaermequelleForm,
    GwpEingabeForm,
    SonneneintragsParameterForm,
)
from .berechnungen import (
    berechne_gebaeudedaten,
    berechne_nutzenergiebedarf,
    berechne_strombedarf,
    berechne_waermebedarf,
    berechne_endenergiebedarf,
)


# ————— Start & Wizard Steps —————

def startseite(request):
    return render(request, 'startseite.html')


def gebaeude_allg(request):
    if request.method == 'POST':
        form = GebaeudeAllgForm(request.POST)
        if form.is_valid():
            geb = form.save()
            request.session['gebaeude_id'] = geb.pk
            return redirect('gebaeude_kennzahlen')
    else:
        form = GebaeudeAllgForm()
    return render(request, 'mylist/gebaeude_allg.html', {'form': form})


def gebaeude_kennzahlen(request, gebaeude_id):
    geb = get_object_or_404(Gebaeude, pk=gebaeude_id)
    if request.method == 'POST':
        form = GebaeudeEnergieKennzahlenForm(request.POST, instance=geb)
        if form.is_valid():
            form.save()
            return redirect('gebaeude_verluste', gebaeude_id=geb.pk)
    else:
        form = GebaeudeEnergieKennzahlenForm(instance=geb)
    return render(request, 'mylist/gebaeude_kennzahlen.html', {'form': form})


def gebaeude_verluste(request, gebaeude_id):
    geb = get_object_or_404(Gebaeude, pk=gebaeude_id)
    if request.method == 'POST':
        form = GebaeudeVerlusteForm(request.POST, instance=geb)
        if form.is_valid():
            form.save()
            return redirect('lueftung', gebaeude_id=geb.pk)
    else:
        form = GebaeudeVerlusteForm(instance=geb)
    return render(request, 'mylist/gebaeude_verluste.html', {'form': form})


def lueftung(request, gebaeude_id):
    geb = get_object_or_404(Gebaeude, pk=gebaeude_id)
    if request.method == 'POST':
        form = LueftungForm(request.POST)
        if form.is_valid():
            lueftung = form.save(commit=False)
            # You might want to associate the lueftung with the gebaeude here
            lueftung.save()
            return redirect('beleuchtung', gebaeude_id=geb.pk)
    else:
        form = LueftungForm()
    return render(request, 'mylist/lueftung.html', {'form': form, 'gebaeude': geb})


def beleuchtung(request, gebaeude_id):
    geb = get_object_or_404(Gebaeude, pk=gebaeude_id)
    if request.method == 'POST':
        form = BeleuchtungForm(request.POST)
        if form.is_valid():
            beleuchtung = form.save(commit=False)
            # You might want to associate the beleuchtung with the gebaeude here
            beleuchtung.save()
            return redirect('waermequelle', gebaeude_id=geb.pk)
    else:
        form = BeleuchtungForm()
    return render(request, 'mylist/beleuchtung.html', {'form': form, 'gebaeude': geb})


def waermequelle(request, gebaeude_id):
    geb = get_object_or_404(Gebaeude, pk=gebaeude_id)
    if request.method == 'POST':
        form = WaermequelleForm(request.POST)
        if form.is_valid():
            waermequelle = form.save(commit=False)
            # You might want to associate the waermequelle with the gebaeude here
            waermequelle.save()
            return redirect('gwp', gebaeude_id=geb.pk)
    else:
        form = WaermequelleForm()
    return render(request, 'mylist/waermequelle.html', {'form': form, 'gebaeude': geb})


def gwp_eingabe(request, gebaeude_id):
    geb = get_object_or_404(Gebaeude, pk=gebaeude_id)
    if request.method == 'POST':
        form = GwpEingabeForm(request.POST)
        if form.is_valid():
            gwp = form.save(commit=False)
            gwp.gebaeude = geb
            gwp.save()
            return redirect('sonneneintrag', gebaeude_id=geb.pk)
    else:
        form = GwpEingabeForm(initial={'gebaeude': geb})
    return render(request, 'mylist/gwp_eingabe.html', {'form': form, 'gebaeude': geb})


def sonneneintrag(request, gebaeude_id):
    geb = get_object_or_404(Gebaeude, pk=gebaeude_id)
    if request.method == 'POST':
        form = SonneneintragsParameterForm(request.POST)
        if form.is_valid():
            sonneneintrag = form.save(commit=False)
            sonneneintrag.gebaeude = geb
            sonneneintrag.save()
            return redirect('ergebnis')
    else:
        form = SonneneintragsParameterForm(initial={'gebaeude': geb})
    return render(request, 'mylist/sonneneintrag.html', {'form': form, 'gebaeude': geb})


# ————— PDF-Export —————

def einfach_ergebnis_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(w/2, h-80, "Ergebnis der Gebäudeberechnung")

    p.setFont("Helvetica", 12)
    y = h - 120
    for label, val in [
        ("Länge (m)", request.GET.get('laenge', '-')),
        ("Breite (m)", request.GET.get('breite', '-')),
        ("Geschosshöhe (m)", request.GET.get('geschosshoehe', '-')),
        ("Anzahl Geschosse", request.GET.get('geschosse', '-')),
    ]:
        p.drawString(80, y, f"{label}: {val}")
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)
    resp = HttpResponse(buffer, content_type='application/pdf')
    resp['Content-Disposition'] = 'attachment; filename="ergebnis.pdf"'
    return resp


# ————— JSON-API —————

def api_berechnung(request):
    try:
        laenge = float(request.GET.get("laenge", 0))
        breite = float(request.GET.get("breite", 0))
        geschosshoehe = float(request.GET.get("geschosshoehe", 0))
        anz_geschosse = int(request.GET.get("anz_geschosse", 0))
    except (ValueError, TypeError):
        laenge = breite = geschosshoehe = 0
        anz_geschosse = 0

    geb = berechne_gebaeudedaten(laenge, breite, geschosshoehe, anz_geschosse)
    
    try:
        ne = berechne_nutzenergiebedarf(
            geb["nf"],
            float(request.GET.get("jahres_heizbedarf", 0)),
            float(request.GET.get("tw_pro_m2", 0)),
            float(request.GET.get("lwt_pro_m2", 0)),
            float(request.GET.get("bel_pro_m2", 0)),
            float(request.GET.get("nutzer_pro_m2", 0)),
        )
        sb = berechne_strombedarf(
            geb["nf"],
            float(request.GET.get("tw_pro_m2", 0)),
            float(request.GET.get("lwt_pro_m2", 0)),
            float(request.GET.get("bel_pro_m2", 0)),
            float(request.GET.get("nutzer_pro_m2", 0)),
        )
        wb = berechne_waermebedarf(
            float(request.GET.get("jahres_heizbedarf", 0)),
            float(request.GET.get("verlust_verteilung", 0)),
            float(request.GET.get("verlust_speicher", 0)),
            float(request.GET.get("ww_warmwasser", 0)),
        )
        ee = berechne_endenergiebedarf(geb["nf"], sb, wb)
    except (ValueError, TypeError):
        ne = {"ne_absolut": 0, "ne_spezifisch": 0}
        sb = {"sb_absolut": 0, "sb_spezifisch": 0}
        wb = {"wb_absolut": 0}
        ee = {"ee_absolut": 0, "ee_spezifisch": 0}

    return JsonResponse({
        "gebaeudedaten": geb,
        "nutzenergie":   ne,
        "strombedarf":   sb,
        "waermebedarf":  wb,
        "endenergie":    ee,
    })


# ————— Neue Wizard-Flow Views —————

def allg_angaben(request):
    """
    Erster Schritt des Wizards: Allgemeine Gebäudedaten.
    """
    if request.method == 'POST':
        form = GebaeudeAllgForm(request.POST)
        if form.is_valid():
            gebaeude = form.save()
            request.session['geb_pk'] = gebaeude.pk
            return redirect('wizard_energie')
    else:
        form = GebaeudeAllgForm()
    
    return render(request, 'allg_angaben.html', {
        'form': form,
        'orte': ['Bremerhaven', 'Rostock', 'Hamburg', 'Potsdam', 'Essen', 
                'Bad Marienberg', 'Kassel', 'Braunlage', 'Chemnitz', 'Hof', 
                'Fichtelberg', 'Mannheim', 'Passau', 'Stötten', 'Garmisch-Partenkirchen']
    })


def energie_angaben(request):
    """
    Zweiter Schritt des Wizards: Energiekennzahlen.
    """
    gebaeude_pk = request.session.get('geb_pk')
    if not gebaeude_pk:
        return redirect('wizard_allg')
    
    gebaeude = get_object_or_404(Gebaeude, pk=gebaeude_pk)
    
    if request.method == 'POST':
        form = GebaeudeEnergieKennzahlenForm(request.POST, instance=gebaeude)
        if form.is_valid():
            form.save()
            return redirect('wizard_verluste')
    else:
        form = GebaeudeEnergieKennzahlenForm(instance=gebaeude)
    
    return render(request, 'energie_angaben.html', {'form': form, 'gebaeude': gebaeude})


def verluste_angaben(request):
    """
    Dritter Schritt des Wizards: Verluste und Warmwasserbedarf.
    """
    gebaeude_pk = request.session.get('geb_pk')
    if not gebaeude_pk:
        return redirect('wizard_allg')
    
    gebaeude = get_object_or_404(Gebaeude, pk=gebaeude_pk)
    
    if request.method == 'POST':
        form = GebaeudeVerlusteForm(request.POST, instance=gebaeude)
        if form.is_valid():
            form.save()
            return redirect('wizard_bauteile')
    else:
        form = GebaeudeVerlusteForm(instance=gebaeude)
    
    return render(request, 'verluste_angaben.html', {'form': form, 'gebaeude': gebaeude})


def bauteile_angaben(request):
    """
    Vierter Schritt des Wizards: Bauteile.
    """
    gebaeude_pk = request.session.get('geb_pk')
    if not gebaeude_pk:
        return redirect('wizard_allg')
    
    gebaeude = get_object_or_404(Gebaeude, pk=gebaeude_pk)
    
    if request.method == 'POST':
        form = BauteilForm(request.POST)
        if form.is_valid():
            bauteil = form.save(commit=False)
            
            # Gebäude-Basisdaten berechnen
            gd = berechne_gebaeudedaten(
                laenge=bauteil.laenge,
                breite=bauteil.breite,
                geschosshoehe=bauteil.geschosshoehe,
                anz_geschosse=bauteil.anz_geschosse,
            )
            
            # Berechnete Werte setzen
            bauteil.hoehe = gd['hoehe']
            bauteil.volumen = gd['volumen']
            bauteil.bgf = gd['bgf']
            bauteil.nf = gd['nf']
            
            # Bauteil mit Gebäude verknüpfen
            # Annahme: Bauteil hat ein ForeignKey-Feld 'gebaeude'
            # bauteil.gebaeude = gebaeude
            
            bauteil.save()
            request.session['teil_pk'] = bauteil.pk
            return redirect('wizard_lueftung')
    else:
        form = BauteilForm()
    
    return render(request, 'bauteile_angaben.html', {'form': form, 'gebaeude': gebaeude})


def lueftung_angaben(request):
    """
    Fünfter Schritt des Wizards: Lüftung.
    """
    bauteil_pk = request.session.get('teil_pk')
    if not bauteil_pk:
        return redirect('wizard_bauteile')
    
    bauteil = get_object_or_404(Bauteil, pk=bauteil_pk)
    
    if request.method == 'POST':
        form = LueftungForm(request.POST, instance=bauteil)
        if form.is_valid():
            form.save()
            return redirect('wizard_beleuchtung')
    else:
        form = LueftungForm(instance=bauteil)
    
    return render(request, 'lueftung_angaben.html', {'form': form, 'bauteil': bauteil})


def beleuchtung_angaben(request):
    """
    Sechster Schritt des Wizards: Beleuchtung.
    """
    gebaeude_pk = request.session.get('geb_pk')
    if not gebaeude_pk:
        return redirect('wizard_allg')
    
    gebaeude = get_object_or_404(Gebaeude, pk=gebaeude_pk)
    
    if request.method == 'POST':
        form = BeleuchtungForm(request.POST)
        if form.is_valid():
            beleuchtung = form.save(commit=False)
            # Annahme: Beleuchtung hat ein ForeignKey-Feld 'gebaeude'
            # beleuchtung.gebaeude = gebaeude
            beleuchtung.save()
            return redirect('wizard_waermequelle')
    else:
        form = BeleuchtungForm()
    
    return render(request, 'beleuchtung_angaben.html', {'form': form, 'gebaeude': gebaeude})


def waermequelle_angaben(request):
    """
    Siebter Schritt des Wizards: Wärmequelle.
    """
    gebaeude_pk = request.session.get('geb_pk')
    if not gebaeude_pk:
        return redirect('wizard_allg')
    
    gebaeude = get_object_or_404(Gebaeude, pk=gebaeude_pk)
    
    if request.method == 'POST':
        form = WaermequelleForm(request.POST)
        if form.is_valid():
            waermequelle = form.save(commit=False)
            # Annahme: Waermequelle hat ein ForeignKey-Feld 'gebaeude'
            # waermequelle.gebaeude = gebaeude
            waermequelle.save()
            return redirect('wizard_gwp')
    else:
        form = WaermequelleForm()
    
    return render(request, 'waermequelle_angaben.html', {'form': form, 'gebaeude': gebaeude})


def gwp_angaben(request):
    """
    Achter Schritt des Wizards: GWP (Global Warming Potential).
    """
    gebaeude_pk = request.session.get('geb_pk')
    if not gebaeude_pk:
        return redirect('wizard_allg')
    
    gebaeude = get_object_or_404(Gebaeude, pk=gebaeude_pk)
    
    if request.method == 'POST':
        form = GwpEingabeForm(request.POST)
        if form.is_valid():
            gwp = form.save(commit=False)
            gwp.gebaeude = gebaeude
            gwp.save()
            return redirect('wizard_sonneneintrag')
    else:
        form = GwpEingabeForm(initial={'gebaeude': gebaeude})
    
    return render(request, 'gwp_angaben.html', {'form': form, 'gebaeude': gebaeude})


def sonneneintrag_angaben(request):
    """
    Neunter Schritt des Wizards: Sonneneintrag.
    """
    gebaeude_pk = request.session.get('geb_pk')
    if not gebaeude_pk:
        return redirect('wizard_allg')
    
    gebaeude = get_object_or_404(Gebaeude, pk=gebaeude_pk)
    
    if request.method == 'POST':
        form = SonneneintragsParameterForm(request.POST)
        if form.is_valid():
            sonneneintrag = form.save(commit=False)
            sonneneintrag.gebaeude = gebaeude
            sonneneintrag.save()
            return redirect('wizard_ergebnis')
    else:
        form = SonneneintragsParameterForm(initial={'gebaeude': gebaeude})
    
    return render(request, 'sonneneintrag_angaben.html', {'form': form, 'gebaeude': gebaeude})


def wizard_ergebnis(request):
    """
    Letzter Schritt des Wizards: Ergebnisanzeige.
    """
    gebaeude_pk = request.session.get('geb_pk')
    bauteil_pk = request.session.get('teil_pk')
    
    if not gebaeude_pk or not bauteil_pk:
        return redirect('wizard_allg')
    
    gebaeude = get_object_or_404(Gebaeude, pk=gebaeude_pk)
    bauteil = get_object_or_404(Bauteil, pk=bauteil_pk)
    
    # Berechnungen durchführen
    ne = berechne_nutzenergiebedarf(
        nf_m2=bauteil.nf,
        jahres_heizwaermebedarf_kwh=gebaeude.jahres_heizwert,
        trinkwarmwasser_kwh_pro_m2=gebaeude.tw_kwh_m2,
        luftfoerderung_kwh_pro_m2=gebaeude.luft_kwh_m2,
        beleuchtung_kwh_pro_m2=gebaeude.bel_kwh_m2,
        nutzer_pro_m2=gebaeude.nutz_kwh_m2,
    )
    
    sb = berechne_strombedarf(
        nf_m2=bauteil.nf,
        trinkwarmwasser_kwh_pro_m2=gebaeude.tw_kwh_m2,
        luftfoerderung_kwh_pro_m2=gebaeude.luft_kwh_m2,
        beleuchtung_kwh_pro_m2=gebaeude.bel_kwh_m2,
        nutzer_pro_m2=gebaeude.nutz_kwh_m2,
    )
    
    wb = berechne_waermebedarf(
        jahres_heizwaermebedarf_kwh=gebaeude.jahres_heizwert,
        verteilungsverlust_kwh=gebaeude.verteilungsverlust_kwh,
        speicherverlust_kwh=gebaeude.speicherverlust_kwh,
        warmwasserbedarf_kwh=gebaeude.warmwasserbedarf_kwh,
    )
    
    ee = berechne_endenergiebedarf(bauteil.nf, sb, wb)
    
    # Ergebnisse im Bauteil speichern
    bauteil.ne_absolut = ne['ne_absolut']
    bauteil.ne_spez = ne['ne_spezifisch']
    bauteil.sb_absolut = sb['sb_absolut']
    bauteil.sb_spez = sb['sb_spezifisch']
    bauteil.wb_absolut = wb['wb_absolut']
    bauteil.ee_absolut = ee['ee_absolut']
    bauteil.ee_spez = ee['ee_spezifisch']
    bauteil.save()
    
    # Alle relevanten Daten für die Ergebnisseite sammeln
    context = {
        'gebaeude': gebaeude,
        'bauteil': bauteil,
        'nutzenergie': ne,
        'strombedarf': sb,
        'waermebedarf': wb,
        'endenergie': ee,
        # Weitere Daten wie GWP, Beleuchtung, etc. könnten hier hinzugefügt werden
    }
    
    return render(request, 'wizard_ergebnis.html', context)


def einfach_ergebnis(request):
    """
    Einfache Ergebnisanzeige für die Schnellberechnung.
    """
    # Beispiel-Implementierung, die Daten aus GET-Parametern liest
    laenge = float(request.GET.get('laenge', 0))
    breite = float(request.GET.get('breite', 0))
    geschosshoehe = float(request.GET.get('geschosshoehe', 0))
    geschosse = int(request.GET.get('geschosse', 0))
    
    # Gebäudedaten berechnen
    daten = berechne_gebaeudedaten(laenge, breite, geschosshoehe, geschosse)
    
    # Nutzenergiebedarf berechnen (Beispielwerte)
    jahres_heizwert = float(request.GET.get('jahres_heizwert', 0))
    tw_kwh_m2 = float(request.GET.get('tw_kwh_m2', 0))
    luft_kwh_m2 = float(request.GET.get('luft_kwh_m2', 0))
    bel_kwh_m2 = float(request.GET.get('bel_kwh_m2', 0))
    nutz_kwh_m2 = float(request.GET.get('nutz_kwh_m2', 0))
    
    ne = berechne_nutzenergiebedarf(
        daten['nf'], jahres_heizwert, tw_kwh_m2, luft_kwh_m2, bel_kwh_m2, nutz_kwh_m2
    )
    
    context = {
        'daten': daten,
        'ne_absolut': ne['ne_absolut'],
        'ne_spezifisch': ne['ne_spezifisch'],
    }
    
    return render(request, 'einfach_ergebnis.html', context)


# ————— Weitere Views für die Navigation —————

def ausfuehrlich(request):
    """View für die ausführliche Bilanzierung."""
    return render(request, 'ausfuehrlich.html')


def grundriss(request):
    """View für die Grundrisserfassung."""
    return render(request, 'grundriss.html')


def raumkonfigurator(request):
    """View für den Raumkonfigurator."""
    return render(request, 'raumkonfigurator.html')


def floorplanner(request):
    """View für den Floorplanner."""
    return render(request, 'floorplanner.html')


def wandaufbau(request):
    """View für die Wandaufbau-Konfiguration."""
    return render(request, 'wandaufbau.html')


def uber_tool(request):
    """View für die 'Über das Tool'-Seite."""
    return render(request, 'uber_tool.html')


def entwicklerteam(request):
    """View für die Entwicklerteam-Seite."""
    return render(request, 'entwicklerteam.html')


def kontakt(request):
    """View für die Kontakt-Seite."""
    return render(request, 'kontakt.html')


def hilfe(request):
    """View für die Hilfe-Seite."""
    return render(request, 'hilfe.html')


def baukrper(request):
    """View für die Baukörper-Seite."""
    return render(request, 'baukrper.html')


def bauteil(request):
    """View für die Bauteil-Seite."""
    return render(request, 'bauteil.html')


def pv(request):
    """View für die PV-Seite."""
    return render(request, 'pv.html')


def lftung(request):
    """View für die Lüftung-Seite."""
    return render(request, 'lftung.html')


def beleuchtung_2(request):
    """View für die Beleuchtung-Seite (Teil 2)."""
    return render(request, 'beleuchtung_2.html')


def waermequellen(request):
    """View für die Wärmequellen-Seite."""
    return render(request, 'wrmequellen.html')


def sdf(request):
    """View für die SDF-Seite."""
    return render(request, 'sdf.html')


def gwp(request):
    """View für die GWP-Seite."""
    return render(request, 'gwp.html')


def ergebnis(request):
    """View für die Ergebnis-Seite."""
    return render(request, 'ergebnis.html')


def baukoerper_kp(request):
    """View für die komplexe Baukörper-Seite."""
    return render(request, 'baukrper_kp.html')


def baukrper_kp_2(request):
    """View für die komplexe Baukörper-Seite (Teil 2)."""
    return render(request, 'baukrper_kp_2.html')


def bauteil_kp(request):
    """View für die komplexe Bauteil-Seite."""
    return render(request, 'bauteil_kp.html')


# Additional views for the wizard flow
def bauteile_bezugsgroessen(request):
    return render(request, 'bauteile_bezugsgroessen.html')

def bauteile_aufbau(request):
    return render(request, 'bauteile_aufbau.html')

def bauteile_luftfoerderung(request):
    return render(request, 'bauteile_luftfoerderung.html')

def bauteile_photovoltaik(request):
    return render(request, 'bauteile_photovoltaik.html')

def waerme_heizwaerme(request):
    return render(request, 'waerme_heizwaerme.html')

def waerme_waermequellen(request):
    return render(request, 'waerme_waermequellen.html')

def waerme_waermeschutz(request):
    return render(request, 'waerme_waermeschutz.html')

def waerme_lichtwasser(request):
    return render(request, 'waerme_lichtwasser.html')

def gwp_herstellung(request):
    return render(request, 'gwp_herstellung.html')

def gwp_waermequellen(request):
    return render(request, 'gwp_waermequellen.html')