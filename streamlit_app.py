import streamlit as st
import json
import logging
from zipimport import zipimporter
from zipfile import ZIP_DEFLATED

# Función para processar los datos bibliográficos
def process_data(data):
    text = data.lower()
    return text

# Función para generar los archivos .ris
def generate_ris_files(data):
    text = data.lower()
    with open("example.ris", "w") as file:
        file.write(text)
    return text

# Función para comprimir los archivos .ris en un archivo ZIP
def compress_files(data):
    text = data.lower()
    with zipfile.ZipFile("example.zip", "w") as zip_file:
        zip_file.write("example.ris", arcpath="")
    return text

# Función para descargar los archivos .ris y el archivo ZIP
def download_files():
    data = process_data(st.text_input("Ingrese un texto: "))
    generated_files = generate_ris_files(data)
    compressed_files = compress_files(data)
    return generated_files, compressed_files

# Crear la aplicación de Streamlit
st.title("Aplicación de Streamlit para generar archivos .ris y comprimirlos en un archivo ZIP")
st.write("Ingrese un texto: ", None)
button = st.button("Descargar")

@button.click
def download_files():
    data = process_data(st.text_input("Ingrese un texto: "))
    generated_files = generate_ris_files(data)
    compressed_files = compress_files(data)
    return generated_files, compressed_files

st.button("Descargar", download_files)
