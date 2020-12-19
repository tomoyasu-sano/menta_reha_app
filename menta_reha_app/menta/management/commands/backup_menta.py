import csv
import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Menta


class Command(BaseCommand):
    help = "Backup Menta data"

    def handle(self, *args, **options):
        # 実行時のYYYYMMDDを取得
        date = datetime.date.today().strftime("%Y%m%d")

        # 保存ファイルの相対パス
        file_path = settings.BACKUP_PATH + 'menta_' + date + '.csv'

        # 保存ディレクトリが存在しなければ作成
        os.makedirs(settings.BACKUP_PATH, exist_ok=True)

        # バックアップファイルの作成
        with open(file_path, 'w') as file:
            writer = csv.writer(file)

            # ヘッダーの書き込み
            header = [field.name for field in Menta._meta.fields]
            writer.writerow(header)

            # Mentaテーブルの全データを取得
            mentas = Menta.objects.all()

            # データ部分の書き込み
            for menta in mentas:
                writer.writerow([str(menta.user),
                                 menta.title,
                                 menta.content,
                                 str(menta.photo1),
                                 str(menta.photo2),
                                 str(menta.photo3),
                                 str(menta.created_at),
                                 str(menta.updated_at)])

        # 保存ディレクトリのファイルリストを取得
        files = os.listdir(settings.BACKUP_PATH)
        # ファイルが設定数以上あったら一番古いファイルを削除
        if len(files) >= settings.NUM_SAVED_BACKUP:
            files.sort()
            os.remove(settings.BACKUP_PATH + files[0])
