from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import time

from sqlalchemy import create_engine, text


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE_URL = "mysql+pymysql://myglico:myglico@127.0.0.1:3307/myglico?charset=utf8mb4"


def run(command: list[str], *, env: dict[str, str] | None = None) -> None:
    print("$ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT_DIR, env=env, check=True)


def wait_for_database(database_url: str, timeout_seconds: int) -> None:
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            engine = create_engine(database_url, future=True, pool_pre_ping=True)
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            engine.dispose()
            print("MySQL is ready.", flush=True)
            return
        except Exception as exc:
            last_error = exc
            time.sleep(2)
    raise RuntimeError(f"MySQL did not become ready within {timeout_seconds}s. Last error: {last_error}")


def run_migrations(database_url: str) -> None:
    env = os.environ.copy()
    env["MYGLICO_DATABASE_URL"] = database_url
    run([sys.executable, "-m", "alembic", "upgrade", "head"], env=env)


def import_dataset(database_url: str, force: bool) -> None:
    os.environ["MYGLICO_DATABASE_URL"] = database_url
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

    from app.db.session import SessionLocal
    from app.models.entities import GlucoseRecord, GlucoseRecordSource, Patient, RawImportRecord
    from app.services.uci_importer import import_uci_diabetes

    with SessionLocal() as db:
        import_batch, dataset = import_uci_diabetes(db, skip_if_loaded=not force)
        counts = {
            "patients": db.query(Patient).count(),
            "raw_import_records": db.query(RawImportRecord).count(),
            "glucose_records": db.query(GlucoseRecord).count(),
            "glucose_record_sources": db.query(GlucoseRecordSource).count(),
        }

    print("", flush=True)
    print("UCI Diabetes import completed.", flush=True)
    print(f"Import batch: {import_batch.id}", flush=True)
    print(f"Dataset imported now: {'yes' if dataset is not None else 'no, already loaded'}", flush=True)
    print(f"Raw records in batch: {import_batch.raw_record_count}", flush=True)
    print(f"Normalized glucose records in batch: {import_batch.normalized_record_count}", flush=True)
    print("Table counts:", flush=True)
    for name, count in counts.items():
        print(f"  - {name}: {count}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize MySQL and import the UCI Diabetes dataset for MyGlico Semantic.")
    parser.add_argument("--database-url", default=os.environ.get("MYGLICO_DATABASE_URL", DEFAULT_DATABASE_URL))
    parser.add_argument("--skip-docker", action="store_true", help="Do not start Docker Compose db service.")
    parser.add_argument("--skip-migrations", action="store_true", help="Do not run Alembic migrations.")
    parser.add_argument("--force-import", action="store_true", help="Import even when dataset records already exist.")
    parser.add_argument("--timeout", type=int, default=180, help="Seconds to wait for MySQL readiness.")
    args = parser.parse_args()

    if not args.skip_docker:
        run(["docker", "compose", "up", "-d", "db"])

    wait_for_database(args.database_url, args.timeout)

    if not args.skip_migrations:
        run_migrations(args.database_url)

    import_dataset(args.database_url, force=args.force_import)


if __name__ == "__main__":
    main()
