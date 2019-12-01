from flask import Flask
from flask import jsonify
from flask_pymongo import PyMongo
from Constants.constants import ConstantVariables

app = Flask(__name__)
app.config["MONGO_URI"] = ConstantVariables.MONGO_PATH.value + ConstantVariables.DB_NAME.value

mongo = PyMongo(app)


@app.route('/quotes', methods=['GET'])
def get_all_quotes():
    quotes = mongo.db.quotes
    output = []
    for quote in quotes.find():
        quote.pop("_id")
        output.append(quote)
    return jsonify({'result': output})


if __name__ == '__main__':
    app.run()

