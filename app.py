import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup Analysis')
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

def load_investor_details(investor):
    st.title(investor)
    # load recent 5 investments
    st.subheader('Most recent investments')
    st.dataframe(df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']])

    #biggest investments
    col1, col2 = st.columns(2)
    with col1:
        big_investments = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest investments')
        fig, ax = plt.subplots()
        ax.bar(big_investments.index, big_investments.values)
        st.pyplot(fig)

    # investment by sectors
    with col2:
        sectors_invested = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(sectors_invested, labels=sectors_invested.index, autopct='%0.01f%%')
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    # investment by rounds
    with col3:
        rounds = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Investment rounds')
        fig2, ax2 = plt.subplots()
        ax2.pie(rounds, labels=rounds.index, autopct='%0.01f%%')
        st.pyplot(fig2)

    # investment by cities
    with col4:
        cities = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Investment by cities')
        fig3, ax3 = plt.subplots()
        ax3.pie(cities, labels=cities.index, autopct='%0.01f%%')
        st.pyplot(fig3)

    col5, col6 = st.columns(2)
    # YoY investment
    with col5:
        YoY = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('YoY investment')
        fig4, ax4 = plt.subplots()
        ax4.plot(YoY.index, YoY.values)
        st.pyplot(fig4)


def load_overall_analysis():
    st.title('Overall Analysis')
    col1, col2, col3, col4 = st.columns(4)
    # total investment
    total_investment = round(df['amount'].sum())
    # max funding
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # average funding
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    total_startups = df['startup'].nunique()
    with col1:
        st.metric('Total', '{} Cr'.format(total_investment))
    with col2:
        st.metric('Max funding', '{} Cr'.format(max_funding))
    with col3:
        st.metric('Average funding', '{} Cr'.format(round(avg_funding)))
    with col4:
        st.metric('Total funded startups', '{}'.format(total_startups))

    # top sectors
    col5, col6 = st.columns(2)
    with col5:
        st.subheader('Top 5 sectors')
        top5_sectors = df['vertical'].value_counts().head()
        fig1, ax1 = plt.subplots()
        ax1.bar(top5_sectors.index, top5_sectors.values)
        st.pyplot(fig1)
    with col6:
        st.subheader('Amount invested')
        amount_invested = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(5)
        fig2, ax2 = plt.subplots()
        ax2.bar(amount_invested.index, amount_invested.values)
        st.pyplot(fig2)

    # MoM investment
    st.header('Month on Month investment')
    selected_option = st.selectbox('Select type', ['Amount', 'Startups'])
    if selected_option == 'Amount':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig3)


st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select one', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Startup':
    st.sidebar.selectbox('Select startup', sorted(df['startup'].unique().tolist()))
    start_up_button = st.sidebar.button('Analyze')
else:
    selected_investor = st.sidebar.selectbox('Select investor', sorted(set(df['investors'].str.split(',').sum())))
    investor_button = st.sidebar.button('Analyze')
    if investor_button:
        load_investor_details(selected_investor)
