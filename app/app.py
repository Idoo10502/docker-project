import os
import pymysql
from fastapi import FastAPI, HTTPException

app = FastAPI()

def get_connection():
    return pymysql.connect(
        host=os.environ["HOST_DB"],
        user=os.environ["USER_DB"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/")
def root():
    return {"message": "Welcome to the items API!"}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/items")
def get_items():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items")
            return cursor.fetchall()
    finally:
        conn.close()
        
@app.post("/items/{name}")
def add_item(name: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO items (name) VALUES (%s)", (name,))
            conn.commit()
            new_id = cursor.lastrowid
            return {"id": new_id, "name": name}
    finally:
        conn.close()

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Item not found")
        return {"deleted": item_id}
    finally:
        conn.close()



