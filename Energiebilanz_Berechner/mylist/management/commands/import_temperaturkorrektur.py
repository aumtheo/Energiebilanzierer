# mylist/management/commands/import_temperaturkorrektur.py

# mylist/management/commands/import_temperaturkorrektur.py

import os
import csv

from django.core.management.base import BaseCommand
from mylist.models import Temperaturkorrekturfaktor

class Command(BaseCommand):
    help = "Importiert Temperaturkorrekturfaktoren aus mylist/management/commands/csv/."

    def handle(self, *args, **options):
        # 1. Verzeichnis dieser Datei:
        this_dir = os.path.dirname(__file__)  
        #    → <...>/mylist/management/commands

        # 2. In den Unterordner 'csv' wechseln und dort die Datei öffnen:
        csv_path = os.path.join(this_dir, 'csv', 'temperaturkorrekturfaktoren.csv')

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"CSV-Datei nicht gefunden: {csv_path}"))
            return

        # 3. Vorhandene Einträge löschen (falls nötig):
        Temperaturkorrekturfaktor.objects.all().delete()

        # 4. CSV einlesen und Datensätze anlegen
        with open(csv_path, newline='', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                bauteil_name = row.get('Bauteil', '').strip()
                fx_str       = row.get('Fx', '').replace(',', '.').strip()

                if not bauteil_name or not fx_str:
                    continue  # unvollständige Zeile überspringen

                try:
                    fx_wert = float(fx_str)
                except ValueError:
                    continue

                Temperaturkorrekturfaktor.objects.create(
                    bauteil=bauteil_name,
                    fx=fx_wert
                )

        self.stdout.write(self.style.SUCCESS(
            "✅ Temperaturkorrekturfaktoren wurden erfolgreich importiert."
        ))

