from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    favorites_personaje: Mapped[List["Favorites_Personaje"]] = relationship(back_populates="user")
    favorites_planeta: Mapped[List["Favorites_Planeta"]] = relationship(back_populates="user")
    favorites_nave: Mapped[List["Favorites_Nave"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }


class Favorites_Personaje(db.Model):
    __tablename__ = "favorites_personaje"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personaje.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorites_personaje")
    personaje: Mapped["Personaje"] = relationship(back_populates="favorited")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "personaje_id": self.personaje_id
        }


class Favorites_Planeta(db.Model):
    __tablename__ = "favorites_planeta"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planeta.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorites_planeta")
    planeta: Mapped["Planeta"] = relationship(back_populates="favorited")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planeta": self.planeta_id
        }


class Favorites_Nave(db.Model):
    __tablename__ = "favorites_nave"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    nave_id: Mapped[int] = mapped_column(ForeignKey("nave.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorites_nave")
    nave: Mapped["Nave"] = relationship(back_populates="favorited")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "nave": self.nave_id
        }


class Personaje(db.Model):
    __tablename__ = "personaje"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)

    id_planeta: Mapped[Optional[int]] = mapped_column(ForeignKey("planeta.id"), nullable=True)
    id_nave: Mapped[Optional[int]] = mapped_column(ForeignKey("nave.id"), nullable=True)

    planeta: Mapped["Planeta"] = relationship(back_populates="residentes")
    nave: Mapped["Nave"] = relationship(back_populates="pilotos")
    favorited: Mapped[List["Favorites_Personaje"]] = relationship(back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "id_planeta": self.id_planeta,
            "id_nave": self.id_nave
        }


class Planeta(db.Model):
    __tablename__ = "planeta"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    clima: Mapped[str] = mapped_column(String(120), nullable=False)

    residentes: Mapped[List["Personaje"]] = relationship(back_populates="planeta")
    favorited: Mapped[List["Favorites_Planeta"]] = relationship(back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima
        }


class Nave(db.Model):
    __tablename__ = "nave"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    modelo: Mapped[str] = mapped_column(String(120), nullable=False)

    pilotos: Mapped[List["Personaje"]] = relationship(back_populates="nave")
    favorited: Mapped[List["Favorites_Nave"]] = relationship(back_populates="nave")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "modelo": self.modelo
        }