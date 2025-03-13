import sqlite3;
 
con = sqlite3.connect("C:\sh\safehouse\db.sqlite3")
cursor = con.cursor()
 
# данные для добавления
locker2 = ("92.100.36.69", "SITYMALL Улица главная", 3, 1, 1)
cursor.execute("INSERT INTO lockerslist (ip, location, size, isopen, magnet) VALUES (?, ?, ?, ?, ?)", locker2)
 
con.commit()