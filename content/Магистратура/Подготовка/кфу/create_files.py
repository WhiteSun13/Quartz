import os

# --- Настройки ---
# Имя файла, из которого будем читать названия
SOURCE_FILE = "names.txt"
# Название папки, куда будут сохраняться созданные файлы
OUTPUT_DIR = "markdown_files"
# -----------------

def create_markdown_files():
    """
    Читает названия из SOURCE_FILE и создает пронумерованные markdown-файлы
    в директории OUTPUT_DIR.
    """
    # Создаем папку для результатов, если она еще не существует
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
            print(f"✔ Создана директория: '{OUTPUT_DIR}'")
        except OSError as e:
            print(f"✖ Ошибка при создании директории: {e}")
            return

    # Проверяем, существует ли исходный файл
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            # Считываем все строки, убирая пустые
            titles = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"✖ Ошибка: Исходный файл '{SOURCE_FILE}' не найден.")
        print("Пожалуйста, создайте этот файл и поместите в него названия.")
        return

    if not titles:
        print("ℹ Исходный файл пуст. Файлы не созданы.")
        return

    # Определяем, сколько знаков нужно для нумерации (для красивого выравнивания)
    # Например, если файлов 120, то нумерация будет 001, 002... 120
    # Если файлов 99, то нумерация будет 01, 02... 99
    # Если же файлов 9, то 1, 2... 9
    padding = len(str(len(titles)))
    # Но по задаче нужно минимум 2 знака (01, 02...), поэтому:
    if padding < 2:
        padding = 2

    print(f"\nНачинаю создание {len(titles)} файлов...")

    # Используем enumerate для получения индекса и названия
    for i, title in enumerate(titles, start=1):
        # Форматируем номер файла с ведущими нулями
        # f"{i:0{padding}d}" -> i - число, 0 - символ для заполнения, padding - ширина
        # Например, для i=1 и padding=2 результат будет "01"
        # Для i=10 и padding=2 результат будет "10"
        # Для i=100 и padding=2 результат будет "100" (т.к. 2 - минимальная ширина)
        file_number = f"{i:0{padding}d}"

        # Собираем полное имя файла
        file_name = f"{file_number} {title}.md"
        
        # Формируем полный путь к файлу
        full_path = os.path.join(OUTPUT_DIR, file_name)

        try:
            # Создаем и открываем файл для записи
            with open(full_path, 'w', encoding='utf-8') as md_file:
                # В качестве бонуса добавим в сам файл заголовок первого уровня
                md_file.write(f"# {title}\n")
            print(f"  Создан: {file_name}")
        except OSError as e:
            # Обрабатываем возможные ошибки, например, недопустимые символы в имени
            print(f"✖ Не удалось создать файл '{file_name}'. Ошибка: {e}")

    print(f"\n🎉 Работа завершена! Все файлы в папке '{OUTPUT_DIR}'.")


def create_demo_source_file():
    """Создает демонстрационный файл names.txt для проверки."""
    if os.path.exists(SOURCE_FILE):
        return
        
    print(f"Создаю демонстрационный файл '{SOURCE_FILE}'...")
    try:
        with open(SOURCE_FILE, 'w', encoding='utf-8') as f:
            f.write("Первое название\n")
            f.write("Второе название\n")
            f.write("Третий файл с цифрами 123\n")
            f.write("\n") # пустая строка для проверки
            f.write("Как работать с Git\n")
            # Добавим много строк, чтобы проверить нумерацию > 100
            for i in range(5, 105):
                f.write(f"Тестовый файл номер {i}\n")
    except OSError as e:
        print(f"✖ Не удалось создать демонстрационный файл: {e}")


if __name__ == "__main__":
    # 1. Создаем тестовый файл `names.txt`, если его нет
    # create_demo_source_file()
    
    # 2. Запускаем основную функцию
    create_markdown_files()