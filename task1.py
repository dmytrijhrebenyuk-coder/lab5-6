import requests
import json
import csv


def fetch_world_bank_data(indicator: str, year: int):
    """
    Надсилає HTTP-запит до API Світового банку та повертає дані у вигляді структур даних Python.
    Параметр per_page=1000 дозволяє отримати всі країни на одній сторінці.
    """
    url = f"http://api.worldbank.org/v2/country/all/indicator/{indicator}?date={year}&format=json&per_page=1000"
    print(f"Надсилання запиту до API: {url}")
    
    try:
        response = requests.get(url, timeout=15)
        # Перевірка успішності виконання запиту за кодом відповіді сервера (status_code)
        if response.status_code == 200:
            print("Запит успішно виконано (status_code = 200).\n")
            return response.json()
        else:
            print(f"Помилка сервера! Код відповіді: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Помилка під час виконання HTTP-запиту: {e}")
        return None


def save_to_json(data: list, filename: str) -> bool:
    """Зберігає отримані дані у файл формату .json."""
    try:
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Дані успішно збережено у файл '{filename}'.")
        return True
    except IOError as e:
        print(f"Помилка запису у JSON-файл '{filename}': {e}")
        return False


def convert_json_to_csv(json_data: list, csv_filename: str, year: int) -> bool:
    """
    Виділяє необхідні поля з JSON-структури та зберігає їх у .csv файл
    відповідно до формату з прикладу (роздільник ';').
    """
    if not json_data or len(json_data) < 2 or not json_data[1]:
        print("Помилка: JSON-дані порожні або мають некоректну структуру.")
        return False

    records = json_data[1]  # У другому елементі списку містяться записи по країнах
    headers = ["Country Name", "Country Code", "Series Name", "Series Code", f"{year} [YR{year}]"]

    try:
        with open(csv_filename, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(headers)

            for item in records:
                country_name = item.get("country", {}).get("value", "")
                # Використовуємо трилітерний код країни ISO3 (або резервний id)
                country_code = item.get("countryiso3code") or item.get("country", {}).get("id", "")
                series_name = item.get("indicator", {}).get("value", "")
                series_code = item.get("indicator", {}).get("id", "")
                
                val = item.get("value")
                # Приводимо формат числа до вигляду з методички (кома як десятковий роздільник або '..' за відсутності)
                if val is None:
                    formatted_val = ".."
                else:
                    formatted_val = str(val).replace(".", ",")

                writer.writerow([country_name, country_code, series_name, series_code, formatted_val])

        print(f"Дані успішно перетворено та збережено у файл '{csv_filename}'.\n")
        return True
    except IOError as e:
        print(f"Помилка під час роботи з CSV-файлом '{csv_filename}': {e}")
        return False


def display_file_content(filename: str, max_lines: int | None = 25):
    """Виводить зміст файлу на екран з обробленням виняткових ситуацій."""
    print("=" * 80)
    print(f"ЗМІСТ ФАЙЛУ: {filename} (показано перші {max_lines} рядків)")
    print("=" * 80)
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            for i, line in enumerate(file):
                if max_lines is not None and i >= max_lines:
                    print(f"... [Виведення скорочено. Повний зміст збережено у файлі {filename}] ...")
                    break
                print(line, end="")
        print("\n")
    except FileNotFoundError:
        print(f"Помилка: Файл '{filename}' не знайдено!\n")
    except IOError as e:
        print(f"Помилка читання файлу '{filename}': {e}\n")


def main():
    INDICATOR = "SP.DYN.LE00.IN"  # Life expectancy at birth, total (years)
    YEAR = 2019
    JSON_FILE = "life_expectancy_2019.json"
    CSV_FILE = "life_expectancy_2019.csv"

    # 1. Одержання даних через API
    data = fetch_world_bank_data(INDICATOR, YEAR)
    
    if data:
        # 2. Збереження у формат JSON
        if save_to_json(data, JSON_FILE):
            # 3. Перетворення у формат CSV
            if convert_json_to_csv(data, CSV_FILE, YEAR):
                # 4. Виведення змісту файлів на екран
                # Щоб вивести файли повністю, замініть max_lines=30 на max_lines=None
                display_file_content(JSON_FILE, max_lines=30)
                display_file_content(CSV_FILE, max_lines=35)


if __name__ == "__main__":
    main()