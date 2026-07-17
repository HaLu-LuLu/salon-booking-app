from datebase import add_reservation

with open("reservations.txt", "r", encoding="utf-8") as f:
  for line in f:
    data = line.strip().split(",")

    if len(data) == 5:
      date = data[0]
      time = data[1]
      name = data[2]
      menu = data[3]
      note = data[4]

      add_reservation(date, time, name, menu, note)

print("txtの予約データをDBに移しました!")