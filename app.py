from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class RentalRequest(BaseModel):
    rental_income: float
    expenses: float
    mortgage_interest: float = 0
    property_tax: float = 0
    insurance: float = 0
    repairs: float = 0
    purchase_price: float = 0
    land_value: float = 0
    filing_status: str
    active_participation: bool = True

@app.post("/rental_analysis")
def rental_analysis(data: RentalRequest):
    annual_depreciation = (data.purchase_price - data.land_value) / 27.5 if data.purchase_price and data.land_value else 0
    cash_flow = data.rental_income - data.expenses
    taxable_income = cash_flow - annual_depreciation
    passive_loss_warning = ""
    if not data.active_participation and taxable_income < 0:
        passive_loss_warning = "Passive losses may be disallowed due to lack of active participation."

    return {
        "cash_flow": cash_flow,
        "taxable_income": taxable_income,
        "annual_depreciation": annual_depreciation,
        "passive_loss_warning": passive_loss_warning
    }
