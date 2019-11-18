#!/usr/bin/python3
import urllib.request
import json

# Products array
products = []

# Checks if the diccionari/object has the key, if not set to 'null'
def keyHasValue(object, key):
    if key in object:
        return object[key]
    else:
        return 'null'

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


# Open the URL of the JSON and save all the info
with urllib.request.urlopen("https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.json") as url:
    data = json.loads(url.read().decode())

for record in data:
    # Create the temporal object
    tmp = Product(keyHasValue(record, 'id'), keyHasValue(record, 'name'), keyHasValue(record, 'brand'), keyHasValue(record, 'retailer'), keyHasValue(record, 'price'), keyHasValue(record, 'in_stock'))

    # Append the object to the list
    products.append(tmp)