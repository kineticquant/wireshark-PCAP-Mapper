import streamlit as st
import logging
import warnings
import time
import io
import pandas as pd
from scapy.all import rdpcap
import random
from protocols import protocols
import networkx as nx
import matplotlib.pyplot as plt
import base64
#import matplotlib.patches as patches
#from matplotlib.patches import FancyArrowPatch

# load proc
timeStr = time.strftime("%Y%m%d-%H%M%S")
timeStrCln = time.strftime("%m-%d-%Y %H:%M")
timeStrSmpl = time.strftime("%m-%d-%Y")
buffer = io.BytesIO()
st.set_page_config(page_title='PCAP Data Extraction Utility', page_icon='MM', initial_sidebar_state='expanded')
#st.sidebar.title("Navigation")

hd_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hd_st_style, unsafe_allow_html=True)

footer="""<style>
a:link , a:visited{
color: black;
background-color: white;
font-size: 15px;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
font-size: 15px;
}
</style>
<div class="footer">
<a style='display: block; text-align: center;' href="https://mikemooney.org" target="_blank">Michael Mooney Software</a>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
# end load proc

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", message="Scapy has detected that your pcap service is not running !")
warnings.filterwarnings("ignore", message="Could not start the pcap service")
warnings.filterwarnings("ignore", message="Access is denied.")

def extrPCAPData(pcapFile):
    packets = rdpcap(pcapFile)

    # List to store packet details
    detailAnalysisDF = []

    for idx, packet in enumerate(packets):
        if 'IP' in packet:
            srcIP = packet['IP'].src
            dstIP = packet['IP'].dst
            protocolNum = packet['IP'].proto
            protocol = protocols.get(protocolNum, 'Unknown')
            
            length = len(packet)
            info = packet.summary()

            detailAnalysisDF.append([idx, srcIP, dstIP, protocol, length, info])

    detailedDF = pd.DataFrame(detailAnalysisDF, columns=['No.', 'Source', 'Destination', 'Protocol', 'Length', 'Info'])
    return detailedDF

def extrIPsFlows(pcapFile):
    packets = rdpcap(pcapFile)
    
    # Store flows
    flows = {}

    for packet in packets:
        if 'IP' in packet:
            srcIP = packet['IP'].src
            dstIP = packet['IP'].dst
            
            flow = f"{srcIP}->{dstIP}"

            # Check if flow already exists in the dictionary
            if flow in flows:
                flows[flow] += 1
            else:
                flows[flow] = 1
                
    flowDataDF = {
        "Source IP": [flow.split('->')[0] for flow in flows.keys()],
        "Destination IP": [flow.split('->')[1] for flow in flows.keys()],
        "Occurrences": list(flows.values())
    }
    flowDF = pd.DataFrame(flowDataDF)

    return flowDF

def drawNtwkMap(uniqueDataDF):
    st.divider()
    st.caption("Click the expand button in the top right of the image to view in full-screen.")
    
    st.set_option('deprecation.showPyplotGlobalUse', False)

    G = nx.DiGraph()

    for index, row in uniqueDataDF.iterrows():
        source = row['Source']
        destination = row['Destination']
        edge_color = 'gray'

        G.add_edge(source, destination, color=edge_color)

    plt.figure(figsize=(10, 14))

    pos = nx.spring_layout(G, k=1.5)
    maxPopSrc = uniqueDataDF['Source'].mode().values[0]
    
    nodeBorderCol = []
    nodeFillCol = []
    
    for node in G.nodes():
        if node == maxPopSrc:
            nodeBorderCol.append('black')
            nodeFillCol.append('lightblue')
        else:
            nodeBorderCol.append(random.choice(list(plt.cm.tab20.colors)))
            nodeFillCol.append('white')

    # Ensure both lists have the same length otherwise dep
    maxNodeLength = max(len(nodeBorderCol), len(nodeFillCol))
    nodeBorderCol.extend(['gray'] * (maxNodeLength - len(nodeBorderCol)))
    nodeFillCol.extend(['white'] * (maxNodeLength - len(nodeFillCol)))

    nx.draw(G, pos, with_labels=True, node_size=8000, node_color=nodeFillCol, edgecolors=nodeBorderCol, linewidths=2, arrows=True, edge_color='gray')


    plt.axis('off')

    col1, col2, col3 = st.columns(3)

    with col1:
        imageDLFormat = st.selectbox("Select desired download format:", ["PNG", "JPG"])
    with col2:
        ""
    with col3:
        st.caption("Analysis as of " + timeStrCln)
        
    col4, col5 = st.columns(2)

    imgbtnLbl = "Download Image as " + imageDLFormat
    saveImg = st.download_button(label=imgbtnLbl, data=imageDLBytes(plt), file_name=f"network_plot_{timeStrSmpl}.{imageDLFormat.lower()}", mime=f"image/{imageDLFormat.lower()}")

    st.pyplot()

def imageDLBytes(plot):
    buffer = io.BytesIO()
    plot.savefig(buffer, format="png")
    buffer.seek(0)
    return buffer


def main():
    st.subheader("PCAP Data Extraction Utility")

    fileUpl = st.file_uploader("Upload a packet capture file (PCAP or PCAPNG) to conduct an analysis.", type=["pcap", "pcapng"])

    if fileUpl is not None:
        st.divider()

        extensionType = fileUpl.name.split('.')[-1].lower() if '.' in fileUpl.name else None
        mimeType = fileUpl.type

        if extensionType == 'pcap' or mimeType == 'application/vnd.tcpdump.pcap' or mimeType == 'application/x-pcap':
            with open("temp.pcap", "wb") as f:
                f.write(fileUpl.getvalue())
            st.toast("PCAP file saved successfully.")
        elif extensionType == 'pcapng' or mimeType == 'application/pcapng':
            with open("temp.pcapng", "wb") as f:
                f.write(fileUpl.getvalue())
            st.toast("PCAPNG file saved successfully.")
        else:
            st.error("Unsupported file format. Please upload a PCAP or PCAPNG file.")

        # Extract detailed packet data and display in a DataFrame
        detailAnalysisDF = extrPCAPData("temp.pcap")#.reset_index(drop=True)
        st.caption("Raw packet capture details:")
        st.toast("Analysis complete.")
        
        #columns = len(detailAnalysisDF.columns)
        #width = columns * 100
        st.dataframe(detailAnalysisDF,hide_index=True)

        #### Don't want to require manual interaction. Auto-draw map on upload
        #if st.button("Show Network Map"): 
        uniqueDataDF = detailAnalysisDF[['Source', 'Destination']].drop_duplicates()
        drawNtwkMap(uniqueDataDF)   
        
        st.divider()
        
         # Extract flows and display in a DataFrame
        flowDataDF = extrIPsFlows("temp.pcap").sort_values(by="Occurrences", ascending=False)
        st.caption("Occurence analysis:")
        st.markdown(
        f'<div style="display: flex; justify-content: center;">{flowDataDF.to_html()}</div>',
        unsafe_allow_html=True
        )
        #st.dataframe(flowDataDF,hide_index=True)

if __name__ == '__main__':
    main()