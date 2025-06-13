import psycopg2

def conectar():
    return psycopg2.connect(
        dbname="figurinapp",
        user="admin",
        password="5kzDjoQ1FdiaUZfzBVismFY2SFFQuHsl",
        host="dpg-d1682numcj7s73bdlp3g-a.oregon-postgres.render.com",
        port="5432"
    )
