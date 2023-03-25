
#%%
# Importing required modules
from flask import Flask, jsonify, current_app, request
from sqlalchemy import create_engine
from flask_restx import Api, Namespace, Resource

user = "root"
passw = "%TGBnhy6"
host = "34.175.28.179"
database = "myflaskDB"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = host

# Creating the api V1
api = Api(app, version = '1.0',
    title = 'customers articile and transaction API',
    description = """
        API endpoints used to communicate data customers, articles 
        and  transaction sample
        between MySQL database and streamlit
        """,
    contact = "",
    endpoint = "/api/v1"
)


def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()


customers = Namespace(
    'customers',
    description = 'All the customers',
    path='/api/v1')
api.add_namespace(customers)


articles  = Namespace(
    'articles ',
    description = 'All the articles',
    path='/api/v2')
api.add_namespace(articles )

transactions_sample = Namespace(
    'transactions_sample',
    description = 'All the transactions_sample',
    path='/api/v3')
api.add_namespace(transactions_sample )


@customers.route("/customers")
class get_all_customers(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM customers
            LIMIT 100;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@customers.route("/customer/<string:id>")
@customers.doc(params = {'id': 'The ID of the beer'})
class select_user1(Resource):

    @api.response(404, "BEER not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM customers
            WHERE id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
    

@articles.route("/articles")
class get_all_articiless(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM articles
            LIMIT 10;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@articles.route("/articles/<string:id>")
@articles.doc(params = {'id': 'The ID of the articles'})
class select_user2(Resource):

    @api.response(404, " articles not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM articles
            WHERE id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})


@transactions_sample.route("/transactions_sample")
class get_all_transaction(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM transactions_sample
            LIMIT 10;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@transactions_sample.route("/transactions_sample/<string:id>")
@transactions_sample.doc(params = {'id': 'The ID of the brewery'})
class select_user3(Resource):

    @api.response(404, " transactions_sample not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM transactions_sample
            WHERE id = '{0}';""".format(id)
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
if __name__ == '__main__':
    app.run(
        host = '0.0.0.0', 
        port = 8080,debug = True ,use_reloader=False)
# %%
