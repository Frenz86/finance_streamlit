import pandas as pd
import streamlit as st
import yfinance
import plotly.express as px

@st.cache
def load_data():
    components = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    return components.drop('SEC filings', axis=1).set_index('Symbol')


#st.cache(ignore_hash=True)
def load_quotes(asset):
    return yfinance.download(asset)



def main():
    components = load_data()
    title = st.empty()
    st.sidebar.title("Options")

  
    #st.markdown("""
    #<style>
    #body {
    #    color: #fff;
    #    background-color: #0A3648;
    #}
    #</style>
    #""", unsafe_allow_html=True) #071433   0A3648

    def label(symbol):
        a = components.loc[symbol]
        return symbol + ' - ' + a.Security

    if st.sidebar.checkbox('View companies list'):
        st.dataframe(components[['Security',
                                 'GICS Sector',
                                 'Date first added',
                                 'Founded']])

    st.sidebar.subheader('Select asset')
    asset = st.sidebar.selectbox('Click below to select a new asset',
                                 components.index.sort_values(), index=3,
                                 format_func=label)
    title.title(components.loc[asset].Security)
    if st.sidebar.checkbox('View company info', True):
        st.table(components.loc[asset])
    data0 = load_quotes(asset)
    data = data0.copy().dropna()
    data.index.name = None

    section = st.sidebar.slider('Number of quotes', min_value=30,
                        max_value=min([2000, data.shape[0]]),
                        value=500,  step=10)

    data2 = data[-section:]['Adj Close'].to_frame('Adj Close')

    sma = st.sidebar.checkbox('SMA', True)
    if sma:
        period= st.sidebar.slider('SMA period', min_value=5, max_value=500,
                             value=20,  step=1)
        data[f'SMA {period}'] = data['Adj Close'].rolling(period ).mean()
        data2[f'SMA {period}'] = data[f'SMA {period}'].reindex(data2.index)

    sma2 = st.sidebar.checkbox('SMA2')
    if sma2:
        period2= st.sidebar.slider('SMA2 period', min_value=5, max_value=500,
                             value=100,  step=1)
        data[f'SMA2 {period2}'] = data['Adj Close'].rolling(period2).mean()
        data2[f'SMA2 {period2}'] = data[f'SMA2 {period2}'].reindex(data2.index)

    st.subheader('Chart')
    fig2 = px.line(data2,title = ' ')
    fig2.update_xaxes(
        rangeslider_visible= True,
        rangeselector=dict(
                            buttons = list([
                            dict(count = 3,label = '1y',step='year',stepmode = "backward"),
                            dict(count = 9,label = '3y',step='year',stepmode = "backward"),
                            dict(count = 15,label = '5y',step='year',stepmode = "backward"),
                            dict(step= 'all')
                                ])        
                            )
                    )
    st.plotly_chart(fig2)

    if st.sidebar.checkbox('View statistic', True):
        st.subheader('Stadistic')
        st.table(data2.describe())

    if st.sidebar.checkbox('View quotes', True):
        st.subheader(f'{asset} historical data')
        st.write(data2)

    st.sidebar.title("About")
    st.sidebar.info('This app is a simple example of \n '
                    'using financial data .\n'
                    'It is maintained by Daniele Grotti \n'
                     '@infomanager')


if __name__ == '__main__':
    main()
