import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from mylist.models import SonnenschutzFaktor  # passender Model‐Name

class Command(BaseCommand):
    help = "Importiert sonnenschutzfaktor.csv aus mylist/management/commands/csv/"

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        csv_path = os.path.join(
            base_dir,
            'mylist', 'management', 'commands', 'csv', 'sonnenschutzfaktor.csv'
        )

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"CSV-Datei nicht gefunden: {csv_path}"))
            return

        df = pd.read_csv(csv_path)

        # Alte Daten löschen
        SonnenschutzFaktor.objects.all().delete()

        # Neue Datensätze anlegen
        for _, row in df.iterrows():
            SonnenschutzFaktor.objects.create(
                zeile=row['zeile'],
                sonnenschutzvorrichtung=row['sonnenschutzvorrichtung'],
                f_c_g_le_0_40_zweifach=float(row['f_c_g_le_0_40_zweifach']),
                f_c_g_le_0_40_dreifach=float(row['f_c_g_le_0_40_dreifach']),
                f_c_g_gt_0_40_zweifach=float(row['f_c_g_gt_0_40_zweifach']),
            )

        self.stdout.write(self.style.SUCCESS("✅ Sonnenschutzfaktoren erfolgreich importiert."))
