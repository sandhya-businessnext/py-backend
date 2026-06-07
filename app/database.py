import sqlite3
from .schemas import ShipmentCreate, ShipmentUpdate
from typing import Any


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("shipments.db",check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.create_table('shipment')
        # self.create({"content": "Licht", "weight": 200, "status": "In Transit"})
        self.delete(2)
       
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

db = Database()