# ruff: noqa: D100, D101, D103, F841


import duckdb
import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


zpravy = pd.read_pickle("pickle/zpravy.pkl")
vazby = pd.read_pickle("pickle/vazby.pkl")
dokumentace = pd.read_pickle("pickle/dokumentace.pkl")
materialy = pd.read_pickle("pickle/material.pkl")
vykony = pd.read_pickle("pickle/vykony.pkl")
vykpac = pd.read_pickle("pickle/vykpac.pkl")


def read_jsonl(path: str) -> dict:
    import json

    with open(path) as f:
        obj_lines = [json.loads(line) for line in f]
        return {str(line["code"]): line["name"] for line in obj_lines}


def read_jsonl_vykony(path: str) -> pd.DataFrame:
    import json

    with open(path) as f:
        obj_lines = [json.loads(line) for line in f]
        return pd.DataFrame(obj_lines)


materialy_labels = read_jsonl("data/ciselniky/materialy.jsonl")
vykony_labels = read_jsonl("data/ciselniky/vykon.jsonl")
vykony_labels_df = read_jsonl_vykony("data/ciselniky/vykon.jsonl")


res = duckdb.sql(
    """
    with zpravy_a_vazby as (
        select
            z.serial as zprava_serial,
            z.rc,
            z.ambnum,
            z.content,
            date_trunc('day', STRFTIME(STRPTIME(vazby.DATFR, '%d.%m.%Y %H:%M'), '%Y-%m-%dT%H:%M:%S')::timestamp) as datum_a_cas_zpravy,
            vazby.DEPARTM,
            vazby.WHO,
        from zpravy z
            left join vazby using (serial, ambnum)
    ), zpravy_a_vazby_a_dokumentace_tmp as (
        select distinct  -- why do we have duplicates
            datum_a_cas_zpravy,
            date_trunc('day', strptime(d.DATUM_CAS::text, '%Y%m%d_%H%M%S')) as datum_a_cas_dokumentace,
            zv.ambnum,
            zv.content,
            d.CISPAC,
        from zpravy_a_vazby zv
            asof left join dokumentace d
                on zv.ambnum = d.ambnum
                and date_trunc('day', strptime(d.DATUM_CAS::text, '%Y%m%d_%H%M%S')) >= datum_a_cas_zpravy
    ), zpravy_a_vazby_a_dokumentace as (
        select
            datum_a_cas_zpravy,
            ambnum,
            array_agg(distinct content) as contents,
            min(cispac) as cispac,
        from zpravy_a_vazby_a_dokumentace_tmp
        group by 
            datum_a_cas_zpravy,
            ambnum
    ), zpravy_a_vazby_a_dokumentace_a_vykony_tmp as (
        select
            date_trunc('day', strptime(datum::text, '%d.%m.%Y %H:%M')) as datum_vykonu,
            z.*,
            u.CDOKL,
            u.kod as kod_vykonu,
            u.odbornost,
            u.mnozstvi as mnozstvi_vykonu,
            u.body,
        from zpravy_a_vazby_a_dokumentace z
            left join vykony u on
                z.cispac = u.cispac
                and date_trunc('day', strptime(datum::text, '%d.%m.%Y %H:%M')) = datum_a_cas_zpravy
    ), zpravy_a_vazby_a_dokumentace_a_vykony as (
        select
            datum_a_cas_zpravy,
            contents,
            AMBNUM,
            cispac,
            array_agg(
                struct_pack(
                    CDOKL,
                    kod_vykonu,
                    odbornost,
                    mnozstvi_vykonu,
                    body
                )
            ) as vykony
        from zpravy_a_vazby_a_dokumentace_a_vykony_tmp
        group by 
            datum_a_cas_zpravy,
            contents,
            AMBNUM,
            cispac,
    ), zpravy_a_vazby_a_dokumentace_a_vykony_a_materialy_tmp as (
        select
            z.*,
            m.cdokl,
            m.kod as kod_materialu,
            m.mnozstvi as mnozstvi_materialu,
        from zpravy_a_vazby_a_dokumentace_a_vykony z
            left join materialy m on
                z.cispac = m.cispac
                and date_trunc('day', strptime(m.datum::text, '%d.%m.%Y %H:%M')) = datum_a_cas_zpravy
    ), zpravy_a_vazby_a_dokumentace_a_vykony_a_materialy as (
        select
            datum_a_cas_zpravy,
            contents,
            AMBNUM,
            cispac,
            vykony,
            array_agg(
                struct_pack(
                    cdokl,
                    kod_materialu,
                    mnozstvi_materialu
                )
            ) as materialy
        from zpravy_a_vazby_a_dokumentace_a_vykony_a_materialy_tmp
        group by 
            datum_a_cas_zpravy,
            contents,
            AMBNUM,
            cispac,
            vykony,
    )
    select *
    from zpravy_a_vazby_a_dokumentace_a_vykony_a_materialy
    order by datum_a_cas_zpravy ASC
    """
).df()


@app.get("/vykony")
async def get_vykony_cis(query: str = Query(default="")) -> dict:
    test = (
        duckdb.sql(
            f"select * from vykony_labels_df where name ilike '%{query}%' or description ilike '%{query}%' limit 10"
        )
        .df()
        .to_dict(orient="records")
    )

    return {"result": test}


@app.get("/get_patient_data/{iloc}")
async def get_patient_data(iloc: int):
    row = res.iloc[iloc].fillna("").to_dict()

    def map_kod_vykonu(input: dict) -> dict:
        res = input.copy()
        if kod_vykonu := vykony_labels.get(str(res["kod_vykonu"])):
            res["kod_vykonu"] = f"({res['kod_vykonu']}): {kod_vykonu}"
        return res

    def map_kod_materialu(input: dict) -> dict:
        res = input.copy()
        if kod_materialu := (
            materialy_labels.get(str(int(res["kod_materialu"])))
            or materialy_labels.get(str(res["kod_materialu"]))
        ):
            res["kod_materialu"] = f"({res['kod_materialu']}): {kod_materialu}"
        return res

    response = {
        "zpravy_content": "\n".join(row["contents"]),
        "material": list(
            map_kod_materialu(x)
            for x in row["materialy"]
            if any(filter(lambda y: y, x.values()))
        ),
        "vykony": list(
            map_kod_vykonu(x)
            for x in row["vykony"]
            if any(filter(lambda y: y, x.values()))
        ),
    }

    return response
