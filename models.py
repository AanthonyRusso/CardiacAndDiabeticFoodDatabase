import db
import sqlite3

def add_food(name,category,carbs,GI,GINote,sodium,SodiumStatus,calories,ServingSize):
    con = db.get_connection()
    cur = con.cursor()

    cur.execute("INSERT INTO Food(name,category,carbs,GI,GINote,sodium,SodiumStatus,calories, ServingSize) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (name, category, carbs, GI, GINote, sodium, SodiumStatus, calories, ServingSize))

    con.commit()
    con.close()

def update_food(original_name, name, category, carbs, GI, GINote, sodium, SodiumStatus, calories, ServingSize):
    con = db.get_connection()
    cur = con.cursor()
    cur.execute("UPDATE Food SET name=?, category=?, carbs=?, GI=?, GINote=?, sodium=?, SodiumStatus=?, calories=?, ServingSize=? WHERE name=?",
                (name, category, carbs, GI, GINote, sodium, SodiumStatus, calories, ServingSize, original_name))
    con.commit()
    con.close()

def delete_food(name):
    con = db.get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM Food WHERE name=?", (name,))
    con.commit()
    con.close()

def get_all_foods():
    con = db.get_connection()
    cur = con.cursor()

    cur.execute("SELECT name FROM Food")
    rows = cur.fetchall()

    con.close()
    
    return rows


def find_food_info(food_name):
    con = db.get_connection()
    cur = con.cursor()

    cur.execute("SELECT * FROM Food WHERE name = ?", (food_name,))

    result = cur.fetchone()
    con.close()

    return result
