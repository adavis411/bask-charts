# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
  
cols = ["latitude", "longitude", "sid", "title", "chart_title", "type"]
rows = []
  
# Parsing the XML file
xmlparse = Xet.parse('datapoints-0710.xml')
root = xmlparse.getroot()
for i in root:
    t = i.attrib["station_type"]
    marker = i.find("marker")
    latitude = marker.attrib["lat"]
    longitude = marker.attrib["lng"]
    title = i.attrib["title"]
    if "xid" in i.attrib:
        sid = "x_" + i.attrib["xid"]
    elif "cid" in i.attrib:
        sid = "c_" + i.attrib["cid"]
    elif "tid" in i.attrib:
        sid = "t_" + i.attrib["tid"]
    else:
        sid = ""

    if "chart_title" in i.attrib:
        chart_title = i.attrib["chart_title"]
    else:
        chart_title = ""

    rows.append({"latitude": latitude,
                 "longitude": longitude,
                 "sid": sid,
                 "title": title,
                 "chart_title": chart_title,
                 "type": t})
  
df = pd.DataFrame(rows, columns=cols)
  
# Writing dataframe to csv
df.to_csv('datapoints-0710.csv', index=False)