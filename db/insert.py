import pymysql
import os

# Connect to the database
mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="000000",
  database="pdbqtDB"
)

# Create cursor
mycursor = mydb.cursor()

# Specify the directory you want to read from
dir_path = '~/output'

# Convert the tilde in the path to the user's home directory
dir_path = os.path.expanduser(dir_path)

# Get a list of all files in the directory
files = os.listdir(dir_path)

# For each file in the directory
for filename in files:
    # If the file has the .pdbqt extension
    if filename.endswith(".pdbqt"):
        # Read the file
        with open(os.path.join(dir_path, filename), 'r') as file:
            pdbqt_text = file.read()
        
        # Insert file content to database
        sql = "INSERT INTO pdbqtData (fileName, pdbqtText) VALUES (%s, %s)"
        val = (filename, pdbqt_text)
        mycursor.execute(sql, val)

# Commit the transaction
mydb.commit()

print(len(files), "records inserted.")

# Close the connection
mydb.close()