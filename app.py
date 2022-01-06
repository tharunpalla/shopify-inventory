from flask import Flask, render_template, request, redirect, make_response
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
import pandas
import io

app = Flask(__name__)
client = MongoClient(
    "mongodb+srv://tpalla:shopify@shopify-inventory.gsiky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = client.get_database("shopify")
db_collection = database.inventory_list


@app.route('/')
def index():
    try:
        inventory_list = list(db_collection.find())
        return render_template('index.html', inventory_list=inventory_list)
    except:
        return 'There was an issue getting your inventory'


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        try:
            product_name = request.form['product_name']
            product_category = request.form['product_category']
            product_code = request.form['product_code']
            available_units = request.form['available_units']
            db_collection.insert_one(create_new_inventory(
                product_name, product_category, product_code, available_units))
            return redirect('/')
        except:
            return 'There was an issue adding your inventory'
    else:
        return render_template('add.html')


def create_new_inventory(product_name, product_category, product_code, available_units):
    return {"product_name": product_name,
            "product_category": product_category,
            "product_code": product_code,
            "available_units": available_units,
            "date_created": datetime.utcnow().strftime("%m-%d-%Y")}


@app.route('/delete/<id>')
def delete(id):
    try:
        db_collection.delete_one({'_id': ObjectId(id)})
        return redirect('/')
    except:
        return 'There was a problem deleting that inventory'


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        try:
            product_name = request.form['product_name']
            product_category = request.form['product_category']
            product_code = request.form['product_code']
            available_units = request.form['available_units']
            inventory = create_new_inventory(
                product_name, product_category, product_code, available_units)
            db_collection.update_one({'_id': ObjectId(id)}, {
                                     '$set': inventory
                                     })
            return redirect('/')
        except:
            return 'There was an issue updating your inventory'
    else:
        try:
            inventory = db_collection.find_one({'_id': ObjectId(id)})
            return render_template('update.html', inventory=inventory)
        except:
            return 'There was an issue getting your inventory'


@app.route('/export')
def export():
    mongo_docs = list(db_collection.find())
    docs = pandas.DataFrame(mongo_docs)
    docs.pop("_id")
    excel_file = io.StringIO()
    docs.to_csv(excel_file, sep=',', encoding='utf-8', index=False)
    print(excel_file.getvalue())
    response = make_response(excel_file.getvalue())
    excel_file.close()
    cd = 'attachment; filename=inventory.csv'
    response.headers['Content-Disposition'] = cd
    response.headers['Content-Type'] = 'text/csv'
    return response


if __name__ == "__main__":
    app.run(debug=True)
