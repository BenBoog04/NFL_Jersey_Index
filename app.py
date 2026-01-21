from flask import Flask, render_template, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "dbname": "NFL_Jersey_db",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": "5432",
}

STATE_FULL_TO_ABBR = {
    "ALABAMA": "AL",
    "ALASKA": "AK",
    "ARIZONA": "AZ",
    "ARKANSAS": "AR",
    "CALIFORNIA": "CA",
    "COLORADO": "CO",
    "CONNECTICUT": "CT",
    "DELAWARE": "DE",
    "FLORIDA": "FL",
    "GEORGIA": "GA",
    "HAWAII": "HI",
    "IDAHO": "ID",
    "ILLINOIS": "IL",
    "INDIANA": "IN",
    "IOWA": "IA",
    "KANSAS": "KS",
    "KENTUCKY": "KY",
    "LOUISIANA": "LA",
    "MAINE": "ME",
    "MARYLAND": "MD",
    "MASSACHUSETTS": "MA",
    "MICHIGAN": "MI",
    "MINNESOTA": "MN",
    "MISSISSIPPI": "MS",
    "MISSOURI": "MO",
    "MONTANA": "MT",
    "NEBRASKA": "NE",
    "NEVADA": "NV",
    "NEW HAMPSHIRE": "NH",
    "NEW JERSEY": "NJ",
    "NEW MEXICO": "NM",
    "NEW YORK": "NY",
    "NORTH CAROLINA": "NC",
    "NORTH DAKOTA": "ND",
    "OHIO": "OH",
    "OKLAHOMA": "OK",
    "OREGON": "OR",
    "PENNSYLVANIA": "PA",
    "RHODE ISLAND": "RI",
    "SOUTH CAROLINA": "SC",
    "SOUTH DAKOTA": "SD",
    "TENNESSEE": "TN",
    "TEXAS": "TX",
    "UTAH": "UT",
    "VERMONT": "VT",
    "VIRGINIA": "VA",
    "WASHINGTON": "WA",
    "WEST VIRGINIA": "WV",
    "WISCONSIN": "WI",
    "WYOMING": "WY",
    "DISTRICT OF COLUMBIA": "DC",
}

def normalize_state(value: str) -> str:
    if not value:
        return ""
    v = value.strip()
    if len(v) <= 2:
        return v.upper()
    key = v.upper()
    return STATE_FULL_TO_ABBR.get(key, v)

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html",
        player_no_idx="",
        state_no_idx="",
        player_idx="",
        state_idx="",
        no_idx_single=None,
        no_idx_single_time=None,
        no_idx_join=None,
        no_idx_join_time=None,
        idx_single=None,
        idx_single_time=None,
        idx_join=None,
        idx_join_time=None,
    )

@app.route("/search_no_index", methods=["POST"])
def search_no_index():
    player = (request.form.get("player_no_idx") or "").strip()
    state_raw = (request.form.get("state_no_idx") or "").strip()
    state = normalize_state(state_raw)

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    t0 = time.perf_counter()
    cur.execute(
        """
        SELECT jerseyname, team, jerseytype, jerseysize, jerseyprice, quantitysold
        FROM jersey_sales
        WHERE jerseyname ILIKE %s
        ORDER BY datesold DESC
        LIMIT 5;
        """,
        (player,)  # full-name match, case-insensitive, no wildcards
    )
    no_idx_single = cur.fetchall()
    t1 = time.perf_counter()

    cur.execute(
        """
        SELECT o.orderid, o.shippingstate, o.ordertotal,
               j.jerseyname, j.team, j.jerseyprice, j.quantitysold
        FROM orders o
        JOIN jersey_sales j ON j.orderid = o.orderid
        WHERE j.jerseyname ILIKE %s AND o.shippingstate ILIKE %s
        ORDER BY o.orderdate DESC
        LIMIT 5;
        """,
        (player, state,)
    )
    no_idx_join = cur.fetchall()
    t2 = time.perf_counter()

    cur.close()
    conn.close()

    return render_template(
        "index.html",
        player_no_idx=player,
        state_no_idx=state_raw,
        player_idx=player,
        state_idx=state_raw,
        no_idx_single=no_idx_single,
        no_idx_single_time=(t1 - t0) * 1000.0,
        no_idx_join=no_idx_join,
        no_idx_join_time=(t2 - t1) * 1000.0,
        idx_single=None,
        idx_single_time=None,
        idx_join=None,
        idx_join_time=None,
    )

@app.route("/search_with_index", methods=["POST"])
def search_with_index():
    player = (request.form.get("player_idx") or "").strip()
    state_raw = (request.form.get("state_idx") or "").strip()
    state = normalize_state(state_raw)

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_js_name ON jersey_sales (jerseyname);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_state ON orders (shippingstate);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_js_order ON jersey_sales (orderid);")
    conn.commit()

    t0 = time.perf_counter()
    cur.execute(
        """
        SELECT jerseyname, team, jerseytype, jerseysize, jerseyprice, quantitysold
        FROM jersey_sales
        WHERE jerseyname ILIKE %s
        ORDER BY datesold DESC
        LIMIT 5;
        """,
        (player,)
    )
    idx_single = cur.fetchall()
    t1 = time.perf_counter()

    cur.execute(
        """
        SELECT o.orderid, o.shippingstate, o.ordertotal,
               j.jerseyname, j.team, j.jerseyprice, j.quantitysold
        FROM orders o
        JOIN jersey_sales j ON j.orderid = o.orderid
        WHERE j.jerseyname ILIKE %s AND o.shippingstate ILIKE %s
        ORDER BY o.orderdate DESC
        LIMIT 5;
        """,
        (player, state,)
    )
    idx_join = cur.fetchall()
    t2 = time.perf_counter()

    cur.close()
    conn.close()

    return render_template(
        "index.html",
        player_no_idx=player,
        state_no_idx=state_raw,
        player_idx=player,
        state_idx=state_raw,
        no_idx_single=None,
        no_idx_single_time=None,
        no_idx_join=None,
        no_idx_join_time=None,
        idx_single=idx_single,
        idx_single_time=(t1 - t0) * 1000.0,
        idx_join=idx_join,
        idx_join_time=(t2 - t1) * 1000.0,
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
