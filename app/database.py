import sqlite3
from .schemas import ShipmentCreate, ShipmentUpdate
from typing import Any
from contextlib import contextmanager


class Database:
    def __init__(self):
        pass

    
    def __enter__(self):
        print("Connecting to database")
        self.connect_to_db("shipments.db")
        self.create_table('shipment')
        return self

       
    def connect_to_db(self, db_name:str):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
    
    def create_table(self,name:str):
        self.cur.execute(f"""
         CREATE TABLE IF NOT EXISTS {name} (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )
            """)
    
    def create(self, shipment:ShipmentCreate):
         self.cur.execute('SELECT MAX(id) FROM shipment')
         result = self.cur.fetchone()[0]
         new_id = result + 1 if result is not None else 1
         values = {"id":new_id, **shipment.model_dump(mode="json",exclude={"id"})}
         self.cur.execute(
             '''INSERT INTO shipment(id, content, weight, status) 
             VALUES(:id, :content, :weight, :status)''',
             {**values}
         )
         self.conn.commit()
         return values
    
    def get(self, id:int) -> dict[str, Any] | None:
        self.cur.execute('SELECT * FROM shipment WHERE id=?',(id, ))
        entry = self.cur.fetchone()
        return dict(entry) if entry else None
    
    def get_all(self) -> list[dict[str,Any]]:
        self.cur.execute('SELECT * FROM shipment')
        return [dict(row) for row in self.cur.fetchall()]
    
    def update(self, id:int, shipment:ShipmentUpdate) -> int:
        self.cur.execute('''
         UPDATE shipment
            SET content = :content, weight = :weight, status = :status
            WHERE id = :id
      ''',shipment.model_dump(mode="json"))
        self.conn.commit()
        return self.get(id)

    def delete(self, id):
        self.cur.execute('DELETE FROM shipment WHERE id = ?', (id, ))
        self.conn.commit()
        return self.cur.rowcount > 0

    def close(self):
        self.conn.close()
    
    # def __exit__(self, *args):
    #     print("Closing database connection")
    #     self.close()

# with Database() as db:
#     print(db.get(4))

@contextmanager
def managed_db():
    db = Database()
    db.connect_to_db("shipments.db")
    db.create_table('shipment')
    yield db

    # close
    db.close()

with managed_db() as db:
    print(db.get_all())