from starlette.responses import RedirectResponse
import pandas as pd
from fastapi import Query
import httpx
import seed_db
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

Base.metadata.create_all(bind=engine)

try:
    seed_db.seed()
except Exception as e:
    print(f"Error seeding database: {e}")

app = FastAPI(title="Prueba tecnica - Backend Trainee")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/reconciliation/{batch}")
async def reconciliation(batch: str, db: Session = Depends(get_db)):
    query_exp = "SELECT * FROM expected_payments WHERE batch = :batch"
    query_rec = "SELECT * FROM received_payments WHERE batch = :batch"

    df_expected = pd.read_sql(query_exp, engine, params={"batch": batch})
    df_received = pd.read_sql(query_rec, engine, params={"batch": batch})

    async with httpx.AsyncClient() as client:
        res = await client.get(BASE_URL)
        data = res.json()
        tasa_mxn = data["conversion_rates"].get("MXN", 1.0)

    if not df_expected.empty:
        df_result = pd.merge(df_expected, df_received, left_on="id", right_on="expec_pay_id", how="left", suffixes=('_exp', '_rec'))
        
        def determinar_estado(row):
            if pd.isna(row['amount_rec']):
                return "NO_RECIBIDO"
            elif row['amount_rec'] == row['amount_exp']:
                return "CONCILIADO"
            else:
                return "MONTO_DIFERENTE"
                
        df_result['status'] = df_result.apply(determinar_estado, axis=1)

        df_result['amount_rec_usd'] = round(df_result['amount_rec'] / tasa_mxn, 2)

        columnas_finales = ['id_exp', 'customer_name', 'amount_exp', 'amount_rec', 'status', 'amount_rec_usd']
        df_final = df_result[columnas_finales]
    else:
        df_final = pd.DataFrame()

    csv_text = df_final.to_csv(index=False, encoding="utf-8-sig")

    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=reconciliation_{batch}.csv"}
    )

