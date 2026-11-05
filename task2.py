import csv


def search_countries_in_csv(input_csv: str, output_csv: str, target_countries: list):
    """
    Виконує пошук даних для введених користувачем назв країн у вихідному CSV-файлі
    та записує знайдені результати в новий CSV-файл.
    """
    # Приводимо шукані назви країн до нижнього регістру для нечутливого до регістру пошуку
    search_set = {country.strip().lower() for country in target_countries if country.strip()}
    
    if not search_set:
        print("Список країн для пошуку порожній!")
        return

    found_rows = []
    found_names = set()

    # Читання вихідного CSV-файлу з обробленням помилок відкриття файлу
    try:
        with open(input_csv, mode="r", encoding="utf-8") as infile:
            reader = csv.reader(infile, delimiter=";")
            
            try:
                header = next(reader)  # Зчитуємо заголовок таблиці
            except StopIteration:
                print(f"Помилка: Файл '{input_csv}' порожній.")
                return

            for row in reader:
                if row and len(row) > 0:
                    country_name = row[0].strip()
                    if country_name.lower() in search_set:
                        found_rows.append(row)
                        found_names.add(country_name.lower())

    except FileNotFoundError:
        print(f"Помилка: Вихідний файл '{input_csv}' не знайдено! Спочатку виконайте Завдання 1.")
        return
    except PermissionError:
        print(f"Помилка: Немає прав доступу для читання файлу '{input_csv}'.")
        return
    except IOError as e:
        print(f"Помилка під час відкриття або читання файлу '{input_csv}': {e}")
        return

    # Виведення результатів пошуку в консоль
    if not found_rows:
        print("\nЗа вашим запитом не знайдено жодної країни.")
        return

    print(f"\nЗнайдено записів: {len(found_rows)}")
    print("-" * 80)
    print(";".join(header))
    for row in found_rows:
        print(";".join(row))
    print("-" * 80)

    # Повідомляємо, якщо деякі з введених країн не були знайдені
    not_found = search_set - found_names
    if not_found:
        print(f"Примітка: наступні країни не знайдено в базі: {', '.join(not_found)}")

    # Запис результатів пошуку в новий CSV-файл з обробленням винятків
    try:
        with open(output_csv, mode="w", encoding="utf-8", newline="") as outfile:
            writer = csv.writer(outfile, delimiter=";")
            writer.writerow(header)
            writer.writerows(found_rows)
        print(f"\nРезультати пошуку успішно записано в новий файл '{output_csv}'.")
    except PermissionError:
        print(f"Помилка: Немає прав доступу для запису у файл '{output_csv}' (можливо, він відкритий в іншій програмі).")
    except IOError as e:
        print(f"Помилка під час збереження файлу '{output_csv}': {e}")


def main():
    INPUT_CSV_FILE = "life_expectancy_2019.csv"
    OUTPUT_CSV_FILE = "search_results_2019.csv"

    print(" Пошук даних про очікувану тривалість життя (2019 р.) ")
    print("Введіть назви країн англійською мовою через кому")
    print("(наприклад: Ukraine, Poland, Germany, Australia, Canada):")
    
    user_input = input("> ")
    countries_to_find = user_input.split(",")

    search_countries_in_csv(INPUT_CSV_FILE, OUTPUT_CSV_FILE, countries_to_find)


if __name__ == "__main__":
    main()