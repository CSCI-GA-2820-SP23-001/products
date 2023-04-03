# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is a skeleton you can use to start your projects

## Overview

This project template contains starter code for your class project. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. 


## Running the service locally
Before Run, make sure you have install [Docker Desktop](https://www.docker.com/products/docker-desktop), [Visual Studio Code](https://code.visualstudio.com), [Remote Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) first. Then you could clone the repository and then run the following commands:

- ```cd DevOps``
- ```code products```
- Reopen the folder in Dev Container
- Run ```flask run``` command on the terminal
- The service is available at localhost: ```http://localhost:8000```

To run the all the test cases locally, please run the command nosetests. The test cases have 96% code coverage currently.

## Products Service APIs

### Index

GET `/`

### Products Operations


| Endpoint        | Methods | Rule
| --------------- | ------- | --------------------------
| create_products | POST    | /products
| get_products    | GET     | /products/{int:product_id}
| list_products   | GET     | /products
| update_products | PUT     | /products/{int:product_id}
| delete_products | DELETE  | /products/{int:product_id}


## Product Service APIs - Usage

### Create a Product

URL : `http://127.0.0.1:8000/products`

Method : POST

Auth required : No

Permissions required : None

Create a product with json file which included product name, description, price, category, inventory, discount and created date.

Example:

Request Body (JSON)
```
{
  "name": "cheese",
  "available": true,
  "like": 0,
  "color": "YELLOW",
  "size": "M",
  "category": "GROCERIES",
  "create_date": "2023-03-20",
  "last_modify_date": "2023-03-20"
}
```

Success Response : `HTTP_201_CREATED`
```
{
  "available": true,
  "category": "GROCERIES",
  "color": "YELLOW",
  "like": 0,
  "create_date": "2023-03-20",
  "id": 1023,
  "last_modify_date": "2023-03-20",
  "name": "cheese",
  "size": "M"
}
```

### Read/Get a Product

URL : `http://127.0.0.1:8000/products/{int:product_id}`

Method : GET

Auth required : No

Permissions required : None

Gets/Reads a product with id provided in the URL

Example:

Success Response : `HTTP_200_OK`
```
{
  "available": true,
  "category": "GROCERIES",
  "color": "YELLOW",
  "like": 0,
  "create_date": "2023-03-20",
  "id": 1023,
  "last_modify_date": "2023-03-20",
  "name": "cheese",
  "size": "M"
}
```

Failure Response : `HTTP_404_NOT_FOUND`
```
{
  "error": "Not Found",
  "message": "404 Not Found: Product with id '1024' was not found.",
  "status": 404
}
```

### List Products

URL : `http://127.0.0.1:8000/products`

Method : GET

Auth required : No

Permissions required : None

Lists all the Products

Example:

Success Response : `HTTP_200_OK`
```
[
  {
    "available": true,
    "category": "FASHION",
    "color": "BLACK",
    "create_date": "2023-03-20",
    "id": 1024,
    "like": 0,
    "last_modify_date": "2023-03-20",
    "name": "shoes",
    "size": "L"
  },
  {
    "available": true,
    "category": "OTHER",
    "color": "PINK",
    "like": 0,
    "create_date": "2023-03-20",
    "id": 1025,
    "last_modify_date": "2023-03-20",
    "name": "flowers",
    "size": "OTHER"
  },
  {
    "available": false,
    "category": "UNKNOWN",
    "color": "GREEN",
    "like": 0,
    "create_date": "2011-10-15",
    "id": 1021,
    "last_modify_date": "2012-01-05",
    "name": "pot",
    "size": "XL"
  }
]
```

### Update a Product

URL : `http://127.0.0.1:8000/products/{int:product_id}`

Method : PUT

Auth required : No

Permissions required : None

Updates a product with id provided in the URL according to the updated fields provided in the body

Example:

Request Body (JSON)
```
{
  "name": "cheese",
  "available": true,
  "color": "WHITE",
  "size": "S",
  "category": "GROCERIES",
  "create_date": "2023-03-20",
  "last_modify_date": "2023-03-20"
}
```


Success Response : `HTTP_200_OK`
```
{
  "available": true,
  "category": "GROCERIES",
  "color": "YELLOW",
  "create_date": "2023-03-20",
  "id": 1023,
  "last_modify_date": "2023-03-20",
  "name": "cheese",
  "size": "S"
}
```

Failure Response : `HTTP_404_NOT_FOUND`
```
{
  "error": "Not Found",
  "message": "404 Not Found: Product with id '1024' was not found.",
  "status": 404
}
```


### Delete a Product

URL : `http://127.0.0.1:8000/products/{int:product_id}`

Method : DELETE

Auth required : No

Permissions required : None

Deletes a Product with id

Example:

Success Response : `204 NO CONTENT`


### Like a Product

URL : `http://127.0.0.1:8000/products/like/{int:product_id}`

Method : PUT

Auth required : No

Permissions required : None

Updates a product with id provided in the URL according to the updated fields provided in the body

Example:

Request Body (JSON)
```
{
  "name": "cheese",
  "available": true,
  "like": 0,
  "color": "WHITE",
  "size": "S",
  "category": "GROCERIES",
  "create_date": "2023-03-20",
  "last_modify_date": "2023-03-20"
}
```


Success Response : `HTTP_200_OK`
```
{
  "available": true,
  "category": "GROCERIES",
  "color": "WHITE",
  "like": 1,
  "create_date": "2023-03-20",
  "id": 1023,
  "last_modify_date": "2023-03-20",
  "name": "cheese",
  "size": "S"
}
```

Failure Response : `HTTP_404_NOT_FOUND`
```
{
  "error": "Not Found",
  "message": "404 Not Found: Product with id '1024' was not found.",
  "status": 404
}
```


## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
