from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # allow all headers
)

facing_list=['facingDesc_East', 'facingDesc_West', 'facingDesc_North', 'facingDesc_North-East', 'facingDesc_South', "facingDesc_Don't Know", 'facingDesc_South-East', 'facingDesc_North-West', 'facingDesc_South-West']
furnish_list=['furnishing_Semi', 'furnishing_Unfurnished', 'furnishing_Full']
locality_list=['locality_Kondapur', 'locality_Kukatpally', 'locality_Gachibowli', 'locality_Miyapur', 'locality_Manikonda', 'locality_Nizampet', 'locality_Madhapur', 'locality_Hafeezpet', 'locality_Chanda Nagar', 'locality_Serilingampally', 'locality_Pragathi Nagar', 'locality_Banjara Hills', 'locality_Kothaguda', 'locality_Begumpet', 'locality_Kokapet', 'locality_Narsingi', 'locality_Attapur', 'locality_Madinaguda', 'locality_Shaikpet', 'locality_Ramachandra Puram', 'locality_Puppalguda', 'locality_Bachupally', 'locality_Toli Chowki', 'locality_Bandlaguda Jagir', 'locality_Nagole', 'locality_Nanakaramguda', 'locality_Puppalaguda', 'locality_Borabanda', 'locality_Mehdipatnam', 'locality_Manikonda Jagir', 'locality_Gajularamaram', 'locality_Boduppal', 'locality_Kothapet', 'locality_Uppal', 'locality_Hyderabad', 'locality_Nanakramguda', 'locality_Jubilee Hills', 'locality_Moosapet', 'locality_Saroornagar', 'locality_Hitec City', 'locality_Alwal', 'locality_Vanasthalipuram', 'locality_Pocharam', 'locality_Peerzadiguda', 'locality_Moti Nagar', 'locality_Tellapur', 'locality_Sainikpuri', 'locality_Kapra', 'locality_Beeramguda', 'locality_Nallagandla', 'locality_Somajiguda', 'locality_Amberpet', 'locality_Secunderabad', 'locality_West Marredpally', 'locality_Himayatnagar', 'locality_Malkajgiri', 'locality_Gopanpally', 'locality_Kavadiguda', 'locality_Nacharam', 'locality_Yousufguda', 'locality_Dilsukhnagar', 'locality_Kompally', 'locality_Old Bowenpally', 'locality_Ameerpet', 'locality_Gopanapalli', 'locality_Ameenpur', 'locality_New Nallakunta', 'locality_Adibatla', 'locality_Whitefields', 'locality_Nagaram', 'locality_Upparpally', 'locality_LB Nagar', 'locality_Moula Ali', 'locality_Lingampally']
parking_list=['parking_BOTH', 'parking_TWO_WHEELER', 'parking_FOUR_WHEELER', 'parking_NONE']
water_supply_list=['waterSupply_CORP_BORE', 'waterSupply_CORPORATION', 'waterSupply_BOREWELL']

non_cat_cols=['bathroom', 'property_age', 'property_size', 'totalFloor','amenities']
amenities_list=['swimmingPool', 'lift', 'gym', 'internet', 'AC', 'club', 'INTERCOM', 'servant', 'security']

class HouseRequest(BaseModel):
    bathrooms: str
    property_age: str
    property_size: str
    total_floor: str
    facing: str
    furnishing: str
    locality: str
    parking: str
    water_supply: str
    amenities: str

def get_facing(facing):
    try:
        facing_cols = pd.Series(facing_list)
        facing_cols = np.where(facing_cols == facing.strip(), True, False)
        return facing_cols
    except Exception as e:
        return print("error: "+str(e))

def get_furnishing(furnishing):
    try:
        furnishing_cols = pd.Series(furnish_list)
        furnishing_cols = np.where(furnishing_cols == furnishing.strip(), True, False)
        return furnishing_cols
    except Exception as e:
        return print("error: "+str(e))

def get_locality(locality):
    try:
        locality_cols = pd.Series(locality_list)
        locality_cols = np.where(locality_cols == locality.strip(), True, False)
        return locality_cols
    except Exception as e:
        return print("error: "+str(e))

def get_parking(parking):
    try:
        parking_cols = pd.Series(parking_list)
        parking_cols = np.where(parking_cols == parking.strip(), True, False)
        return parking_cols
    except Exception as e:
        return print("error: "+str(e))

def get_water_supply(water_supply):
    try:
        water_supply_cols = pd.Series(water_supply_list)
        water_supply_cols = np.where(water_supply_cols == water_supply.strip(), True, False)
        return water_supply_cols
    except Exception as e:
        return print("error: "+str(e))

@app.post("/predictprice")
async def predict_price(data: HouseRequest):
    try:
        loaded_model = pickle.load(open("finalized_model.sav", "rb"))

        facing_cols = get_facing(data.facing)
        furnishing_cols = get_furnishing(data.furnishing)
        locality_cols = get_locality(data.locality)
        parking_cols = get_parking(data.parking)
        water_supply_cols = get_water_supply(data.water_supply)

        input_data_list = [int(data.bathrooms), int(data.property_age), int(data.property_size), int(data.total_floor)] + list(facing_cols) + list(furnishing_cols) + list(locality_cols) + list(parking_cols) + list(water_supply_cols) + [int(data.amenities)]
        prediction = loaded_model.predict(np.array(input_data_list).reshape(1, -1))
        return {"prediction": str(round(prediction[0],2))}
    except Exception as e:
        return print("error: "+str(e))
