import streamlit_authenticator as stauth
from sqlalchemy import create_engine, engine, text
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import yaml
import streamlit as st
import requests


headers = {'Accept': 'application/json'}

api_url = "http://192.168.4.58:8080/api/v1/customers"
api_url= "http://192.168.4.58:8080/api/v2/articles"
api_url = "http://192.168.4.58:8080/api/v3/transactions_sample"

customer_url = "customers"

# def make_request(main_url, service_url):
#     response = requests.get(f"{main_url}{service_url}", headers = headers)
#     print(f"Response: {r.json()}")
#     response_json = response.json()
#     return response_json

def load_data(response_json):
    try:
        data = pd.json_normalize(response_json,"result")
    except Exception as e:
        print(e)
    return data


# def load_data(main_url, service_URL):
#     response_json = make_request(api_url, customer_url)
#     df = load_json_to_dataframe(response_json)
#     return response_json, df

# response_json, customer_df  = load_data(api_url, customer_url)


response = requests.get("http://192.168.4.58:8080/api/v1/customers")
response_json = response.json()
customer_df =load_data(response_json)



response = requests.get("http://192.168.4.58:8080/api/v2/articles")
response_json = response.json()
articles_df =load_data(response_json)



response = requests.get("http://192.168.4.58:8080/api/v3/transactions_sample")
response_json = response.json()
transactions_sample_df =load_data(response_json)



st.title("H and M DATA UPDATED KPI and KEY METRICS DASHBOARD ")
st.markdown("## Key Metrics")

option1 =st.sidebar.selectbox("which KPI want to see ?",("colour_group_name per product_group", "graphical_appearance_name per garment_group_name"))
st.header(option1)


customer_df['age_range'] = customer_df.age.apply(lambda x: '0-20' if x<=20 else '21-40' if x>20 and x<=40 else '41-60' if x>40 and x<=60 else '61 plus')

col1, col2 = st.columns(2)
articles_df['Total'] = 1
with col1:
    st.markdown("### Number of products per product group name")
    articles_group_name = articles_df.groupby('product_group_name', dropna=False)['Total'].sum().reset_index().sort_values(by='Total')
    fig2 = px.bar(articles_group_name, x='product_group_name', y='Total')
    st.plotly_chart(fig2, use_container_width=True)
    
with col2:
    st.markdown("### Number of products per garment group name")
    garment_group_name = articles_df.groupby('garment_group_name', dropna=False)['Total'].sum().reset_index().sort_values(by='Total')
    fig3 = px.bar(garment_group_name, x="Total", y="garment_group_name", orientation='h')
    st.plotly_chart(fig3, use_container_width=True)
    
if option1 == 'colour_group_name per product_group':
    groupedChane2 = articles_df.groupby("product_group_name")['colour_group_name'].count().reset_index()
    fig = px.pie(groupedChane2, values='colour_group_name', names='product_group_name', title='colour_group_name per product_group')
    st.plotly_chart(fig, use_container_width=True)
    
elif option1 == "graphical_appearance_name per garment_group_name":
    groupedChane2 = articles_df.groupby("graphical_appearance_name")['garment_group_name'].count().reset_index()
    fig = px.pie(groupedChane2, values='garment_group_name', names='graphical_appearance_name', title='graphical_appearance_name per garment_group_name')
    st.plotly_chart(fig, use_container_width=True)
else:
    print("nothong found")

st.write("Club Membership status per age group")
age_filtered_lst = st.sidebar.slider(
    'Select a range of ages',
    0, 100, (20, 80))
st.sidebar.write('Ages range selected:', age_filtered_lst)


num_customers = len(customer_df["customer_id"])
avg_age = np.mean(customer_df["age"])


# create three columns
kpi1, kpi2, kpi3 = st.columns(3)

# fill in those three columns with respective metrics or KPIs
kpi1.metric(
    label="Active Members",
    value=customer_df[customer_df.club_member_status == 'ACTIVE'].shape[0],
)

kpi2.metric(
    label="PRE-CREATE",
    value=customer_df[customer_df.club_member_status == 'PRE-CREATE'].shape[0],
)

kpi3.metric(
    label="LEFT CLUB",
    value=customer_df[customer_df.club_member_status == 'LEFT CLUB'].shape[0],
)

with st.sidebar:
    kpi4, kpi5 = st.columns(2)

    # fill in those three columns with respective metrics or KPIs
    kpi4.metric(
        label="Regularly",
        value=customer_df[customer_df.fashion_news_frequency == 'Regularly'].shape[0],
    )

    kpi5.metric(
        label="Monthly",
        value=customer_df[customer_df.fashion_news_frequency == 'Monthly'].shape[0],
    )

    kpi5,kpi6 =st.columns(2)
    kpi5.metric(
        label = "Number of different customers",
        value = num_customers,
        delta = num_customers,
    )
        
    kpi6.metric(
        label = "Average age",
        value = round(avg_age, 2),
        delta = -10 + avg_age,
    )

st.bar_chart(customer_df.groupby(["age"])["customer_id"].count())

option2 =st.sidebar.selectbox("which KPI want to see ?" ,("price_per_sales_channel",'gebru'))
#st.header(option2)

#st.dataframe(transaction_df)

if option2 == 'price_per_sales_channel':
    groupedChanel = transactions_sample_df.groupby("sales_channel_id")['price'].mean().reset_index()
    fig = px.pie(groupedChanel, values='price', names='sales_channel_id', title='Price per Channel')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("KPI under dev")


grouped_by_age = customer_df.groupby('age_range')['club_member_status'].count().reset_index()
fig1 = px.bar(grouped_by_age, x='age_range', y='club_member_status')
st.plotly_chart(fig1, use_container_width=True)

    

st.dataframe(articles_df)
