import re, random
import pandas as pd
from bs4 import BeautifulSoup

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
    df.to_excel("./excel-files/ean/ean_codes.xlsx", index=False)


def escape_string(input_string: str):
    """Replaces characters '-' with '\-', and characters '.' with '\.'"""
    return re.sub(r"[-.]", lambda x: "\\" + x.group(), input_string)

def html_to_text(html):
    """Convert a snippet of HTML into plain text."""
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def change_html_to_text():
    """ Read an Excel file containing HTML in a specified column, convert that HTML into plain text
    using the html_to_text function, and save the result to a new Excel file."""
    
    df = pd.read_excel("./excel-files/descriptions/description-html.xlsx")

    # Aplicar la función html_to_text a cada valor de la columna 'columna_html'
    df['columna_texto'] = df['columna_html'].apply(html_to_text)

    # Guardar el DataFrame resultante en un nuevo archivo Excel
    df.to_excel('./excel-files/descriptions/description-text.xlsx', index=False)