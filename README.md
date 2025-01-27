# Packet Capture Mapping & Analytics Web App Utility

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#) [![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=fff)](#) [![NumPy](https://img.shields.io/badge/NumPy-4DABCF?logo=numpy&logoColor=fff)](#) [![Matplotlib](https://custom-icon-badges.demolab.com/badge/Matplotlib-71D291?logo=matplotlib&logoColor=fff)](#)

Also uses:
+ Wireshark, Streamlit, and NetworkX


### About
Written in Python and using Streamlit, this is a lightweight, rapid-analysis utility designed to read and parse packet capture (*.pcap, or *.pcapng) files from Wireshark or a similar utility. It will subsequently map the network connections out in a visible network graph. The utility also provides 2 separate, easily-readable tables, and an export of the packet capture's raw data, which can be downloaded as a CSV file for further analysis.

Simply upload a .pcap or .pcapng file, and the utility will handle the rest. This makes troubleshooting connections or searching for malicious actors from a packet capture much easier than digging through the packet capture itself. Note that this utility is not connected to any database or store. It won't save the packet capture details anywhere, other than in memory, which is by design for security.


### Dependencies
The libraries used to run the utility are in requirements.txt. Install these in your Python virtual environment by running:
+ pip install -r requirements.txt

If you encounter build errors, it's likely related to Matplotlib, and a dependency it has (freetype). Matplotlib requires Microsoft Visual C++ 14.0 or greater to be installed on the Windows machine running it. 
Get it with "Microsoft C++ Build Tools": 
https://visualstudio.microsoft.com/visual-cpp-build-tools/. This cannot be pushed over pip or other Python package managers.


### Running the Tool
Since the tool is built on Streamlit, simply run:
+ streamlit run pcap.py
+ This will launch the web page for it automatically. _(screenshots below)_
+ Upon uploading your pcap or pcapng file(s), the tool will automatically run, and you'll receive 2 toast messages if everything ran correctly.


### Protocol Mapping
The dictionary for protocols corresponding to Wireshark's numerical labels for them is defined in protocols.py. If any protocols are added in Wireshark in the future, just add them to the dictionary to be defined. The tool won't fail if a protocol isn't defined in the dictionary, but it may display the numerical value from Wireshark for it (ex: 133 is UDPLite in Wireshark).


### Preview
_Note: IP's not visible in screenshots below by design. Please run independent tests on your own network(s) to view data._
![Base Utility](https://github.com/user-attachments/assets/bb27c35f-de92-4db6-8cf8-ce626e3251bb)
![Upload_Success_obf](https://github.com/user-attachments/assets/992090d8-6707-4a3e-84ac-5714bbbd8ebf)
![Network_obf](https://github.com/user-attachments/assets/b2aec340-1ec3-4492-9cf1-9870c6965482)
![Occurences_obf](https://github.com/user-attachments/assets/89e20375-4e46-411f-b5bd-e2b32f5033a1)
