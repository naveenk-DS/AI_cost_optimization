import psycopg

conn = psycopg.connect(
    host="192.168.29.13",
    port=5433,
    dbname="postgres",
    user="postgres",
    password="Naveen@677",
)

print("Connected successfully!")

with conn.cursor() as cursor:
    cursor.execute("SELECT version();")
    result = cursor.fetchone()
    print(result[0])

conn.close()