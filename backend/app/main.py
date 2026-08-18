from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from app.database import engine, get_db, Base
from app import models, schemas, thresholds

# Create tables on startup (fine for dev; use Alembic migrations later for production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Water Pollution Monitoring API",
    description="Backend for the IoT-based water pollution monitoring system",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this before production deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "water-pollution-monitoring-api"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/readings", response_model=schemas.ReadingOut)
def create_reading(reading: schemas.ReadingIn, db: Session = Depends(get_db)):
    # Ensure the node exists, create it if this is its first reading
    node = db.query(models.Node).filter(models.Node.node_id == reading.node_id).first()
    if not node:
        node = models.Node(node_id=reading.node_id)
        db.add(node)
        db.commit()
        db.refresh(node)

    # Evaluate thresholds
    turbidity_status = thresholds.evaluate_turbidity(reading.turbidity_ntu)
    ph_status = thresholds.evaluate_ph(reading.ph)
    tds_status = thresholds.evaluate_tds(reading.tds_ppm)

    db_reading = models.Reading(
        node_id=reading.node_id,
        turbidity_ntu=reading.turbidity_ntu,
        ph=reading.ph,
        tds_ppm=reading.tds_ppm,
        temperature_c=reading.temperature_c,
        turbidity_status=turbidity_status,
        ph_status=ph_status,
        tds_status=tds_status,
        is_simulated=reading.is_simulated,
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    # Generate and store alerts for any non-safe parameter
    alerts = thresholds.build_alerts(
        reading.node_id, turbidity_status, ph_status, tds_status,
        reading.turbidity_ntu, reading.ph, reading.tds_ppm
    )
    for alert in alerts:
        db.add(models.Alert(**alert))
    if alerts:
        db.commit()

    return db_reading


@app.get("/api/readings", response_model=List[schemas.ReadingOut])
def list_readings(
    node_id: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Reading)
    if node_id:
        query = query.filter(models.Reading.node_id == node_id)
    return (
        query.order_by(desc(models.Reading.received_at), desc(models.Reading.id))
        .limit(limit)
        .all()
    )


@app.get("/api/readings/latest", response_model=List[schemas.ReadingOut])
def latest_readings(db: Session = Depends(get_db)):
    """Returns the most recent reading for each node."""
    nodes = db.query(models.Node).all()
    latest = []
    for n in nodes:
        reading = (
            db.query(models.Reading)
            .filter(models.Reading.node_id == n.node_id)
            .order_by(desc(models.Reading.received_at), desc(models.Reading.id))
            .first()
        )
        if reading:
            latest.append(reading)
    return latest


@app.get("/api/nodes", response_model=List[schemas.NodeOut])
def list_nodes(db: Session = Depends(get_db)):
    return db.query(models.Node).all()


@app.get("/api/alerts", response_model=List[schemas.AlertOut])
def list_alerts(node_id: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(models.Alert)
    if node_id:
        query = query.filter(models.Alert.node_id == node_id)
    return query.order_by(desc(models.Alert.created_at)).limit(limit).all()


@app.get("/api/stats/reliability")
def transmission_reliability(node_id: str, expected_interval_seconds: int = 60, db: Session = Depends(get_db)):
    """
    Basic transmission reliability metric for Objective iv evaluation:
    compares actual reading count against expected count based on time span.
    """
    readings = (
        db.query(models.Reading)
        .filter(models.Reading.node_id == node_id)
        .order_by(models.Reading.received_at)
        .all()
    )
    if len(readings) < 2:
        raise HTTPException(status_code=400, detail="Not enough readings to calculate reliability yet.")

    time_span_seconds = (readings[-1].received_at - readings[0].received_at).total_seconds()
    expected_count = int(time_span_seconds / expected_interval_seconds) + 1
    actual_count = len(readings)
    reliability_percent = round((actual_count / expected_count) * 100, 2) if expected_count > 0 else 0

    return {
        "node_id": node_id,
        "actual_readings": actual_count,
        "expected_readings": expected_count,
        "reliability_percent": min(reliability_percent, 100.0),
    }

@app.get("/api/classify/{node_id}")
def classify_node(node_id: str, db: Session = Depends(get_db)):
    reading = (
        db.query(models.Reading)
        .filter(models.Reading.node_id == node_id)
        .order_by(desc(models.Reading.received_at), desc(models.Reading.id))
        .first()
    )
    if not reading:
        raise HTTPException(status_code=404, detail="No readings found for this node.")

    result = thresholds.classify_usability(
        reading.turbidity_status, reading.ph_status, reading.tds_status
    )

    return {
        "node_id": node_id,
        "usability_class": result["usability_class"],
        "guidance": result["guidance"],
        "based_on_reading_id": reading.id,
        "received_at": reading.received_at,
    }