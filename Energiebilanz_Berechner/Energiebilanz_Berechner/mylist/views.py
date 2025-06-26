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
    return render(request, 'mylist/startseite.html')


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


def gebaeude_kennzahlen(request):
    gebaeude_id = request.session.get('gebaeude_id')
    geb = get_object_or_404(Gebaeude, pk=gebaeude_id)
    if request.method == 'POST':
        form = GebaeudeEnergieKennzahlenForm(request.POST, instance=geb)
        if form.is_valid():
            form.save()
            return redirect('gebaeude_verluste')
    else:
        form = GebaeudeEnergieKennzahlenForm(instance=geb)
    return render(request, 'mylist/gebaeude_kennzahlen.html', {'form': form})


def gebaeude_verluste(request):
    gebaeude_id = request.session.get('gebaeude_id')
    geb = get_object_or_404(Gebaeude, pk=gebaeude_id)
    if request.method == 'POST':
        form = GebaeudeVerlusteForm(request.POST, instance=geb)
        if form.is_valid():
            form.save()
            return redirect('bauteil_eingabe')
    else:
        form = GebaeudeVerlusteForm(instance=geb)
    return render(request, 'mylist/gebaeude_verluste.html', {'form': form})


def bauteil_eingabe(request):
    gebaeude_id = request.session.get('gebaeude_id')
    geb = get_object_or_404(Gebaeude, pk=gebaeude_id)
    if request.method == 'POST':
        form = BauteilForm(request.POST)
        if form.is_valid():
            b = form.save(commit=False)
            # Gebäude-Basisdaten berechnen
            gd = berechne_gebaeudedaten(
                laenge=b.laenge,
                breite=b.breite,
                geschosshoehe=b.geschosshoehe,
                anz_geschosse=b.anz_geschosse,
            )
            b.hoehe = gd['hoehe']
            b.volumen = gd['volumen']
            b.bgf = gd['bgf']
            b.nf = gd['nf']
            b.save()
            return redirect('lueftung_eingabe', bauteil_id=b.pk)
    else:
        form = BauteilForm()
    return render(request, 'mylist/bauteil_eingabe.html', {'form': form})


def lueftung_eingabe(request, bauteil_id):
    b = get_object_or_404(Bauteil, pk=bauteil_id)
    if request.method == 'POST':
        form = LueftungForm(request.POST, instance=b)
        if form.is_valid():
            form.save()
            return redirect('beleuchtung_eingabe', bauteil_id=b.pk)
    else:
        form = LueftungForm(instance=b)
    return render(request, 'mylist/lueftung_eingabe.html', {'form': form})


def beleuchtung_eingabe(request, bauteil_id):
    b = get_object_or_404(Bauteil, pk=bauteil_id)
    if request.method == 'POST':
        form = BeleuchtungForm(request.POST)
        if form.is_valid():
            lb = form.save(commit=False)
            lb.save()
            return redirect('waermequelle_eingabe', bauteil_id=b.pk)
    else:
        form = BeleuchtungForm()
    return render(request, 'mylist/beleuchtung_eingabe.html', {'form': form})


def waermequelle_eingabe(request, bauteil_id):
    b = get_object_or_404(Bauteil, pk=bauteil_id)
    if request.method == 'POST':
        form = WaermequelleForm(request.POST)
        if form.is_valid():
            wq = form.save(commit=False)
            wq.save()
            return redirect('gwp_eingabe', bauteil_id=b.pk)
    else:
        form = WaermequelleForm()
    return render(request, 'mylist/waermequelle_eingabe.html', {'form': form})


def gwp_eingabe(request, bauteil_id):
    b = get_object_or_404(Bauteil, pk=bauteil_id)
    if request.method == 'POST':
        form = GwpEingabeForm(request.POST)
        if form.is_valid():
            ge = form.save(commit=False)
            ge.save()
            return redirect('sonneneintrag_eingabe', bauteil_id=b.pk)
    else:
        form = GwpEingabeForm()
    return render(request, 'mylist/gwp_eingabe.html', {'form': form})


def sonneneintrag_eingabe(request, bauteil_id):
    b = get_object_or_404(Bauteil, pk=bauteil_id)
    if request.method == 'POST':
        form = SonneneintragsParameterForm(request.POST)
        if form.is_valid():
            sp = form.save(commit=False)
            sp.save()
            return redirect('ergebnis_seite', bauteil_id=b.pk)
    else:
        form = SonneneintragsParameterForm()
    return render(request, 'mylist/sonneneintrag_eingabe.html', {'form': form})


def ergebnis_seite(request, bauteil_id):
    b = get_object_or_404(Bauteil, pk=bauteil_id)

    # Beispiel: Endenergie-Berechnungen
    ne = berechne_nutzenergiebedarf(
        nf_m2=b.nf,
        jahres_heizbedarf_kwh=b.gebaeude.jahres_heizwert,
        trinkwarmwasser_kwh_pro_m2=b.gebaeude.tw_kwh_m2,
        luftfoerderung_kwh_pro_m2=b.luftwechselrate,  # oder b.luft_kwh_m2
        beleuchtung_kwh_pro_m2=b.gebaeude.bel_kwh_m2,
        nutzer_pro_m2=b.gebaeude.nutz_kwh_m2,
    )
    sb = berechne_strombedarf(
        nf_m2=b.nf,
        trinkwarmwasser_kwh_pro_m2=b.gebaeude.tw_kwh_m2,
        luftfoerderung_kwh_pro_m2=b.luftwechselrate,
        beleuchtung_kwh_pro_m2=b.gebaeude.bel_kwh_m2,
        nutzer_pro_m2=b.gebaeude.nutz_kwh_m2,
    )
    wb = berechne_waermebedarf(
        jahres_heizbedarf_kwh=b.gebaeude.jahres_heizwert,
        verteilungsverlust_kwh=b.gebaeude.verteilungsverlust_kwh,
        speicherverlust_kwh=b.gebaeude.speicherverlust_kwh,
        warmwasserbedarf_kwh=b.gebaeude.warmwasserbedarf_kwh,
    )
    ee = berechne_endenergiebedarf(b.nf, sb, wb)

    context = {
        'bauteil': b,
        'nutzenergie': ne,
        'strom': sb,
        'waerme': wb,
        'endenergie': ee,
    }
    return render(request, 'mylist/ergebnis.html', context)


# ————— PDF-Export —————

def ergebnis_pdf(request, bauteil_id):
    b = get_object_or_404(Bauteil, pk=bauteil_id)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(w/2, h-80, f"Ergebnis Bauteil #{b.pk}")

    p.setFont("Helvetica", 12)
    y = h - 120
    for label, val in [
        ("Gebäudehöhe (m)", b.hoehe),
        ("Volumen (m³)", b.volumen),
        ("NF (m²)", b.nf),
        ("Neuz. absolut", b.ne_absolut),
        ("Endenergie absolut", b.ee_absolut),
    ]:
        p.drawString(80, y, f"{label}: {val}")
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)
    resp = HttpResponse(buffer, content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename="ergebnis_bauteil_{b.pk}.pdf"'
    return resp


# ————— JSON-API —————

def api_berechnung(request):
    laenge = float(request.GET.get("laenge", 0))
    breite = float(request.GET.get("breite", 0))
    geschosshoehe = float(request.GET.get("geschosshoehe", 0))
    anz_geschosse = int(request.GET.get("anz_geschosse", 0))

    geb = berechne_gebaeudedaten(laenge, breite, geschosshoehe, anz_geschosse)
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

    return JsonResponse({
        "gebaeudedaten": geb,
        "nutzenergie":   ne,
        "strombedarf":   sb,
        "waermebedarf":  wb,
        "endenergie":    ee,
    })



