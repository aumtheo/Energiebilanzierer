import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from mylist.models import DruckverlustBauteil

class Command(BaseCommand):
    help = "Importiert bauteil_druckverlust.csv aus mylist/management/commands/csv/"

    def handle(self, *args, **options):
        # BASE_DIR ist das Verzeichnis, in dem manage.py liegt
        base_dir = settings.BASE_DIR

        # Pfad zur CSV in commands/csv/
        csv_path = os.path.join(
            base_dir,
            'mylist',
            'management',
            'commands',
            'csv',
            'bauteil_druckverlust.csv'
        )

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"CSV-Datei nicht gefunden: {csv_path}"))
            return

        df = pd.read_csv(csv_path)

        DruckverlustBauteil.objects.all().delete()
        for _, row in df.iterrows():
            DruckverlustBauteil.objects.create(
                bauteil=row['bauteil'],
                druckverlust_pa=int(row['druckverlust_pa'])
            )

        self.stdout.write(self.style.SUCCESS("✅ Druckverlust-Daten erfolgreich importiert."))

