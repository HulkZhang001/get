import wget
import subprocess
from xml.dom.minidom import parse
import math
import pandas as pd

minLat=input("minLat:")
maxLat=input("maxLat:")
minLon=input("minLon:")
maxLon=input("maxLon:")
product_type=input("product_type:")
ingestion_date_FROM=input("ingestion_date_FROM:")
ingestion_date_TO=input("ingestion_date_TO:")
sensing_date_FROM=input("sensing_date_FROM:")
sensing_date_TO=input("sensing_date_TO:")

product_type='SLC'
ingestion_date_FROM='2019-07-11T06:00:00.000Z'
ingestion_date_TO='NOW'
sensing_date_FROM='2016-10-10T12:00:00.000Z'
sensing_date_TO='NOW'

minLat='-4.5300000000000'
maxLat='26.7500000000000'
minLon='29.8500000000000'
maxLon='46.8000000000000'
rows='50'
start='50'

prex = 'https://scihub.copernicus.eu/dhus/search?q=%20producttype:'
ingestion_date = product_type + '%20AND%20%20ingestiondate:[' + ingestion_date_FROM + '%20TO%20' + ingestion_date_TO + ']%20%20%20AND%20%20(%20footprint:%22Intersects(POLYGON(('
# beginPosition = ']%20%20%20AND%20%20beginPosition:[' + sensing_date_FROM + '%20TO%20' + sensing_date_TO
area = minLat+'%20'+minLon+','+maxLat+'%20'+minLon+','+maxLat+'%20'+maxLon+','+minLat+'%20'+maxLon+','+minLat+'%20'+minLon+'%20)))%22)'
num = '&rows=' + rows + '&start=' + start
url = prex + ingestion_date  + area + num

cmd='wget --no-check-certificate --user=sdzhouwenming --password=chow0819 --output-document=%s "%s"'%('tt.xml',url)
subprocess.call(cmd,shell=True)

domTree = parse("./tt.xml")
rootNode = domTree.documentElement
totalResults = rootNode.getElementsByTagName("opensearch:totalResults")
results_sum = totalResults[0].firstChild.data
page_num = math.ceil(int(results_sum)/int(rows))

items=[]

for i in range(page_num):
    start = i * int(rows)
    num = '&rows=' + rows + '&start=' + str(start)
    url = prex + ingestion_date  + area + num
    file_name = str(i) + '.xml' 
    cmd='wget --no-check-certificate --user=sdzhouwenming --password=chow0819 --output-document=%s "%s"'%(file_name , url)
    subprocess.call(cmd,shell=True)
    

for i in range(page_num):
    file_name = str(i) + '.xml' 
    loc = './' + file_name 
    domTree = parse(loc)
    rootNode = domTree.documentElement
    entry = rootNode.getElementsByTagName("entry")
    for e in entry:
        title = e.getElementsByTagName("title")
        title_name = title[0].firstChild.data 
        link = e.getElementsByTagName("link")
        link_href = link[0].getAttribute("href")
        s = e.getElementsByTagName("str")
        size = s[15].firstChild.data
        gmlfootprint = s[16].firstChild.data
        footprint = s[17].firstChild.data
        new_item = (title_name, link_href, size, gmlfootprint, footprint)
        items.append(new_item)
        
        #print(new_item)
        
        
print("total:",results_sum)
df = pd.DataFrame(items, columns=['title_name', 'link_href', 'size', 'gmlfootprint', 'footprint'])
df.to_csv("result_info.csv", header=True, index=False,encoding="utf_8_sig")
print("result saved successfully!")