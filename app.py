#Imports:
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import geopandas
from millify import millify
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

#Options:
pd.set_option('display.float_format', lambda x: '%.2f' % x)
st.set_page_config(layout='wide')
path = 'reworked_kc_house_data.csv'
geopath = 'https://opendata.arcgis.com/datasets/73f5184d9062458c81ff86e5f5bcdbb8_9.geojson'
#geopath = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
counter = 0

@st.cache(allow_output_mutation=True)
def get_data(path):
    df = pd.read_csv(path)
    return df

@st.cache(allow_output_mutation=True)
def get_geodata(geopath):
    geofile = geopandas.read_file(geopath)
    return geofile

def sample(df):
    f_fulldata = st.checkbox('Use full data sample')
    if f_fulldata == False:
        df = df.sample(100, random_state=101)
    else:
        df = df
    return df

def map_filters(df):
    # 2 Map Filters
    st.sidebar.title('Map Filters :world_map:')

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
    f_waterfront = st.sidebar.checkbox(f'Only waterfront properties')
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
           'worth_buying',  'profit_value', 'selling_price', 'condition']]  # ][['id', 'lat', 'long', 'price']]

    return houses

def charts(houses):

    st.subheader('#1) Which real state must be bought by Home Sales and for how much?')
    x1, x2 = st.columns([4,1])
    with x1:
        fig = px.scatter(houses, x='price', y='yr_built', title='<b>Worth Buying Properties</b>',
                         height=300, color='worth_buying', color_continuous_scale=['#EF553B', '#00CC96'], opacity=0.9,
                         size='price', size_max=20,
                         hover_name='id',
                         hover_data={'price': ':,.2f', 'worth_buying': ':.f', 'yr_built':':.f'},
                         labels={'price': 'Price', 'worth_buying': 'Worth Buying', 'yr_built':'Year Built'},
                         template='ggplot2')
        fig.update_layout(title_x=0.525, margin=dict(l=0, r=0, t=25, b=0))
        fig.update_yaxes(showticklabels=False, showgrid=True, title="Year Built", ticks="") #visible=False
        fig.update_xaxes(showgrid=True, ticks="")  # visible=False
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with x2:
        st.write('  \n')
        st.write('  \n')
        st.write('  \n')
        st.metric(label='Worth Buying', value=f'{houses[houses["worth_buying"] == 1]["worth_buying"].count()}/{houses["worth_buying"].count()}', delta=f'{(houses[houses["worth_buying"] == 1]["worth_buying"].count()/houses["worth_buying"].count())*100:.2f}% worths!')
        st.metric(label='Total Investment x Profit Values', value=f'U${millify(houses[houses["worth_buying"] == 1]["price"].sum(), precision=2)}', delta=f'U${millify(houses[houses["worth_buying"] == 1]["profit_value"].sum(), precision=2)} profit!')

    st.subheader('#2) Once the real state is bought, for how much should it be sold?')
    houses2 = houses[houses['worth_buying'] == 1]
    fig2 = px.scatter(houses2, x='selling_price', y='yr_built', title='<b>Selling Price x Profit</b>',
                      height=300, color_discrete_sequence=['#AB63FA'], opacity=0.9,
                      size='profit_value', size_max=20,
                      hover_name='id',
                      hover_data={'selling_price': ':,.2f', 'profit_value': ':.2f'},
                      labels={'selling_price': 'Selling Price', 'profit_value':'Profit Value','yr_built':'Year Built'})
    fig2.update_layout(title_x=0.525, margin=dict(l=0, r=0, t=25, b=0))
    fig2.update_yaxes(showticklabels=False)
    fig2.update_coloraxes(showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

def maps(geofile, houses):
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True) #Exibir os checkboxes na horizontal
    map_type = ['Price Map', 'Density Map', 'Region Price Map']
    map = st.radio('Select map type to show:', map_type)
    #Price Map
    price_map = px.scatter_mapbox(houses, lat='lat', lon='long', size='price', color_continuous_scale=['#60cd06','#da0721'], size_max=12, zoom=10, color='price', hover_name='id')
    price_map.update_layout(mapbox_style='open-street-map', height=800, margin={'r': 0, 't': 0, "l": 0, "b": 0})
    #Density Map
    density_map = folium.Map(location=[houses['lat'].mean(), houses['long'].mean() ], default_zoom_start=15 )
    marker_cluster = MarkerCluster().add_to(density_map)
    popitup = folium.Popup("test", max_width=800, min_width=800, show=True)
    for name, row in houses.iterrows():
       folium.Marker([row['lat'], row['long']],
           popup='<i>${:,.2f}</i>.'
                 '<br><b>Sqft:</b> {};'
                 '<br><b>Bedroom:</b> {};'
                 '<br><b>Bathroom:</b> {:,.0f};'
                 '<br><b>Year Built:</b> {}.'.format(row['price'], row['sqft_living'], row['bedrooms'], row['bathrooms'], row['yr_built']).replace(",",".")).add_to(marker_cluster)

    #Region Price Map
    df2 = houses[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df2.columns = ['ZIP', 'PRICE']
    geofile = geofile[geofile['ZIP'].isin(df2['ZIP'].tolist())]
    region_price_map = folium.Map(location=[df['lat'].mean(), df['long'].mean()], default_zoom_start=15)
    region_price_map.choropleth(data=df2, geo_data=geofile, columns=['ZIP', 'PRICE'], key_on='feature.properties.ZIP', fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2, legend_name='Average price')

    if map == 'Price Map':
            st.plotly_chart(price_map, use_container_width=True)
    elif map == 'Density Map':
            folium_static(density_map)
    else:
            folium_static(region_price_map)

if 'count' not in st.session_state:
    st.session_state.count = 0

def counter():
    st.session_state.count += 1

def intro():
    st.write('Home Sales is a ficticious company specialized in buying and reselling real states.  \n'
             'Our business model consists of analyzing features and locations of properties to perform '
             'advantageous buying and selling operations.  \n'
             'Currently, the objective of data analysis is to find and filter those properties with safe '
             'purchase and profit potential through the answer of two business questions:  \n\n'
             '__Question 1) Which real state must be bought by Home Sales and for how much?__  \n'
             '__Question 2) Once the real state is bought, for how much should it be sold?__  \n\n'
            'The estimated profit (profit_value) on the purchase of a property is about 30% of its purchase value.  \n'
            'This application allows you to travel beyond these data and properties, choosing and filtering its features, locations and values.')
    st.button('Show me the data!', on_click=counter)


#st.title('Home Sales Data Overview :cityscape:')
#if __name__ == '__main__':
#if st.session_state.count % 2 == 0:
#	intro()
#if st.session_state.count % 2 != 0:
#	df = get_data(path)
#	geofile = get_geodata(geopath)
#	df = sample(df)
#	print(geofile)
#	houses = map_filters(df)
#	charts(houses)
#	maps(geofile, houses)
#	st.sidebar.caption('[_Contact me. :email:_](https://www.linkedin.com/in/ricardo-estevam-carli-475461181/)')
print('oi')
geofile = get_geodata(geopath)
print(geofile.head())
