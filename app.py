import streamlit as st
import pandas as pd
from pathlib import Path
from st_pages import Page, Section, add_page_title, show_pages

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
show_pages([
    Page("app.py", "Home"),
    Page("acharsala.py", "Achar Sala"),
    Page("listapiloto.py","Lista Piloto"),
    Page("fichadoaluno.py","Ficha do Aluno"),
])
# Título da aplicação
st.title("Sistema Secretaria Escolar")
