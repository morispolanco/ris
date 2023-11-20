import streamlit as st
import requests
import zipfile
import base64

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
            # Comprimir las fichas en un archivo ZIP
            zip_filename = "fichas_bibliograficas.zip"
            with zipfile.ZipFile(zip_filename, "w") as zip_file:
                for i, ris in enumerate(ris_list):
                    zip_file.writestr(f"ficha_{i+1}.ris", ris.encode('utf-8'))

            # Abrir el archivo ZIP como bytes
            with open(zip_filename, "rb") as file:
                zip_data = file.read()

            # Descargar el archivo ZIP
            b64_zip = base64.b64encode(zip_data).decode()
            href = f'<a href="data:application/zip;base64,{b64_zip}" download="{zip_filename}">Descargar archivo ZIP</a>'
            st.markdown(href, unsafe_allow_html=True)

            st.success("Se han generado las fichas bibliográficas.")
        else:
            st.warning("No se generaron fichas para ninguna de las referencias ingresadas.")


def generate_ris(item):
    ris = ""

    # Generar la ficha en formato RIS
    ris += f"TY  - {item.get('type', '')}\n"
    ris += f"TI  - {item.get('title', [''])[0]}\n"

    authors = item.get('author', [])
    for author in authors:
        given_name = author.get('given', '')
        family_name = author.get('family', '')
        ris += f"AU  - {family_name}, {given_name}\n"

    date_parts = item.get("issued", {}).get("date-parts", [[]])
    date = date_parts[0][0] if date_parts else ""
    ris += f"PY  - {date}\n"

    if 'journal-issue' in item:
        issue = item['journal-issue']
        if 'title' in issue:
            publication = issue['title'][0]
            ris += f"PB  - {publication}\n"

    # Otros campos opcionales
    volume = item.get('volume', '')
    if volume:
        ris += f"VL  - {volume}\n"

    issue = item.get('issue', '')
    if issue:
        ris += f"IS  - {issue}\n"

    page = item.get('page', '')
    if page:
        ris += f"SP  - {page}\n"

    doi = item.get('DOI', '')
    if doi:
        ris += f"DO  - {doi}\n"

    # Agregar los campos que desees incluir en la ficha RIS

    ris += "ER  -\n\n"
    return ris


if __name__ == "__main__":
    main()
