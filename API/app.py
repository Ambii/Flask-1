import os
from flask import Flask, request, jsonify
import psycopg2
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/init_user',methods=['GET'])
def init_table():
    conn = get_db_connection()
    cur = conn.cursor();

    cur.execute("""
            create table if not exists users(
                    id Serial primary key,
                    name varchar(20) not null,
                    email varchar(150) unique
                );
    """)
    conn.commit()
    cur.close()
    conn.close()

    return "USERS TABLE IS CREATED....!"

@app.route('/user',methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("insert into users(name,email) values(%s , %s) RETURNING id",(name,email))

    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id":user_id, "name":name, "email":email})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
