import re, random
import pandas as pd


def generate_random_numbers(random_numbers_quantity: int):
    """Generates a list of random EAN codes of 13 digits."""
    numbers = []
    for _ in range(random_numbers_quantity):
        # Generar el primer dígito aleatorio, asegurándonos de que no sea cero
        first_digit = str(random.randint(1, 9))
        # Generar los restantes 12 dígitos aleatorios
        remaining_digits = "".join([str(random.randint(0, 9)) for _ in range(12)])
        # Combinar los dígitos para formar el número completo
        number = first_digit + remaining_digits
        numbers.append(number)
    return numbers


def save_to_excel(numbers_list: list):
    """Saves a list of EAN codes to an Excel file."""
    df = pd.DataFrame({"EAN": numbers_list})
    df.to_excel("./excel-files/ean_codes.xlsx", index=False)


def escape_string(input_string: str):
    """Replaces characters '-' with '\-', and characters '.' with '\.'"""
    return re.sub(r"[-.]", lambda x: "\\" + x.group(), input_string)
