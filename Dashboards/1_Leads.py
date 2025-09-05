import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly._subplots import make_subplots

st.set_page_config(layout="wide")
st.subheader("📊 Dashboard de Vendas")

#=====================
# Criando um dicionário de Dataframes
#=====================

dfs = pd.read_excel("projeto-sql-visualizacao-de-dados-Postgre-Excel-Streamlit/Leads-Vendas.xlsx", sheet_name=None)

#=====================
# Lendo cada aba do Excel
#=====================

df_local = pd.DataFrame(dfs["Local"])

# Adicionando Latitude e Longitude para mapa geografico
df_local["Latitude"] = [-23.5505, -19.9167, -27.5954, -30.0346, -22.9068]
df_local["Longitude"] = [-46.6333, -43.9345, -48.5480, -51.2177, -43.1729]

df_leads = pd.DataFrame(dfs["Vendas"])
df_marcas = pd.DataFrame(dfs["Marcas"])
df_lojas = pd.DataFrame(dfs["Lojas"])
df_visitas = pd.DataFrame(dfs["Leads_Semana"])


#=====================
# Grafico receita e ticket medio
#=====================

fig_receita = go.Figure()
fig_receita = make_subplots(specs=[[{"secondary_y": True}]])

fig_receita.add_trace(go.Bar(
    y = df_leads["Receita (k, R$)"],
    x = df_leads["Mês"],
    text=[f"{valor:.2f}" for valor in df_leads["Receita (k, R$)"]],
    textposition="outside",
    textangle=0,
    marker_color= "rgb(0, 128, 128)",
    name = "Receita (k, R$)"
),
secondary_y =False,
)

fig_receita.add_trace(go.Scatter(
    y = df_leads["Ticket médio (k, R$)"],
    x = df_leads["Mês"],
    text= [f"{valor:.2f}" for valor in df_leads["Ticket médio (k, R$)"]],
    textposition = "top center",
    textfont=dict(size=9),
    name="Ticket médio (k, R$)",
    mode ="lines+markers+text",
    line_color = "rgb(255, 204, 0)" 
),
secondary_y=True,
)

fig_receita.update_xaxes(tickangle=-45, tickvals=df_leads["Mês"], tickformat="%b-%Y")
fig_receita.update_yaxes(range=[0, 100], secondary_y=True)
fig_receita.update_yaxes(range=[0, 80000], secondary_y=False)

fig_receita.update_layout(
    title= "Receita e Ticket Médio por Mês",
    height=600
)


#=====================
# Grafico Leads
#=====================

fig_leads = go.Figure()
fig_leads = make_subplots(specs=[[{"secondary_y": True}]])

fig_leads.add_trace(go.Bar(
    y = df_leads["Leads"],
    x = df_leads["Mês"],
    text=df_leads["Leads"],
    textposition="auto",
    textangle=0,
    marker_color= "rgb(0, 128, 128)",
    name = "Leads"
),
secondary_y =False,
)

fig_leads.add_trace(go.Scatter(
    y = df_leads["Conversão (%)"],
    x = df_leads["Mês"],
    text= [f"{valor*100:.2f}" for valor in df_leads["Conversão (%)"]],
    textposition = "top left",
    textfont=dict(size=9),
    name="Conversão (%)",
    mode ="lines+markers+text",
    line_color = "rgb(255, 204, 0)" 
),
secondary_y=True,
)

fig_leads.update_xaxes(tickangle=-45, tickvals=df_leads["Mês"], tickformat="%b-%Y")
fig_leads.update_yaxes(range=[0, 0.21], secondary_y=True)
fig_leads.update_yaxes(range=[0, 7000], secondary_y=False)

fig_leads.update_layout(
    title= "Leads e Conversão por Mês",
    height=600
)

#=====================
# Grafico vendas por estado
#=====================

fig_local = go.Figure()

fig_local.add_trace(go.Scattergeo(
    lat=df_local["Latitude"],
    lon=df_local["Longitude"],
    text=df_local["Estado"] + "<br>Vendas: " + df_local["Vendas"].astype(str),
    marker= dict(
        size=df_local["Vendas"],
        color=df_local["Vendas"],
        colorscale = "YlOrRd",
        colorbar = dict(title="Nº de Vendas"),
        line_color='black',
        line_width=0.5,
        sizemode = "area",
        opacity = 0.8
    ),
    mode = "markers"
    )
)


fig_local.update_layout(
    title= "Vendas do Mês por Estado (BR)",
    height=600,
    geo = go.layout.Geo(
    scope="south america",
    showland=True,
    landcolor="rgb(229, 229, 229)",
    showcountries=False,
    showframe=False,
    projection_type="mercator",
    center=dict(lat=-15.8, lon=-47.9),  # centro aproximado do Brasil
    )
)


#=====================
# Grafico de marcas
#=====================

fig_marcas = go.Figure()

fig_marcas.add_trace(go.Bar(
    y = df_marcas["Marca"],
    x = df_marcas["Vendas"],
    orientation= 'h',
    text=df_marcas["Vendas"],
    textposition="auto",
    marker_color= "rgb(0, 128, 128)"
    )
)
fig_marcas.update_layout(
        title="Top 5 marcas mais vendidas",
        height=600
)


#=====================
# Grafico de lojas
#=====================

fig_lojas = go.Figure()

fig_lojas .add_trace(go.Bar(
    y = df_lojas["Loja"],
    x = df_lojas["Vendas"],
    orientation= 'h',
    text=df_lojas["Vendas"],
    textposition="auto",
    marker_color= "rgb(0, 128, 128)"
    )
)
fig_lojas.update_layout(
        title="Top 5 lojas que mais venderam",
        height=600       
)


#=====================
# Grafico de visitas
#=====================

fig_visitas = go.Figure()

fig_visitas.add_trace(go.Bar(
    y = df_visitas["Visitas"],
    x = df_visitas["Dia da semana"],
    text=df_visitas["Visitas"],
    textposition="outside",
    marker_color= "rgb(0, 128, 128)"
))

fig_visitas.update_layout(
    title="Visitas por Dias da Semana",
    height=600
)



#=====================
# Melhorando Layout abas + containerizacao
#=====================
aba1, aba2, aba3, aba4 = st.tabs([
    "📈 Vendas & Leads",
    "🌍 Performance Geográfica",
    "🏪 Marcas & Lojas",
    "👥 Visitas"
])

#=====================
# Aba 1 - Vendas e Leads
#=====================

with aba1:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_receita, theme="streamlit", use_container_width=True, key="receita")
    with col2:
        st.plotly_chart(fig_leads, theme="streamlit", use_container_width=True, key="leads")
    
#=====================

# Aba 2 - Mapa
#=====================

with aba2:
    st.plotly_chart(fig_local, theme="streamlit", use_container_width=True, key="mapa")
    st.write("**Dados referentes ao mês de Agosto de 2021.")
#=====================

# Aba 3 - Marcas e Lojas
#=====================

with aba3:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_marcas, theme="streamlit", use_container_width=True, key="marcas")
    with col2:
        st.plotly_chart(fig_lojas, theme="streamlit", use_container_width=True, key="lojas")
    
    st.write("**Dados referentes ao mês de Agosto de 2021.")
#=====================

# Aba 4 - Visitas
#=====================

with aba4:
    st.plotly_chart(fig_visitas, theme="streamlit", use_container_width=True, key="visitas")
    st.write("**Dados referentes ao mês de Agosto de 2021.")


