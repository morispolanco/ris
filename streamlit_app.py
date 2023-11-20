# Importar las librerías necesarias
import streamlit as st
import requests
import re
import zipfile
import io

# Crear una función para buscar una referencia bibliográfica en internet y devolver una ficha .ris con los datos recopilados
def buscar_referencia(referencia):
  # Usar el servicio de Bing para obtener los resultados de la búsqueda web
  url = "https://api.bing.microsoft.com/v7.0/search"
  headers = {"Ocp-Apim-Subscription-Key": "tu_clave_de_suscripción"}
  params = {"q": referencia, "count": 1}
  response = requests.get(url, headers=headers, params=params)
  data = response.json()

  # Extraer el título, el autor, la fecha, la fuente y el enlace del primer resultado
  titulo = data["webPages"]["value"][0]["name"]
  autor = data["webPages"]["value"][0]["snippet"].split("-")[0].strip()
  fecha = data["webPages"]["value"][0]["dateLastCrawled"].split("T")[0]
  fuente = data["webPages"]["value"][0]["displayUrl"]
  enlace = data["webPages"]["value"][0]["url"]

  # Crear una ficha .ris con el formato adecuado
  ficha = f"""TY  - GEN
TI  - {titulo}
AU  - {autor}
PY  - {fecha}
UR  - {enlace}
PB  - {fuente}
ER  - 
"""
  return ficha

# Crear la interfaz de la app de streamlit
st.title("App de streamlit para buscar referencias bibliográficas")
st.write("Esta app toma una lista de referencias bibliográficas y busca cada entrada en internet; luego, con los datos recopilados, hace una ficha .ris por cada entrada. Por último, comprime las fichas y genera un zip.")

# Crear un campo de texto para que el usuario introduzca la lista de referencias separadas por saltos de línea
referencias = st.text_area("Introduce la lista de referencias bibliográficas separadas por saltos de línea", "")

# Crear un botón para iniciar el proceso de búsqueda y generación de fichas
if st.button("Buscar y generar fichas"):
  # Crear una lista vacía para almacenar las fichas
  fichas = []

  # Iterar por cada referencia de la lista
  for referencia in referencias.split("\n"):
    # Buscar la referencia y obtener la ficha correspondiente
    ficha = buscar_referencia(referencia)

    # Añadir la ficha a la lista
    fichas.append(ficha)

  # Crear un archivo zip en memoria con las fichas
  zip_buffer = io.BytesIO()
  with zipfile.ZipFile(zip_buffer, "w") as zip_file:
    for i, ficha in enumerate(fichas):
      # Crear un nombre de archivo para cada ficha
      nombre = f"referencia_{i+1}.ris"

      # Escribir la ficha en el archivo zip
      zip_file.writestr(nombre, ficha)

  # Enviar el archivo zip al usuario
  st.write("Aquí tienes el archivo zip con las fichas:")
  st.download_button("Descargar zip", zip_buffer.getvalue(), "referencias.zip")
