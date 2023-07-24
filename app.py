# IMPORTING NECESSARY LIBRARIES AND DATASET --------------------------------------------------


import folium
import numpy as np
import pandas as pd
import streamlit as st
import plotly_express as px
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu



original_data = pd.read_csv("Sample Superstore Data.csv", parse_dates=["Order Date", "Ship Date"])

original_data["Total_Discount_Given"] = original_data["Quantity"] * original_data["Discount"]



# SETTING BASIC PAGE CONFIGURATION --------------------------------------------------

st.set_page_config(
    page_title = "Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state='collapsed'
    )



# CUSTOM CSS FOR PAGE --------------------------------------------------

streamlit_style = """
			<style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

            div.block-container {padding-top:2rem;}
            div.block-container {padding-bottom:0rem;}

     	    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@700');
			html, body, [class*="css"]  {
			font-family: 'Poppins', sans-serif;
			}

            [data-testid="stMetricValue"] {
            font-size: 20px;
            text-align: bottom;
            font-weight: bold;

			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)



# CUSTOM FUNCTIONS AND VARIABLES --------------------------------------------------

colour_1 = "#FF2626"

def gap(s,n):

    for i in range(n):

        s.write("")



def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")



def add_underscore(df):

    cols = df.columns

    new = []

    for i in cols:

        y = i.replace(" ", "_")

        new.append(y)
    
    df.columns = new

add_underscore(original_data)






# SIDEBAR --------------------------------------------------

with st.sidebar.container():

    st.markdown("<center><h2>○ Filter Pane ○</h2></center>", unsafe_allow_html = True)
    
    gap(st, 1)

    segment = st.multiselect(
        label = "Choose Segments",
        options = original_data["Segment"].unique(),
        default = original_data["Segment"].unique()
        )
    
    region = st.multiselect(
        label = "Choose Region",
        options = original_data["Region"].unique(),
        default = original_data["Region"].unique()
        )
    
    category = st.multiselect(
        label = "Choose Category",
        options = original_data["Category"].unique(),
        default = original_data["Category"].unique()
        )
    
    st.divider()

    st.markdown("<center><h3>○ KPIs Used ○</h3></center>", unsafe_allow_html = True)

    st.write("<h4>1. Gross and Net Profit.</h4>", unsafe_allow_html = True)

    st.write("<h4>2. Customer Retention Cost. (CRC)</h4>", unsafe_allow_html = True)

    st.write("<h4>3. Average Transaction Value. (ATV)</h4>", unsafe_allow_html = True)

    st.write("<h4>4. Basket Size.</h4>", unsafe_allow_html = True)

    df = original_data.query("Segment == @segment & Region == @region & Category == @category")



# HEADER --------------------------------------------------

h1, h2 = st.columns(spec = 2)

with h1.container():

    st.markdown("<h2>📊 Superstore Sales Dashboard</h2>", unsafe_allow_html = True)

with h2.container():

    selected = option_menu(
                menu_title = None,
                options = ["Profit", "Sales", "Quantity"],
                icons = ["house-fill", "laptop-fill", "person-badge-fill"],
                menu_icon = "cast",
                default_index = 1,
                orientation = "horizontal",
                styles={
                "container": {"font-family": sans-serif, "text-align": "left"},
                "nav-link": {"font-size": "15px", "text-align": "center"}
                }
            )


st.divider()



gap(st, 2)



c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17  = st.columns(spec = [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2])



ts = df["Sales"].sum()

ts_inm = round(ts/10000, 2)

to = len(df["Order_ID"].unique())

gp = round(df["Profit"].sum(), 2)

gp_inm = round(gp/10000, 2)

td = df["Total_Discount_Given"].sum()
    
netp = ts - td

netp_inm = round(netp/10000, 2)

crc = round(( df["Total_Discount_Given"].sum() / len(df["Customer_ID"].unique()) ), 2)

atv = round( ts / to, 2 )

tqs = df["Quantity"].sum()

bs = round( tqs / to, 2 )

tro = len(df[df["Returned"] == "Y"])



with c1.container():

    st.metric(label = "\# Sales", value = f"$ {ts_inm} M")

with c3.container():

    st.metric(label = "Gross Profit", value = f"$ {gp_inm} M")

with c5.container():

    st.metric(label = "Net Profit", value = f"$ {netp_inm} M")

with c7.container():

    st.metric(label = "CRC", value = f"$ {crc}")

with c9.container():

    st.metric(label = "ATV", value = f"$ {atv}")

with c11.container():

    st.metric(label = "Basket Size", value = f"{bs}")

with c13.container():

    formatted = "{:,}".format(to)

    st.metric(label = "\# Orders", value = f"{formatted}")

with c15.container():

    st.metric(label = "\# Ret. Orders", value = f"{tro}")

with c17.container():

    formatted = "{:,}".format(tqs)

    st.metric(label = "\# Quantities", value = f"{formatted}")


for i in [c2, c4, c6, c8, c10, c12, c14, c16]:

    gap(i, 1)

    i.image(image = "images/border_1.png")

st.divider()



# SECTION ONE --------------------------------------------------

segment_wise = df.pivot_table(index = "Segment", values = ["Sales", "Quantity", "Profit"], aggfunc = "sum")

category_wise = df.pivot_table(index = "Category", values = ["Sales", "Quantity", "Profit"], aggfunc = "sum")

sub_category_wise = df.pivot_table(index = "Sub-Category", values = ["Sales", "Quantity", "Profit"], aggfunc = "sum")

region_wise = df.pivot_table(index = "Region", values = ["Sales", "Quantity", "Profit"], aggfunc = "sum")



sec_1_1, sec_1_2, sec_1_3 = st.columns(spec = [5,1,5])


with sec_1_2.container():

    gap(st, 5)

    st.image(image = "images/border_2.png")

with sec_1_3.container():

    gap(st, 2)

    st.markdown(f"<center><h4>Total {selected} by States</h4></center>", unsafe_allow_html = True)

    gap(st, 2)

    state_wise = df.pivot_table(index = "State", values = ["Sales", "Quantity", "Profit"], aggfunc = "sum").reset_index()

    state_wise_indexed = df.pivot_table(index = "State", values = ["Sales", "Quantity", "Profit"], aggfunc = "sum")

    map = folium.Map(location = [38, -96.5],
                     zoom_start = 4,
                     scrollWheelZoom = False,
                     tiles = "CartoDB dark_matter")
    
    choropleth = folium.Choropleth(
        geo_data = "data/us-state-boundaries.geojson",
        data = state_wise,
        columns = ("State",selected),
        key_on = "feature.properties.name",
        line_opacity=0.8,
        fill_color = "YlOrRd",
        highlight = True
    )

    choropleth.geojson.add_to(map)

    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name']
        feature['properties']['profit'] = 'Profit: $ ' + '{:,}'.format(round(state_wise_indexed.loc[state_name, 'Profit'],2)) if state_name in list(state_wise_indexed.index) else ''
        feature['properties']['sales'] = 'Sales: $ ' + '{:,}'.format(round(state_wise_indexed.loc[state_name, 'Sales'],2)) if state_name in list(state_wise_indexed.index) else ''
        feature['properties']['quantity'] = 'Quantity: ' + '{:,}'.format(state_wise_indexed.loc[state_name, 'Quantity']) if state_name in list(state_wise_indexed.index) else ''

    if selected == "Profit":

        choropleth.geojson.add_child(

            folium.features.GeoJsonTooltip(["name",'profit'], labels = False)
        )
    
    if selected == "Sales":

        choropleth.geojson.add_child(

            folium.features.GeoJsonTooltip(["name",'sales'], labels = False)
        )
    
    if selected == "Quantity":

        choropleth.geojson.add_child(

            folium.features.GeoJsonTooltip(["name",'quantity'], labels = False)
        )

    st_map = st_folium(map,
                       width = 750,
                       height = 400)


with sec_1_1.container():

    gap(st, 2)

    selected2 = option_menu(
                menu_title = None,
                options = ["Category", "Segment", "Region", "Sub-Category"],
                icons = ["house-fill", "laptop-fill", "person-badge-fill", "person-badge-fill"],
                menu_icon = "cast",
                default_index = 1,
                orientation = "horizontal",
                styles={
                "container": {"font-family": "Poppins", "text-align": "left"},
                "nav-link": {"font-size": "15px", "text-align": "center"}
                }
            )
    
    if selected2 == "Category":
    
        g_3 = px.bar(
            category_wise,
            x=selected,
            y=category_wise.index,
            orientation="h",
            title=f"Total {selected} by {selected2}",
            color_discrete_sequence=[colour_1] * len(category_wise),
            template="plotly_white")

        g_3.update_layout(
            title_x=0.4,
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
            xaxis=None
        )

        st.plotly_chart(g_3, use_container_width=True)
    
    elif selected2 == "Segment":

        g_1 = px.bar(
            segment_wise,
            x=selected,
            y=segment_wise.index,
            orientation="h",
            title=f"Total {selected} by {selected2}",
            color_discrete_sequence=[colour_1] * len(segment_wise),
            template="plotly_white")

        g_1.update_layout(
            title_x=0.4,
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
            xaxis=None
        )

        st.plotly_chart(g_1, use_container_width=True)

    elif selected2 == "Region":

        g_2 = px.bar(
            region_wise,
            x=selected,
            y=region_wise.index,
            orientation="h",
            title=f"Total {selected} by {selected2}",
            color_discrete_sequence=[colour_1] * len(region_wise),
            template="plotly_white")

        g_2.update_layout(
            title_x=0.4,
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
            xaxis=None
        )

        st.plotly_chart(g_2, use_container_width=True)
    
    elif selected2 == "Sub-Category":

        g_4 = px.bar(
            sub_category_wise,
            y=selected,
            x=sub_category_wise.index,
            title=f"Total {selected} by {selected2}",
            color_discrete_sequence=[colour_1] * len(sub_category_wise),
            template="plotly_white")

        g_4.update_layout(
            title_x=0.4,
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
            xaxis=None
        )

        st.plotly_chart(g_4, use_container_width=True)




st.divider()



# SECTION TWO --------------------------------------------------



# DATAFRAME CREATION



dates_df = df[["Order_Date", "Sales", "Profit", "Quantity"]]

dates_df["Order_Year"] = dates_df["Order_Date"].dt.year

dates_df["Order_Month"] = dates_df["Order_Date"].dt.month_name()

dates_df["Order_Mon"] = dates_df["Order_Date"].dt.month

dates_df["Order_Quarter"] = dates_df["Order_Date"].dt.quarter

dates_df["Order_Month_Year"] = dates_df['Order_Date'].dt.strftime('%b') + "_" + dates_df["Order_Year"].astype(str).str[-2:]

dates_df["Order_Quarter_Year"] = dates_df["Order_Year"].astype(str) + "_" + "Q" + dates_df["Order_Quarter"].astype(str)

dates_df = dates_df.sort_values(by = ["Order_Year", "Order_Mon"])



sec_2_1, sec_2_2, sec_2_3, sec_2_4, sec_2_5 = st.columns(spec = [4,1,16,3,6])

with sec_2_4.container():

    gap(st, 5)

    st.image("images/border_3.png")

with sec_2_1.container():

    gap(st, 7)

    selected3 = option_menu(
                    menu_title = None,
                    options = ["Monthly", "Yearly", "Quarterly", "Combined"],
                    icons = ["house-fill", "laptop-fill", "person-badge-fill", "person-badge-fill"],
                    menu_icon = "cast",
                    default_index = 1,
                    orientation = "vertical",
                    styles={
                    "container": {"font-family": "Poppins", "text-align": "left"},
                    "nav-link": {"font-size": "15px", "text-align": "center"}
                    }
                )


if selected3 == "Monthly":

    with sec_2_3.container():

        ind = "Order_Month"

        months = pd.DataFrame({"Month_Name" : ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                "Month_Number" : [1,2,3,4,5,6,7,8,9,10,11,12]})
        
        a = dates_df.pivot_table(index = ind, values = ["Sales", "Quantity", "Profit"], aggfunc = "sum").reset_index()

        final = a.merge(right = months,
                        how = "inner",
                        left_on = "Order_Month",
                        right_on = "Month_Name").sort_values(by = "Month_Number")
        
        g_5 = px.line(data_frame = final,
                    x = ind,
                    y = selected,
                    markers = True,
                    line_shape = "spline",
                    color_discrete_sequence = ["red"],
                    title = f"{selected3} trend of total {selected}"
        )

        g_5.update_traces(marker=dict(size=8,color="white"))

        g_5.update_layout(
                title_x=0.4,
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=(dict(showgrid=False)),
                xaxis=None
            )
        
        st.plotly_chart(g_5, use_container_width=True)

elif selected3 == "Yearly":

    ind = "Order_Year"

    with sec_2_3.container():

        a = dates_df.pivot_table(index = ind, values = ["Sales", "Quantity", "Profit"], aggfunc = "sum").reset_index()

        g_5 = px.line(data_frame = a,
                    x = ind,
                    y = selected,
                    markers = True,
                    line_shape = "spline",
                    color_discrete_sequence = ["red"],
                    title = f"{selected3} trend of total {selected}"
        )

        g_5.update_traces(marker=dict(size=8,color="white"))


        g_5.update_layout(
                title_x=0.4,
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=(dict(showgrid=False)),
                xaxis=None
            )
        
        g_5.update_xaxes(
                tickmode='linear',
                dtick=1
            )
        
        st.plotly_chart(g_5, use_container_width=True)

elif selected3 == "Quarterly":

    ind = "Order_Quarter_Year"

    with sec_2_3.container():

        a = dates_df.pivot_table(index = ind, values = ["Sales", "Quantity", "Profit"], aggfunc = "sum").reset_index()
        
        g_5 = px.line(data_frame = a,
                    x = ind,
                    y = selected,
                    markers = True,
                    line_shape = "spline",
                    color_discrete_sequence = ["red"],
                    title = f"{selected3} trend of total {selected}"
        )

        g_5.update_traces(marker=dict(size=8,color="white"))

        g_5.update_layout(
                title_x=0.4,
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=(dict(showgrid=False)),
                xaxis=None
            )
        
        st.plotly_chart(g_5, use_container_width=True)

elif selected3 == "Combined":

    ind = "Order_Month_Year"

    cols = ["Order_Month_Year", "Profit", "Quantity", "Sales", "Month_Name", "Month_Number"]

    dff = pd.DataFrame(columns=cols)

    with sec_2_3.container():

        years = [2014, 2015, 2016, 2017]

        for i in years:

            j = str(i)[-2:]

            months = pd.DataFrame({"Month_Name" : ["Jan_" + j, "Feb_" + j, "Mar_" + j, "Apr_" + j, "May_" + j, "Jun_" + j, "Jul_" + j, "Aug_" + j, "Sept_" + j, "Oct_" + j, "Nov_" + j, "Dec_" + j],
                "Month_Number" : [1,2,3,4,5,6,7,8,9,10,11,12]})

            new_df = dates_df[dates_df["Order_Year"] == i]

            a = new_df.pivot_table(index = ind, values = ["Sales", "Quantity", "Profit"], aggfunc = "sum").reset_index()

            final = a.merge(right = months,
                        how = "inner",
                        left_on = "Order_Month_Year",
                        right_on = "Month_Name").sort_values(by = "Month_Number")
            
            dff = pd.concat([dff, final], axis=0, ignore_index=True)
            
        g_5 = px.line(data_frame = dff,
                    x = ind,
                    y = selected,
                    markers = True,
                    line_shape = "spline",
                    color_discrete_sequence = ["red"],
                    title = f"{selected3} trend of total {selected}"
        )

        g_5.update_traces(marker=dict(size=8,color="white"))

        g_5.update_layout(
                title_x=0.4,
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=(dict(showgrid=False)),
                xaxis=None
            )
        
        st.plotly_chart(g_5, use_container_width=True)



with sec_2_5.container():

    gap(st, 2)

    ship_mode_wise = df.pivot_table(index = "Ship_Mode", values = ["Sales", "Quantity", "Profit"], aggfunc = "sum").reset_index()



    g_6 = px.pie(data_frame = ship_mode_wise,
                    values = selected,
                    names = "Ship_Mode",
                    # title = f"Total {selected} by Ship Mode",
                    color_discrete_sequence=px.colors.sequential.RdBu
        )
    
    g_6.update_traces(hoverinfo = 'label+percent',
                      textinfo = 'percent',
                      textfont_size = 15,
                      textposition = 'inside')

    g_6.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            title=dict(text=f"Total {selected} by Ship Mode", font=dict(size=17), x=0.4, xref="paper")
        )
    
    st.plotly_chart(g_6, use_container_width=True)




st.divider()



# FOOTER --------------------------------------------------




footer_1, footer_2, footer_3 = st.columns(spec = 3)

footer_1.markdown('''<b>Let's Connect: &nbsp;&nbsp;&nbsp;</b> <a style = "color: #FFFFFF; text-decoration: none;  width: 500px; height: 500px;" href = "https://www.linkedin.com/in/saurabh-narwane/"> <i class="fa-brands fa-linkedin"></i></a>
                <a style = "color: #FFFFFF; text-decoration: none;  width: 500px; height: 500px;" href = "https://twitter.com/saurabhnarwane"> <i class="fa-brands fa-twitter"></i></a>
                <a style = "color: #FFFFFF; text-decoration: none;  width: 500px; height: 500px;" href = "https://www.instagram.com/saurabh.narwane/"> <i class="fa-brands fa-instagram"></i></a>
                <a style = "color: #FFFFFF; text-decoration: none;  width: 500px; height: 500px;" href = "https://www.youtube.com/channel/UCnDX94mNIcHTHKScgBFzkbQ"> <i class="fa-brands fa-youtube"></i></a>''',
                unsafe_allow_html = True)

st.markdown(
    """
    <style>
    .center-align {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

footer_2.markdown('''<div class="center-align">
                <a href="https://www.novypro.com/profile_projects/saurabhnarwane">
                <img border="0" alt="Novy Pro" src="https://i.imgur.com/6Zoa2mR.png" width="25" height="25">
                </a>
                &nbsp;&nbsp;&nbsp;
                <a href="https://github.com/SN11112001">
                <img border="0" alt="GitHub" src="https://i.imgur.com/ytYEVVv.png" width="25" height="25">
                </a>
                &nbsp;&nbsp;&nbsp;
                <a href="https://public.tableau.com/app/profile/saurabh.narwane">
                <img border="0" alt="Tableau Public" src="https://i.imgur.com/4DXzz7F.png" width="25" height="25">
                </a>''',
                unsafe_allow_html = True)

st.markdown(
    """
    <style>
    .right-align {
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

footer_3.markdown('''<div class="right-align"><b style = "text-alignment:right;">© 2023 Saurabh Narwane. All Rights Reserved.</b></div>''',
                unsafe_allow_html = True)
