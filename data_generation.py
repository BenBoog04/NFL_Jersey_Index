import psycopg2
import csv
import os

# database configuration
DB_CONFIG = {
    'dbname': 'NFL_Jersey_db',
    'user': 'postgres',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

def load_all_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # clear tables
    cursor.execute("TRUNCATE jersey_sales RESTART IDENTITY CASCADE;")
    cursor.execute("TRUNCATE orders RESTART IDENTITY CASCADE;")
    conn.commit()

    # CSV paths (relative to THIS FILE)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    orders_path = os.path.join(BASE_DIR, 'orders.csv')
    sales_path = os.path.join(BASE_DIR, 'jersey_sales.csv')

    # -------- load orders.csv --------
    with open(orders_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO orders (
                    orderid, customername, customeremail, orderdate,
                    shippingaddress, shippingcity, shippingstate,
                    shippingzip, paymentmethod, ordertotal
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                int(row['orderid']),
                row['customername'],
                row['customeremail'],
                row['orderdate'],
                row['shippingaddress'],
                row['shippingcity'],
                row['shippingstate'],
                row['shippingzip'],
                row['paymentmethod'],
                float(row['ordertotal'])
            ))
    conn.commit()

    # -------- load jersey_sales.csv --------
    with open(sales_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO jersey_sales (
                    jerseyid, orderid, jerseyname, jerseynumber, team,
                    jerseytype, jerseyyear, jerseysize, jerseyprice,
                    quantitysold, datesold
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                int(row['jerseyid']),
                int(row['orderid']),
                row['jerseyname'],
                int(row['jerseynumber']),
                row['team'],
                row['jerseytype'],
                int(row['jerseyyear']),
                row['jerseysize'],
                float(row['jerseyprice']),
                int(row['quantitysold']),
                row['datesold']
            ))
    conn.commit()

    cursor.close()
    conn.close()


if __name__ == '__main__':
    try:
        load_all_data()
        print("Data load complete.")
    except Exception as e:
        print(f"Error: {e}")
