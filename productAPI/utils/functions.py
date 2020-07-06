""" File with many util functions """
import json

import pandas as pd
import requests

from productAPI.classes.product import Product
from productAPI.utils.globals import (
    PRODUCTS_FILE,
    JSON_URL,
    # SORTED_PRODUCTS,
    products,
)


def keyHasValue(customObject: object, key: str):
    """
        Checks if the dictionary/object has the key, if not set to None

        Args:
            customObjects {object}: Object to check
            key {str}: Key to be checked

        Returns:
            object value or null
    """
    if key in customObject:
        if customObject[key] is not None:
            if customObject[key] != "":
                if key == "price":
                    return float(customObject[key])
                return customObject[key]

            return None
        return None
    return None


def checkAndReplace(value: str) -> str:
    """
        Checks if the entering value has quotes on it, and removes them

        Args:
            value {str}: Value to be formated

        Returns:
            formated value without quotes
    """
    return value.replace('"', "")


def nonesorter(value):
    if not value:
        return ""
    return value


def addCSV_Records():
    """
        Read the content of the CSV using pandas read_csv. Then it saves all records on a Product array
    """
    # Print message to terminal
    print("Reading content from CSV")

    # Get the data from the CSV
    data = pd.read_csv(PRODUCTS_FILE, compression="gzip", encoding="utf-8-sig")

    # Get Data Length
    for i in range(len(data.index)):
        # All except Id need to have a space in front
        tmp = Product(
            data["Id"][i],
            checkAndReplace(data[" Name"][i]),
            checkAndReplace(data[" Brand"][i]),
            checkAndReplace(data[" Retailer"][i]),
            checkAndReplace(data[" Price"][i]),
            checkAndReplace(data[" InStock"][i]),
        )

        products.append(tmp)


def sortRecordsByPrice():
    """
        Sort products by price. This could be use on python 2.7
        because you could compare float and NoneType
        sorted(products, key=lambda x: x.price, reverse=True)
    """

    # return sorted({product.price for product in products if product.price is not None})
    # products.sort(key=nonesorter)
    return sorted(products, key=lambda x: (x.price is None, x.price))


def addJSON_Records():
    """
        Takes the JSON file from URL and decodes de content to be able to work
        with it. Then it saves all records on a Product array.
    """
    # Print message to terminal
    print("Reading content from external JSON")

    # Open the URL of the JSON and save all the info
    with requests.get(JSON_URL) as response:
        data = json.loads(response.text)

    for record in data:
        # Create the temporal object
        tmp = Product(
            keyHasValue(record, "id"),
            keyHasValue(record, "name"),
            keyHasValue(record, "brand"),
            keyHasValue(record, "retailer"),
            keyHasValue(record, "price"),
            keyHasValue(record, "in_stock"),
        )

        # Append the object to the list
        products.append(tmp)
