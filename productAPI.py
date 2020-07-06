#!/usr/bin/python3
# coding=utf-8
""" Main API file """
import json

import pandas as pd
import requests
from flask import Flask, request
from flask_jsonpify import jsonify

from utils.functions import *
from utils.globals import *

app = Flask(__name__)

# Product class to store the products, it will need to be on the Database
class Product:

    # Init the object
    def __init__(self, productId: str, name: str, brand: str, retailer: str, price: float, inStock: str):
        self.productId = productId
        self.name = name
        self.brand = brand
        self.retailer = retailer
        self.price = price
        self.inStock = inStock

    # productId getter
    def getProductId(self) -> str:
        return self.productId


# Name: addJSON_Records
# Description: Takes the JSON file from URL and decodes de content to be able to work with it. Then it saves all records on a Product array.
# IN:
# OUT:
def addJSON_Records():
    # Print message to terminal
    print('Reading content from external JSON')

    JSON_URL = 'https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.json'
    # Open the URL of the JSON and save all the info
    with requests.get(JSON_URL) as response:
        data = json.loads(response.text)

    for record in data:
        # Create the temporal object
        tmp = Product(
            keyHasValue(record, 'id'),
            keyHasValue(record, 'name'),
            keyHasValue(record, 'brand'),
            keyHasValue(record, 'retailer'),
            keyHasValue(record, 'price'),
            keyHasValue(record, 'in_stock'),
        )

        # Append the object to the list
        products.append(tmp)


# Name: addCSV_Records
# Description: Read the content of the CSV using pandas read_csv. Then it saves all records on a Product array
# IN:
# OUT:
def addCSV_Records():
    # Print message to terminal
    print('Reading content from CSV')

    # Get the data from the CSV
    data = pd.read_csv(PRODUCTS_FILE, compression='gzip', encoding='utf-8-sig')

    # Get Data Length
    for i in range(len(data.index)):
        # All except Id need to have a space in front
        tmp = Product(
            data['Id'][i],
            checkAndReplace(data[' Name'][i]),
            checkAndReplace(data[' Brand'][i]),
            checkAndReplace(data[' Retailer'][i]),
            checkAndReplace(data[' Price'][i]),
            checkAndReplace(data[' InStock'][i]),
        )

        products.append(tmp)


def sortRecordsByPrice():
    # Sort products by price
    # This could be use on python 2.7 because you could compare float and NoneType
    # SortedProducts = sorted(products, key=lambda x: x.price, reverse=True)

    # For Python3 use:
    SortedProducts = sorted(
        {product.price for product in products if product.price is not None}
    )

    SORTED = True

# Basic Route to check if the API is UP
@app.route('/', methods=['GET'])
def status() -> json:
    return jsonify({'message': 'Application is UP!', 'status': 200})


@app.route('/product/', methods=['GET'])
def getByProductId() -> json:
    # Get Id from request
    productId = request.args.get('productId')

    # Check if product id has been send
    if productId:

        # Loop all array searching for the object, on a real environment this would be done on the DB with indexes
        for product in products:
            # If maches
            if productId == product.getProductId():
                # Return the found product
                return jsonify(
                    productId=product.productId,
                    name=product.name,
                    brand=product.brand,
                    retailer=product.retailer,
                    price=product.price,
                    inStock=product.inStock,
                )

    return jsonify({'message': 'No product with that ID!', 'status': 404})


@app.route('/cheapest/', methods=['GET'])
def getCheapestN() -> json:
    """
        Finds the N cheapes products on the saved variable

        Returns:
            json: json object with the requested products

    """
    number_of_products = request.args.get('number')

    if number_of_products:

        if not SORTED:
            sortRecordsByPrice()

        for i in range(int(number_of_products)):
            selectedProducts.append(SortedProducts[i])

        return jsonify(eqtls=[e.serialize() for e in selectedProducts])

    return jsonify({'message': 'You need to specify how many products you want to see', 'status': 400}) 


if __name__ == '__main__':
    print('-> Application started')
    addJSON_Records()
    # addCSV_Records()

    # Creates a new object array, all of them ordered by price
    

    print('-> Starting API')
    app.run(host='127.0.0.1')
