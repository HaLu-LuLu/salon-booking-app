import sqlite3

DB_NAME = "reservations.db"

def init_db():
  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()

  cur.execute("""
      CREATE TABLE IF NOT EXISTS reservations (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          date TEXT NOT NULL,
          time TEXT NOT NULL,
          name TEXT NOT NULL,
          menu TEXT NOT NULL,
          note TEXT
    )
""")
  conn.commit()
  conn.close()

def add_reservation(date, time, name, menu, staff, note):
  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()

  cur.execute("""
      INSERT INTO reservations 
      (date, time, name, menu, staff, note)
      VALUES (?, ?, ?, ?, ?, ?)
""", (date, time, name, menu,  staff, note))
  
  conn.commit()
  conn.close()

def get_reservations():
  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()

  cur.execute("""
      SELECT id, date, time, name, menu, staff, note
      FROM reservations
      ORDER BY date, time
""")
  
  reservations = cur.fetchall()

  conn.close()

  return reservations

def delete_reservation(id):
  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()

  cur.execute(
      "DELETE FROM reservations WHERE id = ?",
      (id,)
  )

  conn.commit()
  conn.close()

def update_reservation(id, date, time, name, menu, staff, note):
  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()

  cur.execute("""
      UPDATE reservations
      SET date = ?, time = ?, name = ?, menu = ?, staff = ?,note = ?
      WHERE id = ?
  """, (date, time, name, menu, staff, note, id))

  conn.commit()
  conn.close()

def get_menu_stats():
  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()

  cur.execute("""
      SELECT menu, COUNT(*)
      FROM reservations
      GROUP BY menu
      ORDER BY COUNT(*) DESC
  """)

  stats = cur.fetchall()
  conn.close()

  return stats

def get_staff_stats():
  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()

  cur.execute("""
      SELECT staff, COUNT(*)
      FROM reservations
      GROUP BY staff
      ORDER BY COUNT(*) DESC
  """)

  stats = cur.fetchall()
  conn.close()

  return stats

def get_total_sales():
  prices = {
    "カット": 4000,
    "カラー": 6000,
    "パーマ": 8000,
    "カット+カラー": 10000,
    "カット+パーマ": 12000,
  }

  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()

  cur.execute("SELECT menu FROM reservations")
  menus = cur.fetchall()

  total = 0

  for menu in menus:
    menu_name = menu[0]
    total += prices.get(menu_name, 0)

  conn.close()

  return total

def get_staff_sales():
  prices = {
    "カット": 4000,
    "カラー": 6000,
    "パーマ": 8000,
    "カット+カラー": 10000,
    "カット+パーマ": 12000,
  }

  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()

  cur.execute("""
        SELECT staff, menu
        FROM reservations
  """)
  rows = cur.fetchall()

  staff_sales = {}

  for staff, menu in rows:
      if staff is None:
        staff = "未設定"

      staff_sales[staff] = staff_sales.get(staff, 0) + prices.get(menu, 0)

  conn.close()

  return staff_sales.items()

def get_monthly_sales():
  prices = {
    "カット": 4000,
    "カラー": 6000,
    "パーマ": 8000,
    "カット+カラー": 10000,
    "カット+パーマ": 12000,
  }

  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()

  cur.execute("""
        SELECT date, menu
        FROM reservations
  """)

  rows = cur.fetchall()

  monthly_sales = {}

  for date, menu in rows:
    month = date[:7]

    monthly_sales[month] = (
      monthly_sales.get(month, 0)
      + prices.get(menu, 0)
    )

  conn.close()

  return monthly_sales.items()

def  get_reservation_dates():
  conn = sqlite3.connect(DB_NAME)
  cur = conn.cursor()

  
  cur.execute("""
        SELECT date
        FROM reservations
  """)

  dates = [row[0] for row in cur.fetchall()]

  conn.close()

  return dates