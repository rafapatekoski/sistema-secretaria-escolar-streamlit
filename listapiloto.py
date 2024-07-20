import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, Section, add_page_title, show_pages
import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
import random
from time import sleep
import pandas as pd
from st_pages import Page, Section, add_page_title, show_pages
from streamlit_extras.switch_page_button import switch_page
from time import sleep
import io
from docxtpl import DocxTemplate
from pathlib import Path
from datetime import datetime
# Caminho para o arquivo Excel (uma pasta acima)
file_path = 'dados/LISTA PILOTO COMPLETA.xls'
def doc_file_creation(template_path, data):
    doc = DocxTemplate(template_path)
    doc.render(data)
    return doc

def funcaozinha():
    dataframe = st.session_state["data"]["edited_rows"]
    dataframe = pd.DataFrame(dataframe)
    ultimo_registro = dataframe.iloc[-1]
    st.write("Primeiro registro da coluna 'edited_rows':", ultimo_registro)
    st.write(st.session_state["sheet"])
    st.session_state["fichadoaluno"] = ultimo_registro
# Título da aplicação
st.title("Leitura de Dados de uma Planilha Excel")
if "fichadoaluno" not in st.session_state:
    print('0s')
else:
    switch_page("Ficha do Aluno")
# Caminho para o arquivo Excel (uma pasta acima)
file_path = 'dados/LISTA PILOTO COMPLETA.xls'

# Nome da planilha que você quer ler
sheet_name = 'FASE 1'
st.session_state["sheet"] = sheet_name
salas = ["FASE 1","FASE 2","1A","1B","1C","1D","2A","2B","2C","3A","3B","3C","4A","4B","4C","5A","5B","5C","5D"]
numero_de_elementos = len(salas)
valor_filtro = st.selectbox('Filtrar por sala:', salas)
col1, col2 = st.columns(2)
status_filtrar = col1.button('Filtrar')
status_limpar = col2.button('Limpar')
if status_filtrar:
    sheet_name = valor_filtro
    st.session_state["sheet"] = sheet_name
elif status_limpar:
    st.session_state["sheet"] = sheet_name
    sheet_name = 'FASE 1'
# Linha onde o cabeçalho começa (contagem começando do zero)
header_row = 2  # Linha 3 do Excel é a linha 2 no pandas (0-indexed)

# Verifique se o arquivo existe e leia-o
try:
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
    # Exibir os dados da planilha
    st.write(f"Dados da planilha '{sheet_name}':")
    df["select"] = False
    # Reordenar as colunas para que 'select' seja a primeira
    cols = ['select'] + [col for col in df.columns if col != 'select']
    df = df[cols]
    st.data_editor(df,on_change=funcaozinha,key='data')
    
    # Exibir algumas estatísticas básicas
    st.write("Estatísticas Descritivas:")
    st.write(df.describe())
except FileNotFoundError:
    st.error(f"O arquivo {file_path} não foi encontrado. Verifique o caminho e tente novamente.")
except ValueError as e:
    st.error(f"Ocorreu um erro ao ler a planilha: {e}")
except Exception as e:
    st.error(f"Ocorreu um erro inesperado: {e}")