import streamlit as st

def home():
    st.write("# Projeto SQL para Análise de Dados: do básico ao avançado! 💻")
    st.sidebar.markdown("Desenvolvido por [Laryssa Bueno](https://www.linkedin.com/in/laryssa-bueno-eng/)" )

    btn_1, btn_2, btn_3 = st.columns(3, vertical_alignment="center")

    btn_1.link_button("Curso na Udemy", "https://www.udemy.com/course/sql-para-analise-de-dados/", icon="🛒", use_container_width=True)
    btn_2.link_button("Me encontre no GitHub", "https://github.com/laryssabueno", icon="💡", use_container_width=True)
    btn_3.link_button("Me encontre no Linkedin", "https://www.linkedin.com/in/laryssa-bueno-eng/" ,icon="📥", use_container_width=True)

    st.markdown("""

Curso desenvolvido e lecionado por [Midori Toyota](https://www.linkedin.com/in/midoritoyota/).

SGBD utilizado foi:![PostgreSQL](https://img.shields.io/badge/PostgreSQL-000?style=for-the-badge&logo=postgresql)

Nesse curso foi ministrado os seguintes tópicos:

- Sintaxe básica do SQL
- Filtragem de dados com  WHERE
- Análise de dados agregados com GROUP BY
- Relacionamento entre tabelas utilizando JOIN
- Queries avançadas com o uso de Subqueries
- Limpeza e tratamento de dados
- Como criar e manipular tabelas
- Como aplicar o SQL na análise de dados de negócio
e muito mais! 
                
Ao final foram desenvolvidas consultas SQL e uso de Excel como fonte de dados para os dashboards e dataframes.""" )

home_page = st.Page(home, title="Home", icon="🏡")
dash_sales = st.Page("Dashboards/1_Leads.py", title = "Vendas", icon= "💰")
dash_leads = st.Page("Dashboards/2_Clients.py", title = "Perfil Leads", icon= "👤")
query_vendas = st.Page("Dados e Queries/1_Vendas.py", title = "Dataframe e Queries Vendas", icon= "📓")
query_clientes = st.Page("Dados e Queries/2_Clientes.py", title = "Dataframe e Queries Leads", icon= "🗄")

pg = st.navigation(
    {
        "Navegação": [home_page],
        "Dashboards": [dash_sales, dash_leads],
        "Dados e Querys": [query_vendas, query_clientes]
    }
)


pg.run()


