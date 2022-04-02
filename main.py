from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Path, Query, HTTPException
from datetime import date

#create instance of fastapi
app = FastAPI()

#create basemodel of data you are entering
class Trip(BaseModel):
    country: str
    city: str

travel = {}

#get (returns info)
#create homepage
@app.get("/")
def home():
    return travel

#search by country
@app.get("/get-country/{country}")
def get_country(country: str):
    for start_date in travel:
        if travel[start_date].country == country:
            return travel[start_date]
    raise HTTPException(status_code=404, detail="Country not found.")

#create trip
@app.post("/create_trip/{start_date}")
def create_trip(start_date: date, trip: Trip):
    if start_date in travel:
        raise HTTPException(status_code=400, detail="Date has already been added.")

    travel[start_date] = trip
    return travel[start_date]

#delete trip
@app.delete("/delete-trip/")
