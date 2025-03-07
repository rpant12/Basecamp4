import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(
    page_title="Flexera Server Allocation Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded",
    )


st.title("Flexera Server Allocation Dashboard")

st.subheader("Data As of " + str(datetime.now().strftime("%m-%d-%Y")))

servers = pd.read_csv('query.csv')

overall = pd.read_csv("SNow.csv")

op_status = ["In Operation", "Non-operational", "Retired"]
cmdb_count = [overall[overall.get("OPERATIONAL_STATUS") == 1].shape[0], overall[overall.get("OPERATIONAL_STATUS") == 2].shape[0], overall[overall.get("OPERATIONAL_STATUS") == 6].shape[0]]
felxera_count = [servers[servers.get("OPERATIONAL_STATUS") == 1].shape[0], servers[servers.get("OPERATIONAL_STATUS") == 2].shape[0], servers[servers.get("OPERATIONAL_STATUS") == 6].shape[0]]

overall["OpStatus"] = overall["OPERATIONAL_STATUS"].replace({1: "In Operation", 2: "Non-operational", 6: "Retired"})
servers["OpStatus"] = servers["OPERATIONAL_STATUS"].replace({1: "In Operation", 2: "Non-operational", 6: "Retired"})


newDF = pd.DataFrame()
newDF["CDMB Operational Status"] = op_status
newDF["CMDB Asset Count"] = cmdb_count
newDF["Flexera Asset Count (Matched)"] = felxera_count

st.table(newDF)

dupes = servers.duplicated(subset = "COMPUTERNAME")

with st.sidebar:
    st.title('Flexera Server Allocation Dashboard')
    
    year_list = ["All", "In Operation", "Non-operational", "Retired"]
    
    selected_status = st.selectbox('Select an operational status', year_list, index=len(year_list)-1)
    if selected_status != "All":
        server_selected_status = servers[servers["OpStatus"] == selected_status]
    else:
        server_selected_status = servers       
col1, col2, col3 = st.columns(3)

col1.metric(label = "Count of Matched Flexera Assets", value = str(servers.shape[0]))
col2.metric(label = "Count of Total CMDB Assets", value = str(overall.shape[0]))
col3.metric(label = "\% of Assets Scanned", value = str(servers.shape[0] / overall.shape[0] * 100)[0:5] + "%")



style_metric_cards(background_color = "#292D34", border_size_px = 3, border_color = "#292D34", border_radius_px = 3, border_left_color = "#64B2F7")

st.dataframe(server_selected_status)
# with st.sidebar:
#     st.title('🏂 Flexera Server Allocation Dashboard')