import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from database import Base


class ShopModel(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), default="")
    name = Column(String(100), default="Oto Servis")
    logo_url = Column(String(500), default="")
    package = Column(String(20), default="usta")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=True)
    upgrade_request = Column(String(20), nullable=True)

    customers = relationship("CustomerModel", back_populates="shop", cascade="all, delete-orphan")
    vehicles = relationship("VehicleModel", back_populates="shop", cascade="all, delete-orphan")
    quotes = relationship("QuoteModel", back_populates="shop", cascade="all, delete-orphan")

    def to_dict(self):
        c_at = self.created_at.isoformat() if self.created_at else None
        if c_at and not c_at.endswith("Z"):
            c_at += "Z"
        e_at = self.expires_at.isoformat() if self.expires_at else None
        if e_at and not e_at.endswith("Z"):
            e_at += "Z"
        return {
            "phone_number": self.phone_number,
            "password_hash": self.password_hash,
            "name": self.name,
            "logo_url": self.logo_url,
            "package": self.package,
            "is_active": self.is_active,
            "is_admin": self.phone_number == "5555105635",
            "created_at": c_at,
            "expires_at": e_at,
            "upgrade_request": self.upgrade_request
        }


class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="CASCADE"), nullable=False, index=True)
    name_surname = Column(String(100), nullable=False)
    phone_number = Column(String(20), index=True)
    tax_no_or_id = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    shop = relationship("ShopModel", back_populates="customers")
    vehicles = relationship("VehicleModel", back_populates="customer")

    def to_dict(self):
        return {
            "id": self.id,
            "shop_id": self.shop_id,
            "name_surname": self.name_surname,
            "phone_number": self.phone_number,
            "tax_no_or_id": self.tax_no_or_id,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class VehicleModel(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="CASCADE"), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"), nullable=True, index=True)
    plaka = Column(String(20), index=True, nullable=False)
    brand = Column(String(50), default="")
    model = Column(String(50), default="")
    year = Column(Integer, nullable=True)
    vin_number = Column(String(50), nullable=True)
    current_km = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)

    shop = relationship("ShopModel", back_populates="vehicles")
    customer = relationship("CustomerModel", back_populates="vehicles")

    def to_dict(self):
        return {
            "id": self.id,
            "shop_id": self.shop_id,
            "customer_id": self.customer_id,
            "plaka": self.plaka,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "vin_number": self.vin_number,
            "current_km": self.current_km,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class QuoteModel(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    quote_id = Column(String(50), unique=True, index=True, nullable=False)
    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="CASCADE"), nullable=True, index=True)
    phone_number = Column(String(20), index=True, nullable=False)
    plaka = Column(String(20), index=True, nullable=False)
    vehicle = Column(String(100), default="")
    items_json = Column(Text, default="[]")
    subtotal = Column(Float, default=0.0)
    vat = Column(Float, default=0.0)
    total_price = Column(Float, default=0.0)
    discount_price = Column(Float, default=0.0)
    pdf_filename = Column(String(200), default="")
    validity_days = Column(Integer, default=7)
    usta_note = Column(Text, default="")
    status = Column(String(20), default="beklemede")
    created_at = Column(DateTime, default=datetime.now)

    shop = relationship("ShopModel", back_populates="quotes")

    def get_items(self):
        try:
            return json.loads(self.items_json) if self.items_json else []
        except Exception:
            return []

    def set_items(self, items_list):
        self.items_json = json.dumps(items_list, ensure_ascii=False)

    def to_dict(self):
        return {
            "quote_id": self.quote_id,
            "phone_number": self.phone_number,
            "plaka": self.plaka,
            "vehicle": self.vehicle,
            "items": self.get_items(),
            "subtotal": self.subtotal,
            "vat": self.vat,
            "total_price": self.total_price,
            "discount_price": self.discount_price,
            "pdf_filename": self.pdf_filename,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "validity_days": self.validity_days,
            "usta_note": self.usta_note,
            "status": self.status
        }
