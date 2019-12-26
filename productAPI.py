#!/usr/bin/python3
# coding=utf-8
from flask import Flask, request, send_from_directory
from flask_jsonpify import jsonify
import pandas as pd
import urllib.request
import json

app = Flask(__name__)

# Products array
products = []

# Order products array
SoProducts = []

selectedProducts = []

# CSV filename
filename = "products.csv.gz"


# Name: keyHasValue
# Descript: Checks if the diccionari/object has the key, if not set to None
# IN: object / key
# OUT: object value or null
def keyHasValue(object, key):
    if key in object:
        if object[key] is not None:
            if object[key] is not "":
                if key is 'price':
                    return float(object[key])
                else:
                    return object[key]
            else:
                return None
        else:
            return None
    else:
        return None

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
    # Print message to terminal
    print("Reading content from external JSON")

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
    # Print message to terminal
    print("Reading content from CSV")

    # Get the data from the CSV
    data = pd.read_csv('products.csv.gz', compression='gzip',
                       encoding='utf-8-sig')

    # Get Data Lenght
    for i in range(len(data.index)):
        # All except Id need to have a space in front
        tmp = Product(data['Id'][i], checkAndReplace(data[' Name'][i]), checkAndReplace(data[' Brand'][i]), checkAndReplace(
            data[' Retailer'][i]), checkAndReplace(data[' Price'][i]), checkAndReplace(data[' InStock'][i]))

        products.append(tmp)

def sortRecordsByPrice():
    # Sort products by price
    # This could be use on python 2.7 because you could compare float and NoneType
    # SoProducts = sorted(products, key=lambda x: x.price, reverse=True)
    
    # For Python3 use:
    SoProducts = sorted({product.price for product in products if product.price is not None})

    # Print on terminal the list to check
    print(SoProducts)

# Basic Route to check if the API is UP
@app.route("/", methods=['GET'])
def runningCheck():
    return "<h1>The API is UP</h1>"

@app.route("/product/", methods=['GET'])
def getById():
    # Get Id from request
    id = request.args.get('id')

    # Loop all array searching for the object, on a real enviroment this would be done on the DB with indexes
    for product in products:
        # If maches
        if id == product.getId():
            # Return the found product
            return jsonify(id=product.id,
                        name=product.name,
                        brand=product.brand,
                        retailer=product.retailer,
                        price=product.price,
                        inStock=product.inStock
                        )
    
    # No product found
    return "<h1>No product with that ID</h1>"

@app.route("/cheapestN/", methods=['GET'])
def getCheapestN():
    # Get n from request
    n = request.args.get('n')

    print(SoProducts[1])

    for i in range(int(n)):
        selectedProducts.append(SoProducts[i])

    return jsonify(eqtls=[e.serialize() for e in selectedProducts])

if __name__ == "__main__":
    print("-> Application started")
    addJSON_Records()
    # addCSV_Records()

    # Creates a new object array, all of them ordered by price
    sortRecordsByPrice()

    print("-> Starting API")
    app.run(host='0.0.0.0')