import os
import time

import psycopg
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
from psycopg.errors import UniqueViolation
from pydantic import BaseModel, HttpUrl


app = FastAPI(
    title="SiteWatch API",
    description="API para monitoramento de sites.",
    version="0.1.0"
)


site_status_gauge = Gauge(
    "sitewatch_site_up",
    "Status do site monitorado: 1 para online, 0 para offline",
    ["site_id", "site_name", "url"]
)

site_response_time_gauge = Gauge(
    "sitewatch_response_time_ms",
    "Tempo de resposta do site em milissegundos",
    ["site_id", "site_name", "url"]
)

site_checks_counter = Counter(
    "sitewatch_checks_total",
    "Total de verificações executadas pelo SiteWatch",
    ["site_id", "site_name", "url"]
)


class SiteCreate(BaseModel):
    name: str
    url: HttpUrl


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
    )


@app.get("/")
def root():
    return {"message": "SiteWatch API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/sites")
def list_sites():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, url, is_active, created_at
                FROM sites
                ORDER BY id;
                """
            )
            rows = cur.fetchall()

    return [
        {
            "id": row[0],
            "name": row[1],
            "url": row[2],
            "is_active": row[3],
            "created_at": row[4],
        }
        for row in rows
    ]


@app.post("/sites", status_code=201)
def create_site(site: SiteCreate):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO sites (name, url)
                    VALUES (%s, %s)
                    RETURNING id, name, url, is_active, created_at;
                    """,
                    (site.name, str(site.url))
                )
                row = cur.fetchone()

        return {
            "id": row[0],
            "name": row[1],
            "url": row[2],
            "is_active": row[3],
            "created_at": row[4],
        }

    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Site already exists"
        )


@app.post("/sites/{site_id}/check")
def check_site(site_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, url
                FROM sites
                WHERE id = %s AND is_active = TRUE;
                """,
                (site_id,)
            )

            site = cur.fetchone()

            if site is None:
                raise HTTPException(
                    status_code=404,
                    detail="Site not found or inactive"
                )

            site_id = site[0]
            site_name = site[1]
            site_url = site[2]

            status_code = None
            is_up = False
            response_time_ms = None
            error_message = None

            try:
                start_time = time.time()

                response = requests.get(
                    site_url,
                    timeout=5,
                    headers={
                        "User-Agent": "Mozilla/5.0 (SiteWatch Monitor)"
                    }
                )

                response_time_ms = int((time.time() - start_time) * 1000)
                status_code = response.status_code

                is_up = response.status_code < 500

            except requests.RequestException as error:
                error_message = str(error)

            cur.execute(
                """
                INSERT INTO site_checks (
                    site_id,
                    status_code,
                    is_up,
                    response_time_ms,
                    error_message
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, site_id, status_code, is_up, response_time_ms, error_message, checked_at;
                """,
                (
                    site_id,
                    status_code,
                    is_up,
                    response_time_ms,
                    error_message,
                )
            )

            check = cur.fetchone()

    site_status_gauge.labels(
        site_id=str(site_id),
        site_name=site_name,
        url=site_url
    ).set(1 if is_up else 0)

    if response_time_ms is not None:
        site_response_time_gauge.labels(
            site_id=str(site_id),
            site_name=site_name,
            url=site_url
        ).set(response_time_ms)

    site_checks_counter.labels(
        site_id=str(site_id),
        site_name=site_name,
        url=site_url
    ).inc()

    return {
        "id": check[0],
        "site_id": check[1],
        "site_name": site_name,
        "url": site_url,
        "status_code": check[2],
        "is_up": check[3],
        "response_time_ms": check[4],
        "error_message": check[5],
        "checked_at": check[6],
    }


@app.get("/sites/{site_id}/checks")
def list_site_checks(site_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, site_id, status_code, is_up, response_time_ms, error_message, checked_at
                FROM site_checks
                WHERE site_id = %s
                ORDER BY checked_at DESC;
                """,
                (site_id,)
            )

            rows = cur.fetchall()

    return [
        {
            "id": row[0],
            "site_id": row[1],
            "status_code": row[2],
            "is_up": row[3],
            "response_time_ms": row[4],
            "error_message": row[5],
            "checked_at": row[6],
        }
        for row in rows
    ]