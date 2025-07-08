import sqlite3

def create_database():
    conn = sqlite3.connect('sensores.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS datos_sensor (
        id INTEGER,
        fecha_hora REAL,
        temperatura REAL,
        presion REAL,
        humedad REAL
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print('Base de datos creada correctamente.')