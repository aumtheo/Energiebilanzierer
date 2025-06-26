# mylist/management/commands/import_sonneneintragskennwerte.py

import csv
import os
from django.core.management.base import BaseCommand, CommandError
from mylist.models import SonneneintragsKennwert

class Command(BaseCommand):
    help = "Importiert die Sonneneintragskennwerte aus sonneneintragskennwerte.csv"

    def handle(self, *args, **options):
        # 1) Existierende Datensätze löschen, damit nicht doppelt importiert wird
        try:
            SonneneintragsKennwert.objects.all().delete()
        except Exception as e:
            raise CommandError(f"Fehler beim Löschen alter Datensätze: {e}")

        # 2) Pfad zur CSV-Datei zusammensetzen:
        base_dir = os.path.dirname(__file__)        # …/mylist/management/commands
        csv_dir  = os.path.join(base_dir, 'csv')    # …/mylist/management/commands/csv
        csv_path = os.path.join(csv_dir, 'sonneneintragskennwerte.csv')

        if not os.path.isfile(csv_path):
            raise CommandError(f"CSV-Datei nicht gefunden: {csv_path}")

        # 3) CSV einlesen
        with open(csv_path, encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                # a) Kommentar-/Leerzeilen überspringen
                if row.get('kennwert_key', '').startswith('#') or not row.get('kennwert_key'):
                    continue

                # b) Neues ORM-Objekt anlegen
                obj = SonneneintragsKennwert(
                    typ             = row['typ'].strip(),
                    kennwert_key    = row['kennwert_key'].strip(),
                    beschreibung    = row['beschreibung'].strip(),
                    bauart          = row.get('bauart', '').strip() or None,
                    wohng_A         = float(row['wohng_A']) if row.get('wohng_A') not in (None, '') else None,
                    wohng_B         = float(row['wohng_B']) if row.get('wohng_B') not in (None, '') else None,
                    wohng_C         = float(row['wohng_C']) if row.get('wohng_C') not in (None, '') else None,
                    nw_A            = float(row['nw_A'])    if row.get('nw_A')    not in (None, '') else None,
                    nw_B            = float(row['nw_B'])    if row.get('nw_B')    not in (None, '') else None,
                    nw_C            = float(row['nw_C'])    if row.get('nw_C')    not in (None, '') else None,
                )
                obj.save()
                count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {count} Sonneneintragskennwerte importiert."))



