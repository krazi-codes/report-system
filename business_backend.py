# Business Backend System

## Overview
This Python script implements a basic backend system for managing data of a small business. It includes data management, sorting, filtering, searching, and basic API endpoints using Flask.

## Requirements
- Flask

## Install Flask
```bash
pip install Flask
```

## Data Management
This backend will manage data in a simple list. For real applications, consider using a database.

```python
class Business:
    def __init__(self):
        self.data = []

    def add_item(self, item):
        self.data.append(item)

    def get_items(self):
        return self.data

    def filter_items(self, **kwargs):
        filtered = self.data
        for key, value in kwargs.items():
            filtered = [item for item in filtered if item.get(key) == value]
        return filtered

    def sort_items(self, key):
        return sorted(self.data, key=lambda x: x[key])

    def search_items(self, query):
        return [item for item in self.data if query.lower() in item['name'].lower()]
```

## Basic API Endpoints

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
business = Business()

@app.route('/add', methods=['POST'])
def add_item():
    item = request.json
    business.add_item(item)
    return jsonify({'message': 'Item added successfully'}), 201

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(business.get_items())

@app.route('/filter', methods=['GET'])
def filter_items():
    filters = request.args.to_dict()
    filtered_items = business.filter_items(**filters)
    return jsonify(filtered_items)

@app.route('/search', methods=['GET'])
def search_items():
    query = request.args.get('query')
    results = business.search_items(query)
    return jsonify(results)

@app.route('/sort', methods=['GET'])
def sort_items():
    key = request.args.get('key')
    sorted_items = business.sort_items(key)
    return jsonify(sorted_items)

if __name__ == '__main__':
    app.run(debug=True)
```

## Running the Application
Save this script to a file named `business_backend.py` and run it using:
```bash
python business_backend.py
```

## API Testing
You can test the API using tools like Postman or CURL to interact with the endpoints and manage your business data efficiently.