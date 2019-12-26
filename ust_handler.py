import mysql.connector
import bottle_handler

db_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Chong516",
  database="drifting"
)

def create_stars_table(uid):
  db_cursor = db_connection.cursor()
  #Here creating database table as employee with primary key
  db_cursor.execute("CREATE TABLE ust_%d(sid INT AUTO_INCREMENT PRIMARY KEY, bid INT(11), isself INT(1))" % (uid))
  db_connection.commit()
  db_cursor.close ()
  #Get database table
  # db_cursor.execute("SHOW TABLES")
  # for table in db_cursor:
  #   print(table)

def delete_stars_table(uid):
  db_cursor = db_connection.cursor()
  db_cursor.execute("DROP TABLE ust_%d" % (uid))
  db_connection.commit()
  db_cursor.close ()
  # db_cursor.execute("SHOW TABLES")
  # for table in db_cursor:
  #   print(table)

def insert_star(uid, bid, isself):
  db_cursor = db_connection.cursor()
  db_cursor.execute("INSERT INTO ust_%d(bid,isself) VALUES(%d,%d)" % (uid, bid,isself))
  db_connection.commit()
  db_cursor.close ()
  # print(db_cursor.rowcount, "Record Inserted")

def remove_star(uid, bid):
  db_cursor = db_connection.cursor()
  db_cursor.execute("DELETE FROM ust_%d WHERE bid=%d" % (uid, bid))
  db_connection.commit()
  db_cursor.close ()


def select_stars_table(uid):
  db_cursor = db_connection.cursor()
  db_cursor.execute("SELECT * FROM ust_%d" % (uid))
  bids = []
  record = db_cursor.fetchone();
  while record:
    print(record[1])
    res = bottle_handler.get_bottle(record[1])
    file_object = open(res["infos"][4])
    file_context = file_object.read()
    bids.append({
      "botid" : res["infos"][0],
      "bookname" : res["infos"][1],
      "writer" : res["infos"][2],
      "press" : res["infos"][3],
      "description" : file_context,
      "photourls" : res["infos"][5],
      "ispicked" : (res["infos"][7]!=0),
      "isdonated" : (res["infos"][7]!=-1),
      "donateTo" : (res["infos"][7] if res["infos"][7]<0 else 1),
      "uploaddatetime" : res["infos"][8].strftime("%Y-%m-%d %H:%M:%S"),
      "state" : res["infos"][9],
      "belong" : record[2]
    })
    record = db_cursor.fetchone();
  db_connection.commit()
  db_cursor.close ()
  return {
    "msg" : "success",
    "bottles" : bids
  }