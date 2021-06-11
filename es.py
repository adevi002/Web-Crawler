from datetime import datetime
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup as bs
import os
import sys

print("Welcome to our Elastic Search Program. If you have not run main.py yet please do that first")
print("This is because the index is built upon running this program.")

elastic_pass = 'EuW38Hk5V2HaSDJUQJDLIaEJ'

# i-o-optimized-deployment-f7232d.es.us-west1.gcp.cloud.es.io:9243
elastic_endpoint = "i-o-optimized-deployment-f7232d.es.us-west1.gcp.cloud.es.io:9243"
connection_string = "https://elastic:" + elastic_pass + "@" + elastic_endpoint

# curl -u elastic:EuW38Hk5V2HaSDJUQJDLIaEJ

indexName = "cs172-index"
print(connection_string)
esConn = Elasticsearch(connection_string)
response = esConn.indices.create(index=indexName, ignore=400)
print(response)

directory = "MAJ-Project/HTML/"
for filename in os.listdir(directory):
    # if filename.endswith(".html"):
    print(filename)
    with open(directory+filename, 'r', encoding='utf-8') as f:
        contents = f.read()
        # contents.decode('latin-1')
        # dict1 = {}
        count3 = 0
        count2 = 0
        soup = bs(contents, 'lxml')
        for tag in soup.find_all('h2'):
            count3 += 1
            break
        for tag in soup.find_all('a'):
            count3 += 1
            break
        for tag in soup.find_all('p'):
            count3 += 1
            break
        for tag in soup.find_all('title'):
            count2 += 1
            break
        if count3 > 0 and count2 > 0:
            title_tag = soup.title.text
            tags = soup.find_all(['h2', 'p', 'a'])
            body = ""
            for tag in tags:
                body += " " + tag.text
            
            dict1 = {
                'page_title': title_tag,
                'text': body,
                'timestamp': datetime.now()
            }
            response = esConn.index(index=indexName, id=id, body=dict1)

# print("Please enter which option you would like to select:")
# print("1) PUT a new document")
# print("2) GET results for all")
# print("3) GET results for a query word")
# print("0) Exit")
option = 1

while option == 1 or option == 2 or option == 3:
    print("Please enter which option you would like to select:")
    print("1) PUT a new document")
    print("2) GET results for all")
    print("3) GET results for a query word")
    print("0) Exit")
    option = int(input())
    if option == 0:
        print("Thank you, see you next time")
        sys.exit()
    elif option == 1:
        print("Please add the page title for the document you would like to add: ")
        newDocTitle = str(input())
        print("Please enter the text for the document you would like to add: ")
        newDocText = str(input())
        newDoc = {
            'page_title': newDocTitle,
            'text': newDocText,
            'timestamp': datetime.now()
        }
        response = esConn.index(index=indexName, id=id, body=newDoc)

    elif option == 2:
        response = esConn.search(index=indexName, body={"query": {"match_all": {}}})
        print (response)
    elif option == 3:
        print("Please enter the text you would like to search for:")
        query = str(input())
        response = esConn.search(index=indexName, body={
            'query':{
                'match':{
                    "text":query
                }
            }
        })
        print (response)
