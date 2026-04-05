from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date = request.form["date"]
        time = request.form["time"]
        name = request.form["name"]
        menu = request.form["menu"]
        note = request.form["note"]

        with open("reservations.txt", "a", encoding="utf-8") as f:
            f.write(f"{date},{time},{name},{menu},{note}\n")

        return redirect("/")
    
    reservations = []
    with open("reservations.txt", "r", encoding="utf-8") as f:
        for line in f:
            reservations.append(line.strip().split(","))

    reservations.reverse()

    from datetime import date
    today = date.today().isoformat()

    today_reservations = []

    for r in reservations:
        if r[0] == today:
            today_reservations.append(r)

    return render_template("index.html", reservations=reservations, today_reservations=today_reservations)

@app.route("/edit/<int:index>")
def edit(index):
    with open("reservations.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    reservation = lines[index].strip().split(",")

    return render_template("edit.html", reservation=reservation, index=index)

@app.route("/delete/<int:index>")
def delete(index):
    with open("reservations.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines.pop(index)

    with open("reservations.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

    return redirect("/")

@app.route("/update/<int:index>", methods=["POST"])
def update(index):
    date = request.form["date"]
    time = request.form["time"]
    name = request.form["name"]
    menu = request.form["menu"]
    note = request.form["note"]

    new_line = f"{date},{time},{name},{menu},{note}\n"

    with open("reservations.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines[index] = new_line

    with open("reservations.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)