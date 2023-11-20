import streamlit as st
import requests
import zipfile

def main():
    st.title("Generador de fichas bibliográficas")

    # Entrada de referencias bibliográficas
    references = st.text_area("Ingrese las referencias bibliográficas (una por línea)")

    if st.button("Generar fichas"):
        # Separar las referencias en líneas
        reference_list = references.strip().split('\n')

        # Lista para almacenar las fichas
        ris_list = []

        st.write("Procesando...")
        for reference in reference_list:
            # Buscar la entrada en Internet utilizando la API Crossref
            response = requests.get(f"https://api.crossref.org/works?query={reference}")

            if response.status_code == 200:
                data = response.json()

                if data["message"]["items"]:
                    item = data["message"]["items"][0]

                    # Generar la ficha en formato RIS
                    ris = generate_ris(item)

                    # Agregar la ficha a la lista
                    ris_list.append(ris)
                else:
                    st.warning(f"No se encontró información para la referencia: {reference}")
            else:
                st.error(f"Error en la solicitud para la referencia: {reference}")

        if ris_list:
            # Comprimir las fichas en un archivo zip
            zip_filename = "fichas_bibliograficas.zip"
            with zipfile.ZipFile(zip_filename, "w") as zip_file:
                for i, ris in enumerate(ris_list):
                    zip_file.writestr(f"ficha_{i+1}.ris", ris)

            st.success(f"Se han generado las fichas y se han comprimido en el archivo {zip_filename}")
        else:
            st.warning("No se generaron fichas para ninguna de las referencias ingresadas.")

def generate_ris(item):
    # Obtener los campos de la entrada
    title = item.get("title", [""])[0]
    authors = item.get("author", [])
    date = item.get("published-print", item.get("published-online", ""))

    # Generar la ficha en formato RIS
    ris = f"TY  - JOUR\nTI  - {title}\n"
    ris += "AU  - " + "\nAU  - ".join(authors) + "\n"
    ris += f"PY  - {date.get('date-parts', [''])[0][0]}\nER  -\n\n"
    return ris

if __name__ == "__main__":
    main()
