# Working instance:

This app is available
here: [ec2-15-229-250-69.sa-east-1.compute.amazonaws.com:5000](ec2-15-229-250-69.sa-east-1.compute.amazonaws.com:5000)

# API Documentation

## Base URL

All endpoints are prefixed with the base URL:
`https://ec2-15-229-250-69.sa-east-1.compute.amazonaws.com:5000/api/v1`

## Endpoints

### 1. Log in

**Endpoint:** `POST /login`

**Description:** This endpoint allows to perform log in.

**Request:**

- **Headers:**
    - `Content-Type`: `application/json`

- **Body Parameters:**
    - `username` (string): The name of the user. (required)
    - `password` (string): User's password. (optional)

**Response:**

- **200 OK**
    - `id` (integer): The unique identifier.
    - `username` (string): The name of the user.
    - `password` (string): User's password.
    - `active` (boolean): User status.

- **Error Responses:**
    - `404 Not Found`: If user not found or password is incorrect.

### 2. Log out

**Endpoint:** `POST /logout`

**Description:** This endpoint allows to perform log out.

**Request:**

- **Headers:**
    - `Content-Type`: `application/json`

**Response:**

- **200 OK**
    - `message` (string): Status message.

### 3. Perform calculation

**Endpoint:** `POST /do-math`

**Description:** This endpoint allows user make calculations.

**Request:**

- **Headers:**
    - `Content-Type`: `application/json`

- **Body Parameters:**
    - `operation` (string): Type of one of predefined operations: ***addition***, ***subtraction***,
      ***multiplication***, ***division***, ***square_root*** or ***random_string***. (required)
    - `param1` (integer): First parameter for calculation. (required for all the operations except of
      ***random_string***)
    - `param2` (integer): Second parameter for calculation. (required for all the operations except of ***square_root***
      and ***random_string***)

**Response:**

- **200 OK**
    - `result` (string): Result of calculations.

- **Error Responses:**
    - `401 Unauthorized`: In case of user not logged in.
    - `409 Conflict`: In case of missing parameters, wrong attribute types or exceeding credit balance.

### 4. User history

**Endpoint:** `POST /my-records`

**Description:** This endpoint returns historical data of user's calculations.

**Request:**

- **Headers:**
    - `Content-Type`: `application/json`

- **Body Parameters:**
    - `sort_col` (string): Column name to sort records. Possible values: ***date***, ***amount***, ***user_balance***,
      ***operation_id*** or ***operation_response***. (optional) Default: ***date***
    - `page_size` (integer): Number of records per page. (optional) Default: ***20***
    - `page_num` (integer): Page number. (optional) Default: ***1***

**Response:**

- **200 OK**
    - `records` (array): A list of items that match the filter.
        - Each record in the list contains:
            - `id` (integer): The unique identifier of the record.
            - `operation_id` (integer): The unique identifier of the operation.
            - `operation` (string): Name of the operation.
            - `user_id` (integer): The unique identifier of the user.
            - `amount` (integer): Cost of the operation.
            - `user_balance` (integer): User's balance after the operation.
            - `operation_response` (string): Given response.
            - `date` (timestamp): Date when operation was performed.
    - `pageNumber` (integer): Current page number.
    - `pageSize` (integer): Applied page size.
    - `totalRecords` (integer): Total records count.
    - `sortColumn` (string): Applied column to sort.

- **Error Responses:**
    - `400 Bad Request`: In case of any undefined errors.
    - `401 Unauthorized`: In case of user not logged in.

# Run on your local machine

have Python installed

install project libraries:

        pip3 install -r requirements.txt

run *run_app.py* file to start the App

        python3 run_app.py