import pandas as pd
from sqlalchemy import text
from database import engine

def seed():
    with engine.connect() as conn:
        expected_count = conn.execute(text("SELECT COUNT(*) FROM expected_payments")).scalar()
        if expected_count == 0:
            # Añadimos encoding="latin-1" o "utf-8-sig" según corresponda
            df_expected = pd.read_csv("csv/expected_payments.csv", encoding="utf-8-sig")
            df_expected.to_sql("expected_payments", con=engine, if_exists="append", index=False)
            print("Seeded expected_payments.")
            
        received_count = conn.execute(text("SELECT COUNT(*) FROM received_payments")).scalar()
        if received_count == 0:
            # Hacemos lo mismo aquí
            df_received = pd.read_csv("csv/received_payments.csv", encoding="utf-8-sig")
            df_received.to_sql("received_payments", con=engine, if_exists="append", index=False)
            print("Seeded received_payments.")