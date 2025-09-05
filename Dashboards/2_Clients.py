from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly._subplots import make_subplots

st.set_page_config(layout="wide")
st.subheader("📊 Dashboard de Perfil dos Clientes")

#=====================
# Criando um dicionário de Dataframes
#=====================
REPO_ROOT = Path(__file__).parent.parent
dfs = pd.read_excel(REPO_ROOT/"Data"/"Leads-Perfil.xlsx", sheet_name=None)

#=====================
# Lendo cada aba do Excel
#=====================

df_genero = pd.DataFrame(dfs["Genero"])
df_idade = pd.DataFrame(dfs["Faixa_Etaria"])
df_status_profissional = pd.DataFrame(dfs["Status_Profissional"])
df_salario = pd.DataFrame(dfs["Faixa_Salarial"])
df_class_veiculo = pd.DataFrame(dfs["Classificaçao_Veiculo"])
df_idade_veiculo = pd.DataFrame(dfs["Idade_Veiculo"])
df_marcas_visitas = pd.DataFrame(dfs["Marcas_Visitas"])

#=====================
# Grafico rosca genero
#=====================

fig_genero = go.Figure()
fig_genero.add_trace(go.Pie(
    labels= df_genero["gênero"],
    values= df_genero["leads"],
    hole=.5,
    marker_colors=["rgb(0, 128, 128)","rgb(255, 204, 0)"]
    )
)

fig_genero.update_layout(
    title="Percentual de Gênero",
    height=600,
    font_size=15
)

#=====================
# Grafico faixa etaria
#=====================

fig_idade = go.Figure()
fig_idade.add_trace(go.Bar(
    y= df_idade["faixa etária"],
    x = df_idade["leads (%)"],
    orientation="h",
    text= [f"{valor*100:.2f} %" for valor in df_idade["leads (%)"]],
    textposition="auto",
    marker_color= "rgb(0, 128, 128)"
    )
)

fig_idade.update_layout(
    title="Percentual por Faixa Etária",
    height=600
)
#=====================
# Grafico status profissional
#=====================

fig_status_profissional = go.Figure()
fig_status_profissional.add_trace(go.Bar(
    y= df_status_profissional["status profissional"],
    x = df_status_profissional["leads (%)"],
    orientation="h",
    text= [f"{valor*100:.2f} %" for valor in df_status_profissional["leads (%)"]],
    textposition="auto",
    marker_color= "rgb(0, 128, 128)"
    )
)

fig_status_profissional.update_layout(
    title="Percentual por Status Profissional",
    height=600
)

#=====================
# Grafico faixa salarial
#=====================

fig_salario = go.Figure()
fig_salario.add_trace(go.Bar(
    y= df_salario["faixa salarial"],
    x = df_salario["leads (%)"],
    orientation="h",
    text= [f"{valor*100:.2f} %" for valor in df_salario["leads (%)"]],
    textposition="auto",
    marker_color= "rgb(0, 128, 128)"
    )
)

fig_salario.update_layout(
    title="Percentual por Faixa Salarial",
    height=600
)

#=====================
# Grafico pizza classifaçao carro
#=====================

fig_class_veiculo =go.Figure()
fig_class_veiculo.add_trace(go.Pie(
    labels=df_class_veiculo["classificação do veículo"],
    values=df_class_veiculo["veículos visitados"],
    marker_colors=["rgb(255, 204, 0)", "rgb(0, 128, 128)"],
    pull=[0, 0.2]
))

fig_class_veiculo.update_layout(
    title="Percentual de Classificação do Veículo",
    height=600
)

#=====================
# Grafico idade do veiculo
#=====================

fig_idade_veiculo = go.Figure()
fig_idade_veiculo.add_trace(go.Bar(
    y= df_idade_veiculo["idade do veículo"],
    x = df_idade_veiculo["veículos visitados (%)"],
    orientation="h",
    text= [f"{valor*100:.2f} %" for valor in df_idade_veiculo["veículos visitados (%)"]],
    textposition="outside",
    marker_color= "rgb(0, 128, 128)"
    )
)

fig_idade_veiculo.update_layout(
    title="Percentual por Idade do Veículo",
    height=600
)

#=====================
# Grafico treemap marcas visitadas
#=====================

fig_marcas_visitas = px.treemap(
    df_marcas_visitas,
    path=["brand", "model"],
    values= df_marcas_visitas["visitas"],
)

fig_marcas_visitas.update_traces(
    textinfo= "label+value"
)

fig_marcas_visitas.update_layout(
    title="Visitas por Marcas e Modelos",
    height=600
)

#=====================
# Melhorando Layout abas + containerizacao
#=====================

aba1, aba2, aba3, aba4 = st.tabs([
    "👥 Gênero & Faixa Etaria",
    "💵 Status Profissional & Faixa Salarial",
    "🚘 Classificação & Faixa de Idade do Veículo",
    "🔍 Marcas Mais Visitadas"
])

#=====================
# Aba 1 - Genero e idade
#=====================

with aba1:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_genero, theme="streamlit", use_container_width=True)
    with col2:
        st.plotly_chart(fig_idade, theme="streamlit", use_container_width=True)

#=====================
# Aba 2 - Status e salario
#=====================

with aba2:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_status_profissional, theme="streamlit", use_container_width=True)
    with col2:
        st.plotly_chart(fig_salario, theme="streamlit", use_container_width=True)

#=====================
# Aba 3 - Classificaçao e idade do veiculo
#=====================

with aba3:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_class_veiculo, theme="streamlit", use_container_width=True)
    with col2:
        st.plotly_chart(fig_idade_veiculo, theme="streamlit", use_container_width=True)

#=====================
# Aba 4 - Visitas as marcas
#=====================

with aba4:
    st.plotly_chart(fig_marcas_visitas, theme="streamlit", use_container_width=True)




