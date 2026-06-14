import os
import time

import psycopg
import requests


CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))
API_BASE_URL = os.getenv("API_BASE_URL", "http://api:8000")


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
    )


def get_active_sites():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, url
                FROM sites
                WHERE is_active = TRUE
                ORDER BY id;
                """
            )
            return cur.fetchall()


def check_site(site):
    site_id = site[0]
    site_name = site[1]
    site_url = site[2]

    try:
        response = requests.post(
            f"{API_BASE_URL}/sites/{site_id}/check",
            timeout=10,
        )

        if response.status_code >= 400:
            print(
                f"[ERROR] {site_name} | {site_url} | "
                f"API returned status={response.status_code}",
                flush=True,
            )
            return

        result = response.json()

        print(
            f"[CHECK] {site_name} | {site_url} | "
            f"status={result.get('status_code')} | "
            f"up={result.get('is_up')} | "
            f"time={result.get('response_time_ms')}ms",
            flush=True,
        )

    except requests.RequestException as error:
        print(
            f"[ERROR] {site_name} | {site_url} | "
            f"failed to call API | error={error}",
            flush=True,
        )


def run_monitor():
    print("SiteWatch monitor started", flush=True)

    while True:
        sites = get_active_sites()

        print(f"Found {len(sites)} active sites", flush=True)

        for site in sites:
            check_site(site)

        print(f"Waiting {CHECK_INTERVAL_SECONDS} seconds...", flush=True)
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_monitor()
