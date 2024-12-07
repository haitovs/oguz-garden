from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
import requests

app = Flask(__name__)
CATEGORIES = "http://10.20.110.117:5005/api/categories"


@app.route('/')
def index():
    try:
        # Fetch data from the external API
        response = requests.get(CATEGORIES)
        response.raise_for_status()  # Raise an error for bad responses
        categories = response.json()['categories']
    except requests.exceptions.ite as e:
        categories = []
        print(f"Error fetching data from external API: {e}")

    return render_template('index.html', categories=categories)


@app.route('/admin')
def admin():
    # try:
    #     # Fetch data from the external API
    #     response = requests.get(CATEGORIES)
    #     response.raise_for_status()  # Raise an error for bad responses
    #     categories = response.json()['categories']
    # except requests.exceptions.ite as e:
    #     categories = []
    #     print(f"Error fetching data from external API: {e}")

    # return render_template('admin.html', categories=categories)
    return render_template('admin.html')


@app.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        # Get form data
        title = request.form.get('category')
        print(title)

        # Data to send to the external API
        data = {
            "title": title,
        }

        try:
            # Send a POST request to the external API
            response = requests.post(CATEGORIES, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error posting data to external API: {e}")
            return "Failed to submit report", 500

        return redirect(url_for('index'))

    return render_template('categories.html')


@app.route('/search', methods=['GET'])
def search():
    # Retrieve query parameters
    query = request.args.get('query', '')
    category = request.args.get('category', '')

    # Simulate a search operation (replace with actual logic, such as database queries)
    results = [
        {
            "id": 1,
            "name": "Example Item 1",
            "category": category
        },
        {
            "id": 2,
            "name": "Example Item 2",
            "category": category
        },
    ]

    # Filter results if a query is provided
    if query:
        results = [item for item in results if query.lower() in item["name"].lower()]

    return jsonify({"query": query, "results": results})


if __name__ == '__main__':
    app.run(debug=True)
