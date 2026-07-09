from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String, unique=True, index=True, nullable=False)
    location = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    readings = relationship("Reading", back_populates="node")


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("nodes.node_id"), nullable=False, index=True)

    turbidity_ntu = Column(Float, nullable=True)
    ph = Column(Float, nullable=True)
    tds_ppm = Column(Float, nullable=True)
    temperature_c = Column(Float, nullable=True)

    turbidity_status = Column(String, nullable=True)   # safe / warning / danger
    ph_status = Column(String, nullable=True)
    tds_status = Column(String, nullable=True)

    is_simulated = Column(Boolean, default=False)
    received_at = Column(DateTime(timezone=True), server_default=func.now())

    node = relationship("Node", back_populates="readings")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("nodes.node_id"), nullable=False, index=True)
    parameter = Column(String, nullable=False)   # turbidity / ph / tds
    value = Column(Float, nullable=False)
    severity = Column(String, nullable=False)    # warning / danger
    message = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
