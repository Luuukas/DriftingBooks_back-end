import mysql.connector

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
  #Get database table
  # db_cursor.execute("SHOW TABLES")
  # for table in db_cursor:
  #   print(table)

def delete_stars_table(uid):
  db_cursor = db_connection.cursor()
  db_cursor.execute("DROP TABLE ust_%d" % (uid))
  # db_cursor.execute("SHOW TABLES")
  # for table in db_cursor:
  #   print(table)

def insert_stars_table(uid, bid, isself):
  db_cursor = db_connection.cursor()
  db_cursor.execute("INSERT INTO ust_%d(bid,isself) VALUES(%d,%d)" % (uid, bid,isself))
  db_connection.commit()
  # print(db_cursor.rowcount, "Record Inserted")

def select_stars_table(uid):
  db_cursor = db_connection.cursor()
  db_cursor.execute("SELECT * FROM ust_%d" % (uid))
  bids = []
  for record in db_cursor:
    bids.append([record[1],record[2]])
  return {
    "bottles" : bids
  }