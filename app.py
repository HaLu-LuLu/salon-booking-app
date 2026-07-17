from datetime import date, datetime
import calendar
from flask import Flask, render_template, request, redirect
from datebase import init_db, add_reservation, get_reservations, delete_reservation, update_reservation, get_menu_stats, get_total_sales, get_staff_stats, get_staff_sales, get_monthly_sales, get_reservation_dates
app = Flask(__name__)

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    
    reservations = get_reservations()
    menu_stats = get_menu_stats()
    total_sales = get_total_sales()
    staff_stats = get_staff_stats()
    staff_sales = get_staff_sales()
    monthly_sales = get_monthly_sales()
    reservation_dates = get_reservation_dates()

    current_date = datetime.today()

    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)

    if year is None:
        year = current_date.year

    if month is None:
        month = current_date.month

    if month < 1:
        month = 12
        year -= 1

    elif month > 12:
        month = 1
        year += 1

    cal = calendar.monthcalendar(year, month)

    keyword = request.args.get("keyword", "")

    selected_date = request.args.get("selected_date", "")
    selected_reservations = []

    today = date.today().isoformat()
    today_reservations = []
    future_reservations = []
    past_reservations = []

    for i, r in enumerate(reservations):

        if keyword and not (keyword.lower() in r[3].lower() or keyword.lower() in r[4].lower()):
            continue

        if r[1] == today:
            today_reservations.append((i, r))
        
        elif r[1] > today:
            future_reservations.append((i, r))

        else:
            past_reservations.append((i, r))

        if selected_date and r[1] == selected_date:
            selected_reservations.append((i,r))

    if keyword and len(today_reservations) == 0 and len(future_reservations) == 0 and len(past_reservations) == 0:
        message = "該当する予約はありません"   

    if request.method == "POST":
        date_value = request.form["date"]
        time = request.form["time"]
        name = request.form["name"]
        menu = request.form["menu"]
        staff = request.form["staff"]
        note = request.form["note"]

        if not date_value or not time or not name or not menu or not staff:
            return render_template("index.html", error="入力してください",  today_reservations=today_reservations, future_reservations=future_reservations, past_reservations=past_reservations, keyword=keyword, message=message, form_date={"date": "", "time": "", "name": "", "menu": "", "note": ""}, menu_stats=menu_stats, total_sales=total_sales, staff_stats=staff_stats, staff_sales=staff_sales, monthly_sales=monthly_sales, cal=cal, year=year, month=month, reservation_dates=reservation_dates, selected_reservations=selected_reservations, selected_date=selected_date, today=today) 

        add_reservation(date_value, time, name, menu, staff, note)

        return redirect("/")
    
    return render_template("index.html", today_reservations=today_reservations, future_reservations=future_reservations, past_reservations=past_reservations, keyword=keyword, message=message, form_date={"date": "", "time": "", "name": "", "menu": "", "note": ""}, menu_stats=menu_stats,total_sales=total_sales, staff_stats=staff_stats, staff_sales=staff_sales, monthly_sales=monthly_sales, cal=cal, year=year, month=month, reservation_dates=reservation_dates, selected_reservations=selected_reservations, selected_date=selected_date, today=today)

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):

    reservations = get_reservations()

    reservation = None

    for r in reservations:
        if r[0] == index:
            reservation = r
            break
    if reservation is None:
        return redirect("/")

    return render_template("edit.html", reservation=reservation, index=index)

@app.route("/delete/<int:index>")
def delete(index):
    delete_reservation(index)

    return redirect("/")

@app.route("/update/<int:index>", methods=["POST"])
def update(index):
    date_value = request.form["date"]
    time = request.form["time"]
    name = request.form["name"]
    menu = request.form["menu"]
    staff = request.form["staff"]
    note = request.form["note"]

    update_reservation(index, date_value, time, name, menu, staff, note)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)