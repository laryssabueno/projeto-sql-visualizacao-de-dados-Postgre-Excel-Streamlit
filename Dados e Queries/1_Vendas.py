from pathlib import Path
import streamlit as st
import pandas as pd


st.set_page_config(layout="wide")
st.subheader("📂 Dataframe de Vendas")
#=====================
# Criando um dicionário de Dataframes
#=====================
BASE_DIR = Path(__file__).parent
dfs = pd.read_excel(BASE_DIR/"Data"/"Leads-Vendas.xlsx", sheet_name=None)

#=====================
# Lendo cada aba do Excel
#=====================

df_leads = pd.DataFrame(dfs["Vendas"])
df_local = pd.DataFrame(dfs["Local"])
df_marcas = pd.DataFrame(dfs["Marcas"])
df_lojas = pd.DataFrame(dfs["Lojas"])
df_visitas = pd.DataFrame(dfs["Leads_Semana"])

aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "Vendas",
    "Local",
    "Marcas",
    "Lojas",
    "Leads_Semana"
])

with aba1:
    st.dataframe(df_leads, use_container_width=True)
    st.subheader("Query utilizada")

    query_leads = '''
    WITH leads AS (

    SELECT 
        date_trunc('month', visit_page_date)::date as month_visit,
        count(visit_page_date) as visit_per_month
    FROM sales.funnel
    GROUP BY month_visit
    ORDER BY month_visit
    ),

    payments AS (

    SELECT 
        date_trunc('month', paid_date)::date as month_paid,
        COUNT(A.paid_date) as sales,
        SUM(B.price *(1+ A.discount)) as revenue

    FROM sales.funnel as A

    LEFT JOIN sales.products as B 
        ON A.product_id = B.product_id

    WHERE paid_date IS NOT NULL

    GROUP BY month_paid
    ORDER BY month_paid
    )

    SELECT 
        A.month_visit,
        A.visit_per_month,
        B.sales,
        (B.revenue/1000) as renevue_in_k,
        (B.sales::float/A.visit_per_month::float) as converting,
        (B.revenue/B.sales)/1000 as average_ticket
        
    FROM leads as A
    LEFT JOIN payments as B 
    ON A.month_visit = B.month_paid
    '''

    st.code(query_leads,language="sql")       
    
with aba2:
    st.dataframe(df_local, use_container_width=True)
    st.subheader("Query utilizada")
    query_local = ''' 
    WITH states_distinct AS (

    SELECT DISTINCT state,
        country
    FROM temp_tables.regions
    )

    SELECT 
        C.country,
        B.state,
        count(A.paid_date) as sales

    FROM sales.funnel AS A
    LEFT JOIN sales.customers AS B
    ON A.customer_id = B.customer_id

    LEFT JOIN states_distinct AS C
    ON B.state = C.state

    WHERE paid_date BETWEEN '2021-08-01' AND '2021-08-31' 

    GROUP BY C.country, B.state
    ORDER BY sales DESC

    LIMIT 5

    '''
    st.code(query_local,language="sql")
    
with aba3:
    st.dataframe(df_marcas, use_container_width=True)
    st.subheader("Query utilizada")
    query_marcas = '''
    SELECT 
        B.brand,
        COUNT(A.paid_date) as sales

    FROM sales.funnel AS A
    LEFT JOIN sales.products as B
    ON A.product_id = B.product_id

    WHERE paid_date BETWEEN '2021-08-01' AND '2021-08-31'

    GROUP BY brand
    ORDER BY sales DESC

    '''

    st.code(query_marcas,language="sql")

with aba4:
    st.dataframe(df_lojas, use_container_width=True)
    st.subheader("Query utilizada")
    query_lojas = '''
    SELECT 
        B.store_name,
        COUNT(A.paid_date) as sales

    FROM sales.funnel AS A
    LEFT JOIN sales.stores as B
    ON A.store_id = B.store_id

    WHERE paid_date BETWEEN '2021-08-01' AND '2021-08-31'

    GROUP BY store_name
    ORDER BY sales DESC

    '''
    st.code(query_lojas,language="sql")

with aba5:
    st.dataframe(df_visitas, use_container_width=True)
    st.subheader("Query utilizada")
    query_visitas = '''
    SELECT 
	EXTRACT(DOW FROM visit_page_date) AS day_week,
	TO_CHAR(visit_page_date, 'DAY') AS name_day_week,
	COUNT(visit_page_date) AS visits

    FROM sales.funnel

    WHERE visit_page_date BETWEEN '2021-08-01' AND '2021-08-31'
    GROUP BY day_week, name_day_week
    ORDER BY day_week


    '''

    st.code(query_visitas,language="sql")




