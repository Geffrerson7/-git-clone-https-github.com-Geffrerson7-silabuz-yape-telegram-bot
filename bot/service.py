import re, random, requests, os
import pandas as pd
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse


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


def procesar_imagen(url, sku, carpeta_destino):
    """Function to download and process an image."""

    enlaces_separados = url.split("|")

    for i, enlace in enumerate(enlaces_separados, start=1):
        nombre_archivo = f"{sku}-{i}.jpg"  # Nombre del archivo será SKU-i.jpg
        ruta_archivo = os.path.join(
            carpeta_destino, nombre_archivo
        )  # Ruta completa del archivo

        try:
            respuesta = requests.get(enlace.strip())  # Eliminar espacios en blanco
            if respuesta.ok:
                imagen = Image.open(BytesIO(respuesta.content))
                # Verificar si la imagen ya tiene las dimensiones y el formato requeridos
                if imagen.size == (1000, 1000) and imagen.format == "JPEG":
                    print(
                        f"La imagen {enlace} ya está en las dimensiones y formato requeridos. Descargando sin modificar."
                    )
                    with open(ruta_archivo, "wb") as f:
                        f.write(respuesta.content)
                    continue  # Pasar a la próxima iteración sin procesar la imagen

                imagen = imagen.convert("RGB")  # Convertir la imagen a formato RGB

                # Redimensionar la imagen manteniendo su relación de aspecto original
                max_dimension = 1000
                ancho, alto = imagen.size
                proporcion = max_dimension / max(ancho, alto)
                nuevo_ancho = round(ancho * proporcion)
                nuevo_alto = round(alto * proporcion)
                imagen = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

                # Crear un lienzo blanco de 1000x1000 píxeles y pegar la imagen en el centro
                lienzo = Image.new("RGB", (max_dimension, max_dimension), color="white")
                posicion_x = (max_dimension - nuevo_ancho) // 2
                posicion_y = (max_dimension - nuevo_alto) // 2
                lienzo.paste(imagen, (posicion_x, posicion_y))

                lienzo.save(
                    ruta_archivo, "JPEG", quality=95
                )  # Guardar la imagen en formato JPEG
                print(f"Imagen guardada: {ruta_archivo}")
            else:
                print(f"Error al descargar la imagen {enlace}: {respuesta.status_code}")
        except Exception as e:
            print(f"Error al procesar la imagen {enlace}: {e}")


def save_images_from_excel(archivo_excel, carpeta_destino):
    """Extracts image URLs from an Excel file and saves the corresponding images to the specified destination folder."""
    df = pd.read_excel(archivo_excel)

    for index, fila in df.iterrows():
        enlaces_imagen = fila["url"]
        sku = fila["SKU"]
        if not pd.isna(enlaces_imagen) and enlaces_imagen !="":
            procesar_imagen(enlaces_imagen, sku, carpeta_destino)


def check_excel_path(ruta):
    """Verifies if the provided path has the correct format."""
    if not ruta:
        return False

    if not os.path.isabs(ruta):
        return False

    if not os.path.exists(ruta):
        os.makedirs(ruta)

    return True


def check_url(url):
    """Verifies if the URL has the correct format and if it is accessible."""

    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return True

    try:
        response = requests.head(url)
        if response.ok:
            return True
        elif response.status_code == 403:
            return 403
    except requests.ConnectionError:
        return False
    

def create_excel_non_working_urls(archivo_excel, carpeta_destino):
    """Reads an Excel file containing URLs, checks if they are valid and accessible, and saves the non-working URLs to a new Excel file."""
    try:

        df = pd.read_excel(archivo_excel)

        urls_no_funcionan = []

        for index, fila in df.iterrows():

            # Verificar si el valor en la columna "url" es una cadena antes de intentar dividirla
            enlaces_imagen = fila["url"]
            if pd.notnull(enlaces_imagen) and isinstance(enlaces_imagen, str):
                # Dividir los enlaces por los separadores "|"
                urls = enlaces_imagen.split("|")
                sku = fila["SKU"]
                for url in urls:
                    if check_url(url) == False:
                        urls_no_funcionan.append(
                            {
                                "SKU": sku,
                                "URL": url,
                                "Comentario": "URL no válida",
                            }
                        )
                        print(f"URL no funciona para SKU {sku}: {url}")
                    elif check_url(url) == 403:
                        urls_no_funcionan.append(
                            {
                                "SKU": sku,
                                "URL": url,
                                "Comentario": "URL válida, pero no se puede descargar con este programa sino de forma manual.",
                            }
                        )
            else:
                sku = fila["SKU"]
                urls_no_funcionan.append(
                    {"SKU": sku, "URL": enlaces_imagen, "Comentario": "Celda vacía"}
                )
                print(f"URL está vacía para SKU {sku}")

        df_urls_no_funcionan = pd.DataFrame(urls_no_funcionan)

        archivo_resultado = os.path.join(carpeta_destino, "failed_urls.xlsx")
        df_urls_no_funcionan.to_excel(archivo_resultado, index=False)

        print(f"Se han guardado las URL que no funcionan en '{archivo_resultado}'.")
    except Exception as e:
        print(f"Error al procesar el archivo Excel: {e}")




