#!/usr/bin/python3
# coding=utf-8
""" Main API file """
import json

import pandas as pd
import requests
from flask import Flask, request
from flask_jsonpify import jsonify

from classes import product
from utils.functions import *
from utils.globals import PRODUCTS_FILE, SORTED, SORTED_PRODUCTS, products

app = Flask(__name__)


@app.route("/", methods=["GET"])
def status() -> json:
    """
        Status check on main ('/') route.
        Returns a simple 200, with a message.
    """
    return jsonify({"message": "Application is UP!", "status": 200})


@app.route("/product/<product_id>", methods=["GET"])
def getByProductId(product_id) -> json:
    """
        Returns the product that matches the given ID

        Returns:
            json: product information on a json object
    """

    # Check if product id has been send
    if product_id:
        # Loop all array searching for the object, on a real environment this would be done on the DB with indexes
        for product in products:
            # If maches
            if product_id == product.getProductId():
                return jsonify(
                    productId=product_id,
                    name=product.name,
                    brand=product.brand,
                    retailer=product.retailer,
                    price=product.price,
                    inStock=product.inStock,
                )

    return jsonify({"message": "No product with that ID!", "status": 404})


@app.route("/cheapest/<number_of_products>", methods=["GET"])
def getCheapestN(number_of_products) -> json:
    """
        Finds the N cheapes products on the saved variable

        Returns:
            json: json object with the requested products

    """

    if number_of_products:
        selectedProducts = []

        if not SORTED:
            print("Products need to be sorted")
            SORTED_PRODUCTS = sortRecordsByPrice()

        print(SORTED_PRODUCTS)

        for i in range(int(number_of_products)):
            selectedProducts.append(SORTED_PRODUCTS[i])

        # return jsonify(eqtls=[e.serialize() for e in selectedProducts])
        return jsonify(selectedProducts)

    return jsonify(
        {
            "message": "You need to specify how many products you want to see",
            "status": 400,
        }
    )


if __name__ == "__main__":
    print("-> Application started")
    ##addJSON_Records()
    # addCSV_Records()

    # Creates a new object array, all of them ordered by price

    print("-> Starting API")
    app.run(host="127.0.0.1")
