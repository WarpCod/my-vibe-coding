import os
import shutil
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    Image = None

import sys

PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.tiff', '.bmp', '.gif', '.webp'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.3gp', '.webm', '.mts', '.m2ts'}

def get_exif_datetime(img_path):
    if Image is None:
        return None
    try:
        image = Image.open(img_path)
        exif = image._getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag in ('DateTimeOriginal', 'DateTimeDigitized', 'DateTime'):
                    try:
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    except Exception:
                        continue
    except Exception:
        return None
    return None

def get_video_creation_date(file_path):
    return None

def get_file_date(file_path):
    ext = file_path.suffix.lower()
    if ext in PHOTO_EXTENSIONS:
        dt = get_exif_datetime(str(file_path))
        if dt:
            return dt
    # Если метаданных нет, берем дату изменения файла
    t = file_path.stat().st_mtime
    return datetime.fromtimestamp(t)

def organize_media(folder_path):
    folder = Path(folder_path)
    for root, _, files in os.walk(folder):
        # Пропускаем папки, которые мы сами создали (2020, 2021 и т.д.), 
        # чтобы скрипт не ушел в бесконечный цикл
        if any(Path(root).name == str(year) for year in range(1900, 2100)):
            continue

        for file in files:
            # Игнорируем скрытые файлы macOS
            if file.startswith('.') or file.startswith('._'):
                continue
                
            fpath = Path(root) / file
            ext = fpath.suffix.lower()
            
            if ext not in PHOTO_EXTENSIONS and ext not in VIDEO_EXTENSIONS:
                continue
                
            dt = get_file_date(fpath)
            year = dt.strftime('%Y')
            month = dt.strftime('%m')
            
            dest_dir = folder / year / month
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            dest = dest_dir / file
            count = 1
            while dest.exists():
                name, suffix = os.path.splitext(file)
                dest = dest_dir / f"{name}_{count}{suffix}"
                count += 1
            
            try:
                shutil.move(str(fpath), dest)
                print(f"✅ Перенесено: {file} -> {year}/{month}")
            except Exception as e:
                print(f"❌ Ошибка с файлом {file}: {e}")

if __name__ == "__main__":
    folder_path = '/Volumes/T5 EVO/с 4 тб копия/АРХИВ'
    
    if os.path.exists(folder_path):
        print(f"✅ Система видит диск и папку: {folder_path}")
        print("🚀 Начинаю большую сортировку...")
        organize_media(folder_path)
        print("✨ ВСЁ ГОТОВО! Весь архив разобран по годам и месяцам.")
    else:
        print(f"❌ Ошибка: Путь не найден! Проверь, подключен ли диск T5 EVO.")