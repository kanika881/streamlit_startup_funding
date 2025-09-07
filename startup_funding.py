import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
st.set_page_config(layout="wide",page_title="startup_analysis")

def investor_analysis(investor):
    st.title(investor)
    # showing recent 5 investment 
    st.subheader("recent investment")
    df_dataframe=df[df["investors"].str.contains(investor)][["date","startup","vertical","round","amount"]].head()
    st.dataframe(df_dataframe)
    # shwoing the biggest investment 
    col1,col2=st.columns(2)
    with col1:
        st.subheader("biggest investment")
        df_series=df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        fig,ax=plt.subplots()
        ax.bar(df_series.index,df_series.values)
        st.pyplot(fig)
    # st.dataframe(df_series)
    # how much money he invested in each vertical
    with col2:
        st.subheader("sectors invested in:")
        df_series_vertical=df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()
        fig1,ax1=plt.subplots()
        ax1.pie(df_series_vertical,labels=df_series_vertical.index,autopct="%0.01f%%")
        st.pyplot(fig1)
    # how much money invested in each round
    col3,col4=st.columns(2)
    with col3:
        st.subheader("rounds invested in")
        round_invest=df[df["investors"].str.contains(investor)].groupby("round")["amount"].sum()
        fig2,ax2=plt.subplots()
        ax2.pie(round_invest,labels=round_invest.index,autopct="%0.01f%%")
        st.pyplot(fig2)
        
    # cities in which they invested 
    with col4:
        st.subheader("cities  invested in")
        city_invest=df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum()
        fig3,ax3=plt.subplots()
        ax3.pie(city_invest,labels=city_invest.index,autopct="%0.01f%%")
        st.pyplot(fig3)
    # year on year investment graph 
    col5,col6=st.columns(2)
    
    with col5:
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
        df["year"]=df["date"].dt.year
        st.subheader("year on year")
        df_yoy=df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
        fig4,ax4=plt.subplots()
        ax4.plot(df_yoy.index,df_yoy.values)
        st.pyplot(fig4)
def overall_analysis():
    total_money=round(df["amount"].sum())
    total_sector=df.groupby(["vertical"])["vertical"].value_counts().sort_values(ascending=False).head(10)
    money_in_sectors=df.groupby("vertical")["amount"].sum().sort_values(ascending=False).head(10)
    # st.subheader("Total Money Invested in Indian Startup")
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("total",total_money,"Cr")
    max_funding=int(df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0])
    with col2:
        st.metric("max_funding",max_funding,"Cr")
    avg_funding=int(df.groupby("startup")["amount"].sum().mean())
    with col3:
        st.metric("avg_funding",avg_funding,"Cr")
    with col4:
        st.metric("funded startup",df["startup"].nunique())
    col5,col6=st.columns(2)
    with col5:
        fig5,ax5=plt.subplots()
        st.subheader("top sectors")
        ax5.pie(total_sector,labels=total_sector.index,autopct="%0.01f%%")
        st.pyplot(fig5)
    # money invested in each sector 
    with col6:
        fig6,ax6=plt.subplots()
        st.subheader("money ratio in each sector:")
        ax6.pie(money_in_sectors,labels=money_in_sectors.index,autopct="%0.01f%%")
        st.pyplot(fig6)
    col7,col8=st.columns(2)
    with col7:
        funding_type=df.groupby("round")["round"].nunique().index
        st.subheader("Types of Funding")
        st.dataframe(funding_type)
    with col8:
        city_wise_fund=df.groupby(["city","round"])["round"].nunique()
        st.subheader("city wise funding")
        st.dataframe(city_wise_fund)
        
    st.subheader("top startup yearwise")
    # st.
def startup_analysis(startup_name,funding_round):
    st.title(startup_name)
    
    col10,col11,col12=st.columns(3)
    with col10:
        st.subheader("industry")
        industry_name=df[df["startup"]==startup_name]["vertical"].values[0]   
        st.write(industry_name)
    with col11:
        st.subheader("subindustry")
        subindustry_name=df[df["startup"]==startup_name]["subvertical"].values[0]
        st.write(subindustry_name)
    with col12:
        st.subheader("location")
        location=df[df["startup"]==startup_name]["city"].values[0]
        st.write(location)
    st.subheader("Fudning round")
    st.write(df[df["startup"]==startup_name][["round","amount"]])
    st.subheader("similar companies")
    data_similar_startup=df.groupby(["round","startup"])["amount"].sum().reset_index()
    similar_co=data_similar_startup[data_similar_startup["round"]==funding_round]["startup"].values
    st.write(similar_co)
    

df =pd.read_csv("startup_cleaned.csv")
# df["Investors Name"]=df["Investors Name"].fillna("undisclosed")
st.sidebar.title("Startup Funding Analysis")
options=st.sidebar.selectbox("select one",["overall analysis","Startup","Investor"])
if options=="overall analysis":
    st.title("Overall analysis")
    btn0=st.sidebar.button("show overall analysis")
    if btn0:
        overall_analysis()
        
    
elif options=="Startup":
    selected_startup=st.sidebar.selectbox("select one",sorted(df["startup"].unique().tolist()))
    
    btn1=st.sidebar.button("startup analysis")
    round_selected_startup=df[df["startup"]==selected_startup]["round"]
    if btn1:
        startup_analysis(selected_startup,round_selected_startup)
else:
    selcted_investor=st.sidebar.selectbox("select one",sorted(set(df["investors"].str.split(",").sum())))
    # st.title("investor analysis")
    btn2=st.sidebar.button("find investor analysis")
    if btn2:
        investor_analysis(selcted_investor)
