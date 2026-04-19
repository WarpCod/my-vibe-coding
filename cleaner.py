import os
from pathlib import Path

def clean_up(folder_path):
    folder = Path(folder_path)
    
    print(f"\n🧹 Начинаю генеральную уборку в: {folder}")

    # Список мусора и расширений
    junk_patterns = ['.DS_Store', 'Thumbs.db']
    junk_extensions = ['.lnk', '.url']
    
    deleted_files_count = 0
    deleted_dirs_count = 0
    
    for root, dirs, files in os.walk(folder, topdown=False):
        for file in files:
            file_path = Path(root) / file
            
            is_junk = file in junk_patterns or \
                      file.startswith('._') or \
                      any(file.lower().endswith(ext) for ext in junk_extensions)
            
            if is_junk:
                try:
                    file_path.unlink()
                    print(f"   🗑️ Удален мусор/ярлык: {file}")
                    deleted_files_count += 1
                except Exception as e:
                    print(f"   ⚠️ Не удалось удалить {file}: {e}")

        # Удаление пустых папок
        for name in dirs:
            dir_path = Path(root) / name
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"   📂 Удалена пустая папка: {name}")
                    deleted_dirs_count += 1
            except Exception as e:
                continue
                
    print(f"\n✨ Готово! Удалено файлов: {deleted_files_count}, папок: {deleted_dirs_count}")

if __name__ == "__main__":
    print("--- Программа очистки архива от мусора и ярлыков ---")
    
    # Теперь скрипт спрашивает путь у пользователя
    user_path = input("👉 Введите путь к папке для очистки: ").strip()
    
    # Убираем кавычки, если пользователь случайно скопировал путь с ними
    user_path = user_path.replace('"', '').replace("'", "")
    
    if os.path.exists(user_path):
        confirm = input(f"❓ Выполнить очистку в '{user_path}'? (y/n): ")
        if confirm.lower() == 'y':
            clean_up(user_path)
        else:
            print("❌ Операция отменена.")
    else:
        print(f"❌ Ошибка: Путь '{user_path}' не найден. Проверьте правильность ввода.")