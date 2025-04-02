import re
import random
import string
import pandas as pd

def generate_email(name, last_name):
    return f"{name.lower()}.{last_name.lower()}@example.com"

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + './#$@%!?'
    return ''.join(random.choice(characters) for i in range(length))

def is_valid_name(name):
    return bool(re.match(r"^[A-ZА-Я][a-zа-я\-]+$", name))

def is_valid_tel(tel):
    return bool(re.match(r"^\d{7,15}$", tel))

def is_valid_city(city):
    return bool(re.match(r"^[A-ZА-Я][a-zа-яA-Za-zа-я .\-_]*[A-Za-zа-я]$", city))

def clean_data(input_file, output_file, invalid_file):
    valid_rows = []
    invalid_rows = []

    # Читаем данные из файла
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]  # Пропускаем заголовок

        for line in lines:
            parts = line.strip().split(', ')
            try:
                if not is_valid_name(parts[1]):
                    raise ValueError("Имя неправильное")
                if not is_valid_name(parts[2]):
                    raise ValueError("Фамилия неправильная")
                if not is_valid_tel(parts[3]):
                    raise ValueError("Телефон неправильный")
                if not is_valid_city(parts[4]):
                    raise ValueError("Город неправильный")

                if parts[0] != '':
                    valid_rows.append(parts)
                    raise ValueError("Строка заполнена")

                generated_email = generate_email(parts[1], parts[2])
                password = generate_password()
                valid_rows.append([generated_email, parts[1], parts[2], parts[3], parts[4], password])

            except ValueError as e:
                # print(e)
                if e != "Строка заполнена":
                    invalid_rows.append(line.strip())

    # Записываем валидные данные обратно в файл
    df_valid = pd.DataFrame(valid_rows, columns=["EMAIL", "NAME", "LAST_NAME", "TEL", "CITY", "PASSWORD"])
    df_valid.to_csv(output_file, index=False)

    # Открываем файл и добавляем пробелы после запятых
    with open(output_file, 'r') as file:
        data = file.read()
    data = data.replace(',', ', ')
    with open(output_file, 'w') as file:
        file.write(data)

    # Записываем невалидные данные в отдельный файл
    with open(invalid_file, 'w', encoding='utf-8') as f:
        for invalid_line in invalid_rows:
            f.write(invalid_line + '\n')


if __name__ == "__main__":
    clean_data('01ds.txt', 'output.txt', 'invalid.txt')