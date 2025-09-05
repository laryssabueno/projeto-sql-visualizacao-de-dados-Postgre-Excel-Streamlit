from pathlib import Path
import streamlit as st
import pandas as pd


st.set_page_config(layout="wide")
st.subheader("📂 Dataframe de Leads")
st.sidebar.markdown("Desenvolvido por [Laryssa Bueno](https://www.linkedin.com/in/laryssa-bueno-eng/)" )
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

aba1, aba2, aba3, aba4, aba5, aba6, aba7 = st.tabs([
    "Genero",
    "Faixa_Etaria",
    "Status_Profissional",
    "Faixa_Salarial",
    "Classificaçao_Veiculo",
    "Idade_Veiculo",
    "Marcas_Visitas"

])

with aba1:
    st.dataframe(df_genero, use_container_width=True)
    st.subheader("Query utilizada")

    query_genero = '''
    SELECT
        B.gender,
        COUNT(A.customer_id) as leads	
	
    FROM sales.customers AS A

    LEFT JOIN temp_tables.ibge_genders AS B
    ON LOWER(A.first_name) = LOWER(B.first_name)

    GROUP BY gender

    '''

    st.code(query_genero,language="sql")       
    
with aba2:
    st.dataframe(df_idade, use_container_width=True)
    st.subheader("Query utilizada")
    query_idade = ''' 
    SELECT 
        CASE
        WHEN client_age < 20 THEN '0-20'
        WHEN client_age < 40 THEN '20-40'
        WHEN client_age < 60 THEN '40-60'
        WHEN client_age < 80 THEN '60-80'
        ELSE '80+'
        END AS age_range,
        (COUNT(*)::FLOAT)/(SELECT COUNT(*) FROM temp_tables.customers_age) AS leads

    FROM temp_tables.customers_age
    GROUP BY age_range
    ORDER BY age_range
    '''
    st.code(query_idade,language="sql")
    
with aba3:
    st.dataframe(df_status_profissional, use_container_width=True)
    st.subheader("Query utilizada")
    query_status_profissional = '''
    SELECT
        professional_status,
        (COUNT(*)::float)/(SELECT  COUNT(*) FROM sales.customers) AS leads

    FROM sales.customers

    GROUP BY professional_status
    ORDER BY leads ASC
    '''

    st.code(query_status_profissional,language="sql")

with aba4:
    st.dataframe(df_salario, use_container_width=True)
    st.subheader("Query utilizada")
    query_salario = '''
    SELECT 
        CASE
        WHEN income < 5000 THEN '0-5000'
        WHEN income < 10000 THEN '5000-10000'
        WHEN income < 15000 THEN '10000-15000'
        WHEN income < 20000 THEN '15000-20000'
        ELSE '20000+'
        END AS income_range,
        (COUNT(*)::FLOAT)/(SELECT COUNT(*) FROM sales.customers) AS leads,
        CASE
        WHEN income < 5000 THEN 1
        WHEN income < 10000 THEN 2
        WHEN income < 15000 THEN 3
        WHEN income < 20000 THEN 4
        ELSE 5
        END AS order_by

    FROM sales.customers
    GROUP BY income_range, order_by
    ORDER BY order_by
    '''
    st.code(query_salario,language="sql")

with aba5:
    st.dataframe(df_class_veiculo, use_container_width=True)
    st.subheader("Query utilizada")
    query_class_veiculo = '''
    WITH date_convert AS (
    SELECT 
        product_id,
        TO_DATE(model_year, 'YYYY-MM-DD') AS date_model 
    FROM sales.products
    )

    SELECT 
        CASE 
        WHEN datediff('y', A.date_model, CURRENT_DATE) <= 2 THEN 'NEW'
        WHEN datediff('y', A.date_model, CURRENT_DATE) < 5 THEN 'PRE-OWNED'
        ELSE 'USED'
        END AS model_classification,
        COUNT(B.visit_page_date) AS visits_by_classification
        
    FROM date_convert AS A 

    LEFT JOIN sales.funnel AS B
    ON A.product_id = B.product_id

    GROUP BY model_classification
    '''

    st.code(query_class_veiculo,language="sql")

with aba6:
    st.dataframe(df_idade_veiculo, use_container_width=True)
    st.subheader("Query utilizada")
    query_idade_veiculo = '''
   WITH date_convert AS (
    SELECT 
        product_id,
        TO_DATE(model_year, 'YYYY-MM-DD') AS date_model 
    FROM sales.products
    )

    SELECT 
        CASE 
        WHEN datediff('y', A.date_model, CURRENT_DATE) <= 2 THEN '0-2 years'
        WHEN datediff('y', A.date_model, CURRENT_DATE) <= 4 THEN '2-4 years'
        WHEN datediff('y', A.date_model, CURRENT_DATE) <= 6 THEN '4-6 years'
        WHEN datediff('y', A.date_model, CURRENT_DATE) <= 8 THEN '6-8 years'
        WHEN datediff('y', A.date_model, CURRENT_DATE) <= 10 THEN '8-10 years'
        ELSE '10+ years'
        END AS model_age,
        (COUNT(*)::FLOAT)/(SELECT COUNT(visit_page_date) FROM sales.funnel) AS leads_visits,

    CASE 
        WHEN datediff('y', A.date_model, CURRENT_DATE) <= 2 THEN 1
        WHEN datediff('y', A.date_model, CURRENT_DATE) <= 4 THEN 2
        WHEN datediff('y', A.date_model, CURRENT_DATE) <= 6 THEN 3
        WHEN datediff('y', A.date_model, CURRENT_DATE) <= 8 THEN 4
        WHEN datediff('y', A.date_model, CURRENT_DATE) <= 10 THEN 5
        ELSE 6
        END AS order_by
        
    FROM date_convert AS A 

    LEFT JOIN sales.funnel AS B
    ON A.product_id = B.product_id

    GROUP BY model_age, order_by
    ORDER BY order_by

    '''

    st.code(query_idade_veiculo,language="sql")

with aba7:
    st.dataframe(df_marcas_visitas, use_container_width=True)
    st.subheader("Query utilizada")
    query_marcas_visitas = '''
    SELECT
        A.brand,
        A.model,
        COUNT(B.visit_page_date) AS visits
        
    FROM sales.products AS A
    LEFT JOIN sales.funnel AS B
    ON A.product_id = B.product_id

    GROUP BY A.brand, A.model
    ORDER BY brand, model, visits 
    '''

    st.code(query_marcas_visitas,language="sql")






