# ruff: noqa: D100, D101, D103

import datetime

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_patient_data/{iloc}")
async def get_patient_data(iloc: int):
    zpravy = pd.read_pickle("pickle/zpravy.pkl")
    vazby = pd.read_pickle("pickle/vazby.pkl")
    dokumentace = pd.read_pickle("pickle/dokumentace.pkl")
    material = pd.read_pickle("pickle/material.pkl")
    vykony = pd.read_pickle("pickle/vykony.pkl")
    vykpac = pd.read_pickle("pickle/vykpac.pkl")

    try:
        item_zpravy = zpravy.iloc[iloc]
    except IndexError:
        raise HTTPException(status_code=404, detail="Patient data not found")

    item_vazby = vazby[
        (vazby["SERIAL"] == item_zpravy["SERIAL"])
        & (vazby["AMBNUM"] == item_zpravy["AMBNUM"])
    ]

    item_vazby_dokumentace_date = datetime.datetime.strftime(
        pd.to_datetime(item_vazby["DATFR"], format="%d.%m.%Y %H:%M").squeeze(),
        "%Y%m%d_%H%M00",
    )
    item_vazby_vyk_date = datetime.datetime.strftime(
        pd.to_datetime(item_vazby["DATFR"], format="%d.%m.%Y %H:%M").squeeze(),
        "%d.%m.%Y 00:00",
    )

    item_dokumentace = dokumentace[
        (dokumentace["AMBNUM"] == item_zpravy["AMBNUM"])
        & (dokumentace["DATUM_CAS"] == item_vazby_dokumentace_date)
    ]

    cispac = next(x for x in item_dokumentace["CISPAC"])

    material_data = material[
        (material["CISPAC"] == cispac) & (material["DATUM"] == item_vazby_vyk_date)
    ]
    vykony_data = vykony[
        (vykony["CISPAC"] == cispac) & (vykony["DATUM"] == item_vazby_vyk_date)
    ]
    vykpac_data = vykpac[vykpac["CISPAC"] == cispac]

    response = {
        "zpravy_content": item_zpravy["CONTENT"],
        "vazby": item_vazby.fillna("").to_dict(orient="records"),
        "dokumentace": item_dokumentace.fillna("").to_dict(orient="records"),
        "material": material_data.fillna("").to_dict(orient="records"),
        "vykony": vykony_data.fillna("").to_dict(orient="records"),
        "vykpac": vykpac_data.fillna("").to_dict(orient="records"),
    }

    return response
