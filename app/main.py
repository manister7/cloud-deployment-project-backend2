from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .database import SessionLocal
from .schemas import CreateOrder

app = FastAPI(title="Order-Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"service": "orders"}


@app.get("/orders")
def get_orders():

    with SessionLocal() as db:

        rows = db.execute(text("""
            SELECT
                o.id,
                o.customer_name,
                p.name product_name,
                o.created_at
            FROM orders o
            JOIN products p
            ON p.id = o.product_id
            ORDER BY o.id DESC
        """))

        return [
            {
                "id": r.id,
                "customer_name": r.customer_name,
                "product_name": r.product_name,
                "created_at": r.created_at
            }
            for r in rows
        ]


@app.post("/orders")
def create_order(payload: CreateOrder):

    with SessionLocal() as db:

        db.execute(
            text("""
                INSERT INTO orders(
                    customer_name,
                    product_id
                )
                VALUES(
                    :customer_name,
                    :product_id
                )
            """),
            {
                "customer_name": payload.customer_name,
                "product_id": payload.product_id
            }
        )

        db.commit()

        return {
            "message": "Order Created"
        }


@app.delete("/orders/{order_id}")
def delete_order(order_id: int):

    with SessionLocal() as db:

        db.execute(
            text("""
                DELETE FROM orders
                WHERE id=:id
            """),
            {"id": order_id}
        )

        db.commit()

        return {
            "message": "Order Deleted"
        }
