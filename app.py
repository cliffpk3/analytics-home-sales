#Imports:
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import geopandas
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

#Options:
pd.set_option('display.float_format', lambda x: '%.2f' % x)
st.set_page_config(layout='wide')
path = 'reworked_data.csv'
geopath = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

@st.cache(allow_output_mutation=True)
def get_data(path):
    df = pd.read_csv(path)
    return df

@st.cache(allow_output_mutation=True)
def get_geodata(geopath):
    geofile = geopandas.read_file(geopath)
    return geofile

def data_filters(df):
    # 1 Data Filters
    st.sidebar.title('General Filters')
    st.sidebar.header('Dataframe Filters')

    # 1.1 Columns
    f_columns = st.sidebar.multiselect('Specify columns', df.columns)
    if f_columns == []:
        f_columns = df.columns

    f_dataframe = st.checkbox('Show source dataframe')
    if f_dataframe:
        st.write(df[f_columns].head())

    return None

def map_filters(df):
    # 2 Map Filters
    st.sidebar.title('Map Filters')

    # 2.1 Bedrooms
    f_bedrooms = st.sidebar.multiselect('Number of Bedrooms',
                                        sorted(df['bedrooms'].unique()))
    if f_bedrooms == []:
        f_bedrooms = list(sorted(df['bedrooms'].unique()))

    # 2.2 Bathrooms
    f_bathrooms = st.sidebar.multiselect('Number of Bathrooms',
                                         sorted(df['bathrooms'].unique()))
    if f_bathrooms == []:
        f_bathrooms = list(sorted(df['bathrooms'].unique()))

    # 2.3 Floors
    f_floors = st.sidebar.multiselect('Number of Floors',
                                      sorted(df['floors'].unique()))
    if f_floors == []:
        f_floors = list(sorted(df['floors'].unique()))

    # 2.4 Waterfront
    f_waterfront = st.sidebar.checkbox('Only waterfront properties')
    if f_waterfront:
        f2_waterfront = [1]
    else:
        f2_waterfront = [0, 1]

    # 2.5 Worth Buying
    f_worthbuying = st.sidebar.checkbox('Only worth-buying properties')
    if f_worthbuying:
        f2_worthbuying = [1]
    else:
        f2_worthbuying = [0, 1]

    # 2.6 Price
    price_min = int(df['price'].min())
    price_max = int(df['price'].max())
    f_price = st.sidebar.slider('Price Range', price_min, price_max, (price_min, price_max), format='$%f')

    houses = df[
        (df['price'] > f_price[0]) & (df['price'] < f_price[1]) &
        (df['bedrooms'].isin(list(set(df['bedrooms']).intersection(f_bedrooms)))) &
        (df['bathrooms'].isin(list(set(df['bathrooms']).intersection(f_bathrooms)))) &
        (df['floors'].isin(list(set(df['floors']).intersection(f_floors)))) &
        (df['waterfront'].isin(list(set(df['waterfront']).intersection(f2_waterfront)))) &
        (df['worth_buying'].isin(list(set(df['worth_buying']).intersection(f2_worthbuying))))
        ][['id', 'date', 'lat', 'long', 'price', 'sqft_living', 'bedrooms', 'bathrooms', 'yr_built', 'zipcode',
           'worth_buying',  'profit_value', 'selling_price']]  # ][['id', 'lat', 'long', 'price']]

    #FOR FASTER TESTING:
    if len(houses) >= 100:
        houses = houses.sample(100, random_state=101)

    return houses

def charts(houses):
    fig = px.scatter(houses, x='price', y='id', height=400, color='worth_buying', color_continuous_scale=['#da0721', '#60cd06'],
                     size='price', size_max=20,
                     title='<b>Worth Buying Properties</b>',
                     hover_name='id', hover_data={'price': ':.1f', 'worth_buying': ':.f', 'profit_value': ':.2f'},
                     labels={'price': 'Price', 'worth_buying': 'Worth Buying', 'profit_value': 'Profit Value'})
    fig.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=25, b=10))
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    houses2 = houses[houses['worth_buying'] == 1]
    fig2 = px.scatter(houses2, x='price', y='id', height=400, size='profit_value', size_max=20,
                      color_discrete_sequence=['#FF5733'],
                      title='<b>Price x Profit</b>',
                      hover_name='id', hover_data={'price': ':.1f', 'profit_value': ':.2f'},
                      labels={'price': 'Price', 'profit_value': 'Profit Value'})
    fig2.update_layout(title_x=0.5, margin=dict(l=10, r=10, t=25, b=10))
    fig2.update_coloraxes(showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

def maps(geofile, houses):
    map_type = ['Price Map', 'Density Map', 'Region Price Map']
    map = st.radio('Map type', map_type, index=1)
    #Price Map
    price_map = px.scatter_mapbox(houses, lat='lat', lon='long', size='price', color_continuous_scale=['green','red'], size_max=10, zoom=10, color='price', hover_name='id')
    price_map.update_layout(mapbox_style='open-street-map', height=800, margin={'r': 0, 't': 0, "l": 0, "b": 0})
    #Density Map
    density_map = folium.Map(location=[houses['lat'].mean(), houses['long'].mean() ], default_zoom_start=15 )
    marker_cluster = MarkerCluster().add_to(density_map)
    popitup = folium.Popup("test", max_width=500, min_width=600, show=True)
    for name, row in houses.iterrows():
       folium.Marker([row['lat'], row['long']],
           popup='<i>${:,.2f}</i>.'
                 '<br><b>Sqft:</b> {};'
                 '<br><b>Bedroom:</b> {};'
                 '<br><b>Bathroom:</b> {:,.0f};'
                 '<br><b>Year Built:</b> {}.'.format(
                 row['price'],
                 row['sqft_living'],
                 row['bedrooms'],
                 row['bathrooms'],
                 row['yr_built']).replace(",",".")).add_to(marker_cluster)
    #Region Price Map
    df2 = houses[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df2.columns = ['ZIP', 'PRICE']
    geofile = geofile[geofile['ZIP'].isin(df2['ZIP'].tolist())]
    region_price_map = folium.Map(location=[df['lat'].mean(), df['long'].mean()], default_zoom_start=15)
    region_price_map.choropleth(data=df2,
                               geo_data=geofile,
                               columns=['ZIP', 'PRICE'],
                               key_on='feature.properties.ZIP',
                               fill_color='YlOrRd',
                               fill_opacity=0.7,
                               line_opacity=0.2,
                               legend_name='AVG PRICE')
    if map == 'Price Map':
        st.plotly_chart(price_map, use_container_width=True)
    elif map == 'Density Map':
        folium_static(density_map)
    else:
        folium_static(region_price_map)

if __name__ == '__main__':
    df = get_data(path)
    geofile = get_geodata(geopath)
    data_filters(df)
    houses = map_filters(df)
    charts(houses)
    maps(geofile, houses)

#st.title('Home Sales Company')
#st.write('A Home Sales é uma imobiliária fictícia que trabalha com a compra e venda de imóveis. '
#         'Buscamos, através da análise de características e dados dos imóveis, alcançar insights que possibilitam  aquisições de imóveis mais vantajosas e seguras.  \n'
#         'O objetivo desse projeto é relatar a análise de um conjunto de dados de imóveis e, por fim, destacar  aqueles que são interessantes para compra.')
#
#st.header('Questões de Negócio:')
#st.write('1) Quais imóveis a Home Sales deve comprar e por qual preço?')
#st.write('Os critérios de compra são:  \na) Imóveis abaixo da mediana de preço daquela região;  \nb) Em boas condições;  \n c) Em que é possível um ganho de pelo menos 10% sobre o valor de compra.')
#st.write('Os imóveis da amostra que cumprem esses requisitos são listados no gráfico abaixo:')
#
#
#st.write('2) Uma vez que o imóvel foi adquirido, qual deve ser seu valor de venda?')
#st.write('Os imóveis da amostra são exibidos no gráfico abaixo, o tamanho do círculo reflete o percentual de lucro em relação ao valor de compra do imóvel no processo aquisição.')
