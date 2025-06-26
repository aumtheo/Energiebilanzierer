import os
from django.conf import settings
import pandas as pd
from django.core.management.base import BaseCommand
from mylist.models import KlimaregionTemperatur

class Command(BaseCommand):
    help = "Importiert klimadaten_full.csv aus dem Projekt-Root"

    def handle(self, *args, **options):
        # settings.BASE_DIR verweist auf den Ordner, der manage.py enthält
        csv_path = os.path.join(settings.BASE_DIR, 'klimadaten_full.csv')

        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"CSV-Datei nicht gefunden: {csv_path}"))
            return

        KlimaregionTemperatur.objects.all().delete()
        for _, row in df.iterrows():
            KlimaregionTemperatur.objects.create(
                region=int(row['region']),
                referenzort=row['referenzort'],
                jan=float(row['jan']),
                feb=float(row['feb']),
                maer=float(row['maer']),
                apr=float(row['apr']),
                mai=float(row['mai']),
                jun=float(row['jun']),
                jul=float(row['jul']),
                aug=float(row['aug']),
                sep=float(row['sep']),
                okt=float(row['okt']),
                nov=float(row['nov']),
                dez=float(row['dez']),
                jahreswert=float(row['jahreswert']),
            )

        self.stdout.write(self.style.SUCCESS("✅ Klimadaten wurden erfolgreich importiert."))
