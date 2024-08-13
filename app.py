import pandas as pd
import plotly.express as px
import streamlit as st

sp=StreamlitPatcher()
#uploading and cleaning data
df=pd.read_excel('C:\\Users\\dell\\Downloads\\excel dash board and power query//Sales-Dashboard-practice-file (version 1).xlsb','Input Data')
df2=df.rename(columns = {'PAYMENT MODE':'PAYMENT_MODE'})
df1=df2.rename(columns = {'SALE TYPE':'SALE_TYPE'})
df=df1.copy()
df['Profit']=df['sum of total selling price']-df['sum of total buying price']

st.set_page_config(page_title='Sales Dashbard',
                   page_icon=':bar chart:',
                   layout='wide'
)
#adding filter here
st.sidebar.header('please filter here')
Months=st.sidebar.multiselect(
    'Select the months',
    options=df['months'].unique(),
    default=df['months'].unique()
)
sALE_TYPE=st.sidebar.multiselect(
    'Select the sALE_TYPE',
    options=df['SALE_TYPE'].unique(),
    default=df['SALE_TYPE'].unique()
)
pAYMENT_MODE=st.sidebar.multiselect(
    'Select the PAYMENT_MODE',
    options=df['PAYMENT_MODE'].unique(),
    default=df['PAYMENT_MODE'].unique()
)
YEAR=st.sidebar.multiselect(
    'Select the year',
    options=df['year'].unique(),
    default=df['year'].unique()
)

df_selection=df.query(
    "months==@Months & SALE_TYPE==@sALE_TYPE & PAYMENT_MODE== @pAYMENT_MODE & year==@YEAR"
)
st.title('dynamic Sales Dashboard')
st.markdown('##')
#updating KPI
total_quanitiy=int(df_selection['QUANTITY'].sum())
total_SELLINGPRICE=int(df_selection['sum of total selling price'].sum())
total_profit=int(df_selection['Profit'].sum())
left_column,middle_column,right_column=st.columns(3)
with left_column:
    st.subheader('total sales')
    st.subheader(f"US $ {total_SELLINGPRICE:,}"
)
with right_column:
    st.subheader('total quanitity')
    st.subheader(f" {total_quanitiy:,}"
)
with middle_column:
    st.subheader('total profit')
    st.subheader(f"US ${total_profit:,}"
)
st.markdown("""---""")
#exploratory data anlusis using diffrent chart
#sales_by_category_line
sales_by_category_line = (
    df_selection.groupby(by=["Category"]).sum()[["sum of total selling price"]].sort_values(by="sum of total selling price")
)
fig_CATEGORY_sales = px.bar(
    sales_by_category_line,
    x="sum of total selling price",
    y=sales_by_category_line.index,
    orientation="h",
    title="<b>Sales by category Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_category_line),
    template="plotly_white",
)
fig_CATEGORY_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#sales_by_day
sales_by_day = df_selection.groupby(by=["day"]).sum()[["sum of total selling price"]]
fig_daily_sales = px.line(
    sales_by_day,
    x=sales_by_day.index,
    y="sum of total selling price",
    title="<b>Sales by day</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_day),
    template="plotly_white",
)
fig_daily_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)
#sales_by_month 
sales_by_month = df_selection.groupby(by=["months"]).sum()[["Profit"]].sort_values(by="months")
fig_monthly_profit = px.bar(
    sales_by_month,
    x=sales_by_month.index,
    y="Profit",
    title="<b>Sales by month</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_month),
    template="plotly_white",
)
fig_monthly_profit.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)
#sales_by_paymnet_mode
sales_by_paymnet_mode = df_selection.groupby(by=["PAYMENT_MODE"]).sum()[["Profit"]]
fig_PAYMENT_MODE = px.pie(
    sales_by_paymnet_mode,
    values='Profit',
    names=sales_by_paymnet_mode.index,
    title="<bsales_by_paymnet_mode</b>",
    template="plotly_white",
)
sales_by_sales_type = df_selection.groupby(by=["SALE_TYPE"]).sum()[["Profit"]]
fig_SALE_TYPE = px.pie(
    sales_by_sales_type,
    values='Profit',
    names=sales_by_sales_type.index,
    title="<b>sales_by_sales_typ</b>",
    template="plotly_white",
)
#updating above all chart in specific location
left_column,middle_column, right_column = st.columns(3)
left_column.plotly_chart(fig_CATEGORY_sales, use_container_width=True)
middle_column.plotly_chart(fig_monthly_profit, use_container_width=True)
right_column.plotly_chart(fig_PAYMENT_MODE, use_container_width=True)

middle_column,right_column = st.columns(2)
middle_column.plotly_chart(fig_daily_sales, use_container_width=True)
right_column.plotly_chart(fig_SALE_TYPE, use_container_width=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
