# Products-API

## Task

### Description

You have been provided with 2 files of varying sizes, qualities, contents and
formats. These files contain a list of randomly generated products from various
brands and retailers.

Your task is to write a small command line application that on startup ingests this
data as quickly and efficiently as possible. For the sake of keeping this test short
it is fine to load it into memory, you do not need to use a database.

Following this your application should start an API server with two endpoints:

- An endpoint to retrieve a single product by its `productId`
- An endpoint that retrieves the N cheapest products (where N is a configurable number that the client can specify)

Your API endpoints should return the product data as JSON with the following fields:

- `productId` as a string
- `name` as a string
- `brand` as a string
- `retailer` as a string
- `price` as a float
- `in_stock` as a boolean

Any fields that aren't available for a product should be returned as `null`.

The first file ([products.csv.gz](products.csv.gz)) is in the CSV file format and
compressed with GZIP.

The second file ([products.json](https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/python-software-developer/products.json))
is in the JSON file format and is located in an AWS S3 bucket. Your application
should download this once when it starts up.

### Implementation

You are free to implement this using whatever technologies you feel appropriate
although as this is a primarily Python focussed role so it would be nice to see
that used.

There is no time limit on how long you can spend on the task but around 2 to 3
hours is probably a good guide. As mentioned above any further improvements or
ideas you have can be discussed in the interview.

Your submission will be judged on the overall quality of the solution with
various factors such as the following considered:

- Presentation
- Performance
- Simplicity
- Readability
- Reliability
- Scalability
- Extensibility
- Some other words that end in 'ility'


### Requirements

The application needs the following external packages to work:

* Flask
* Pandas

### How to run it

Clone the repository on your computer

````
git clone https://github.com/sWallyx/Products-API.git
````

Enter into the folder Products-API

````
cd Products-API
````

Run the productAPI.py file with python3

````
python3 productAPI.py
````

First the application will load all the info into the memory, and then the API will start in http://0.0.0.0:5000