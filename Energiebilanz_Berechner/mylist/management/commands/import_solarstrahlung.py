# mylist/management/commands/import_solarstrahlung.py

import os
import csv

from django.core.management.base import BaseCommand
from mylist.models import SolarStrahlungMonat

class Command(BaseCommand):
    help = "Importiert die monatlichen Solarstrahlungswerte aus csv/solarstrahlung_fichtelberg.csv"

    def handle(self, *args, **options):
        # 1) Verzeichnis dieser Datei herausfinden
        this_dir = os.path.dirname(__file__)
        #    → .../mylist/management/commands

        # 2) Pfad zur CSV im Unterordner 'csv'
        csv_path = os.path.join(this_dir, 'csv', 'solarstrahlung_fichtelberg.csv')

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"CSV-Datei nicht gefunden: {csv_path}"))
            return

        # 3) Bestehende Datensätze löschen (wenn ein Neuimport gewünscht ist)
        SolarStrahlungMonat.objects.all().delete()

        # 4) CSV mit korrektem Encoding öffnen (Umlaute in deutschen Ortsnamen etc.)
        with open(csv_path, newline='', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Felder aus der Zeile extrahieren
                    region      = int(row['region'])
                    referenzort = row['referenzort'].strip()
                    orientation = row['orientation'].strip()
                    neigung     = int(row['neigung'])

                    # Monate als Integer
                    jan  = int(row['jan'])
                    feb  = int(row['feb'])
                    maerz= int(row['maerz'])
                    apr  = int(row['apr'])
                    mai  = int(row['mai'])
                    jun  = int(row['jun'])
                    jul  = int(row['jul'])
                    aug  = int(row['aug'])
                    sep  = int(row['sep'])
                    okt  = int(row['okt'])
                    nov  = int(row['nov'])
                    dez  = int(row['dez'])

                    # Jahreswert als Integer
                    jahreswert = int(row['jahreswert'])

                except (KeyError, ValueError):
                    # Ungültige Zeile überspringen
                    continue

                SolarStrahlungMonat.objects.create(
                    region=region,
                    referenzort=referenzort,
                    orientation=orientation,
                    neigung=neigung,
                    jan=jan,
                    feb=feb,
                    maerz=maerz,
                    apr=apr,
                    mai=mai,
                    jun=jun,
                    jul=jul,
                    aug=aug,
                    sep=sep,
                    okt=okt,
                    nov=nov,
                    dez=dez,
                    jahreswert=jahreswert
                )

        self.stdout.write(self.style.SUCCESS(
            "✅ Solare Strahlungsdaten (Fichtelberg) erfolgreich importiert."
        ))
