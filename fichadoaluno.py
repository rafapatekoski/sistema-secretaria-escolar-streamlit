import streamlit as st
from time import sleep
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import io
from docxtpl import DocxTemplate
from pathlib import Path
from datetime import datetime
#import locale
#TESTAR SE JA SELECIONARAM O ALUNO
if "sheet" not in st.session_state:
    switch_page("Lista Piloto")
pasta_documentos = Path(__file__).parent.parent / 'documentos'
template_path = pasta_documentos / 'declaracaotransferencia.docx'
template_pathfrequencia = pasta_documentos / 'declaracaodefrequencia.docx'
listapiloto = 'dados/LISTA PILOTO COMPLETA.xls'
# Obtendo o índice do primeiro registro da Series
indice_primeiro_registro = st.session_state["fichadoaluno"].index[0]

# Escrevendo o índice do primeiro registro
st.write("O índice do primeiro registro de st.session_state['fichadoaluno'] é:", indice_primeiro_registro)
# Verifique se o arquivo existe e leia-o
try:
    df = pd.read_excel(listapiloto, sheet_name=st.session_state["sheet"], header=2)
    
    def doc_file_creation(template_path, data):
        doc = DocxTemplate(template_path)
        doc.render(data)
        return doc
    def doc_file_creationfrequencia(template_pathfrequencia, data):
        doc = DocxTemplate(template_pathfrequencia)
        doc.render(data)
        return doc
    infoAluno = df.iloc[st.session_state["fichadoaluno"].index[0]].to_dict()
    template_path = "documentos/declaracaotransferencia.docx"
    template_pathfrequencia = "documentos/declaracaodefrequencia.docx"
        # Data for rendering the template


    # Configurar o idioma local para português do Brasil
    #locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    nascimento = infoAluno["Data de Nasc."].strftime('%d/%m/%Y')
    # Obter a data de hoje
    data_atual = datetime.today()

    # Formatar a data como "6 de Junho de 2024"
    data_formatada = data_atual.strftime("%d de %B de %Y")


    numero = infoAluno["RA"]
    ra = str(numero).rstrip('0').rstrip('.') if '.' in str(numero) else str(numero) 
    serie = st.session_state["sheet"]
    if serie[0] == "1":
        serie = "1° Ano"
    elif serie[0] == "2":
        serie = "2° Ano"
    elif serie[0] == "3":
        serie = "3° Ano"
    elif serie[0] == "4":
        serie = "4° Ano"
    elif serie[0] == "5":
        serie = "5° Ano"
    else:
        pass
    chaves = ["nome", "nascimento", "ra","serie","data"]
    valores = [infoAluno["Nome do Aluno"],nascimento,ra,serie,data_formatada]
    context = dict(zip(chaves, valores))

        # Create and render the Word document
    doc_download = doc_file_creation(template_path, context)
    doc_downloadfrequencia = doc_file_creationfrequencia(template_pathfrequencia, context)
        # Save the document to BytesIO
    bio = io.BytesIO()
    bio2 = io.BytesIO()
    doc_download.save(bio)
    doc_downloadfrequencia.save(bio2)

        # Display the download button
    if doc_download:
        st.download_button(
                label="Declaração de transferencia",
                data=bio.getvalue(),
                file_name=(f"{context['nome']}_saida.docx"),
                mime="docx"
            )
    if doc_downloadfrequencia:
        st.download_button(
                label="Declaração de frequencia",
                data=bio2.getvalue(),
                file_name=(f"{context['nome']}_frequencia.docx"),
                mime="docx"
            )
    st.write(infoAluno["Nome do Aluno"])
    st.write("Sala: ", st.session_state["sheet"])
except FileNotFoundError:
    st.error(f"O arquivo aqruivo não foi encontrado. Verifique o caminho e tente novamente.")
except ValueError as e:
    st.error(f"Ocorreu um erro ao ler a planilha: {e}")
except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")

def doc_file_creation(template_path, data):
    doc = DocxTemplate(template_path)
    doc.render(data)
    return doc