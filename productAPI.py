#!/usr/bin/python3
import pandas as pd
import urllib.request
import json
import gzip
import csv

# Products array
products = []

# CSV filename
filename = "products.csv.gz"


# Name: keyHasValue
# Descript: Checks if the diccionari/object has the key, if not set to 'null'
# IN: object / key
# OUT: object value or null
def keyHasValue(object, key):
    if key in object:
        return object[key]
    else:
        return 'null'

# Name: checkAndReplace
# Descript: Checks if the entering value has quotes on it, and removes them
# IN: Value with or without quotes
# OUT: Value without quotes
def checkAndReplace(value):
    return value.replace('"', '')

# Product class to store the products, it will need to be on the Database
class Product:

    # Init the object
    def __init__(self, id, name, brand, retailer, price, inStock):
        self.id = id
        self.name = name
        self.brand = brand
        self.retailer = retailer
        self.price = price
        self.inStock = inStock

    # Id getter
    def getId(self):
        return self.id


# Name: addJSON_Records
# Descript: Takes the JSON file from URL and decodes de content to be able to work with it. Then it saves all records on a Product array.
# IN:
# OUT:
def addJSON_Records():
    # Open the URL of the JSON and save all the info
    with urllib.request.urlopen("https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.json") as url:
        data = json.loads(url.read().decode())

    for record in data:
        # Create the temporal object
        tmp = Product(keyHasValue(record, 'id'), keyHasValue(record, 'name'), keyHasValue(record, 'brand'), keyHasValue(
            record, 'retailer'), keyHasValue(record, 'price'), keyHasValue(record, 'in_stock'))

        # Append the object to the list
        products.append(tmp)


# Name: addCSV_Records
# Descript: Read the content of the CSV using pandas read_csv. Then it saves all records on a Product array
# IN:
# OUT:
def addCSV_Records():
    # Get the data from the CSV
    data = pd.read_csv('products.csv.gz', compression='gzip',
                       encoding='utf-8-sig')

    # Get Data Lenght
    for i in range(len(data.index)):
        # All except Id need to have a space in front
        tmp = Product(data['Id'][i], checkAndReplace(data[' Name'][i]), checkAndReplace(data[' Brand'][i]), checkAndReplace(
            data[' Retailer'][i]), checkAndReplace(data[' Price'][i]), checkAndReplace(data[' InStock'][i]))
        # print(data['Id'][i])
        print(tmp.getId())

        products.append(tmp)
