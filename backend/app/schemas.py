from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReadingIn(BaseModel):
    node_id: str = Field(..., description="Unique identifier for the ESP32 node")
    turbidity_ntu: Optional[float] = None
    ph: Optional[float] = None
    tds_ppm: Optional[float] = None
    temperature_c: Optional[float] = None
    is_simulated: bool = False


class ReadingOut(BaseModel):
    id: int
    node_id: str
    turbidity_ntu: Optional[float]
    ph: Optional[float]
    tds_ppm: Optional[float]
    temperature_c: Optional[float]
    turbidity_status: Optional[str]
    ph_status: Optional[str]
    tds_status: Optional[str]
    is_simulated: bool
    received_at: datetime

    class Config:
        from_attributes = True


class AlertOut(BaseModel):
    id: int
    node_id: str
    parameter: str
    value: float
    severity: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class NodeOut(BaseModel):
    id: int
    node_id: str
    location: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
