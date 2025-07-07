from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('sensores.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/datos', methods=['GET'])
def obtener_todos():
    conn = get_db_connection()
    datos = conn.execute('SELECT * FROM datos_sensor').fetchall()
    conn.close()
    return jsonify([dict(row) for row in datos])

@app.route('/datos/filtro', methods=['GET'])
def obtener_filtrados():
    temperatura_min = request.args.get('temperatura_min', type=float)
    conn = get_db_connection()
    datos = conn.execute('SELECT * FROM datos_sensor WHERE temperatura > ?', (temperatura_min,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in datos])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)