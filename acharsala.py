import streamlit as st
import pandas as pd
from pathlib import Path
from st_pages import Page, Section, add_page_title, show_pages

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
# Título da aplicação
st.title("Leitura de Dados de uma Planilha Excel")

# Caminho para o arquivo Excel (uma pasta acima)
file_path = 'dados/LISTA PILOTO COMPLETA.xls'

# Nome da planilha que você quer ler
sheet_name = 'LISTA DE ALUNOS ATUALIZADA'
# Linha onde o cabeçalho começa (contagem começando do zero)
# Basicamente preciso fazer um while para ir adicionando as salas da planilha...
# Verifique se o arquivo existe e leia-o
salas = ["FASE 1","FASE 2","1A","1B","1C","1D","2A","2B","2C","3A","3B","3C","4A","4B","4C","5A","5B","5C","5D"]
numero_de_elementos = len(salas)

# Lista de índices que você deseja definir
indices = ['Nome do Aluno', 'Data de Nasc.', 'RA']

# Criando um DataFrame vazio com os índices definidos
combined_df  = pd.DataFrame()

for sala in salas:
    try:
        df_novasala = pd.read_excel(file_path, sheet_name=sala, header=2)
        df_novasala["sala"] = sala
        combined_df = pd.concat([combined_df, df_novasala], ignore_index=True)
    except FileNotFoundError:
        st.error(f"O arquivo {file_path} não foi encontrado. Verifique o caminho e tente novamente.")
    except ValueError as e:
        st.error(f"Ocorreu um erro ao ler a planilha: {e}")
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")
st.dataframe(combined_df)