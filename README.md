# PCAP-Data-Extraction-Utility

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#) [![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=fff)](#) [![NumPy](https://img.shields.io/badge/NumPy-4DABCF?logo=numpy&logoColor=fff)](#) [![Matplotlib](https://custom-icon-badges.demolab.com/badge/Matplotlib-71D291?logo=matplotlib&logoColor=fff)](#)

Also uses:
+ Wireshark, Streamlit, and NetworkX

### About
Written in Python and using Streamlit, this is a lightweight, rapid-analysis utility designed to read and parse packet capture (*.pcap, or *.pcapng) files from Wireshark or a similar utility, and subsequently maps the network connections out in a visible network graph. The utility also provides a Pandas Dataframe as an export of the packet capture, which can be downloaded as an Excel file for further analysis.

Simply upload a .pcap or .pcapng file, and the utility will handle the rest. This makes troubleshooting connections or searching for malicious actors from a packet capture much easier than digging through the packet capture itself.

### Dependencies
The libraries used to run the utility are in requirements.txt. Install these in your Python virtual environment by running:
+ pip install -r requirements.txt

### Running the Tool
Since the tool is built on Streamlit, simply run:
+ streamlit run pcap.py
+ This will launch the web page for it automatically.

### Protocol Mapping
The dictionary for protocols corresponding to Wireshark's numerical labels for them is defined in protocols.py. If any protocols are added in Wireshark in the future, just add them to the dictionary to be defined. The tool won't fail if a protocol isn't defined in the dictionary, but it may display the numerical value from Wireshark for it (ex: 133 is UDPLite in Wireshark).

### Preview
