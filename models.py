from sqlalchemy import create_engine, Integer, String, ForeignKey, Table, Column, Date, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Mapped, mapped_column
from datetime import date, datetime


Base = declarative_base()
engine = create_engine('sqlite:///clinic.db')

Session = sessionmaker(bind=engine)
session = Session()


class Owner(Base):
    """Owner model representing pet owners"""
    __tablename__ = 'owners'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Relationships
    pet: Mapped[list["Pet"]] = relationship("Pet", back_populates="owner")



class Pet(Base):
    """Pet model representing pets in the clinic"""
    __tablename__ = 'pets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=False)
    breed: Mapped[str] = mapped_column(String(100), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('owners.id'), nullable=False)

    # Relationships
    owner: Mapped["Owner"] = relationship("Owner", back_populates="pet")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="pet")




class Vet(Base):
    """Veterinarian model representing clinic veterinarians"""
    __tablename__ = 'vets'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialization: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    # Relationships
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="vet", )


class Appointment(Base):
    """Appointment model representing pet appointments with veterinarians"""
    __tablename__ = 'appointments'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey('pets.id'), nullable=False)
    veterinarian_id: Mapped[int] = mapped_column(Integer, ForeignKey('vets.id'), nullable=False)
    appointment_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="Scheduled", nullable=False)
    
    # Relationships
    pet: Mapped["Pet"] = relationship("Pet", back_populates="appointments")
    vet: Mapped["Vet"] = relationship("Vet", back_populates="appointments")


Base.metadata.create_all(engine)

# Vets
vet1 = Vet(name="Dr. Dizzy", specialization="Anesthesiologist", email="dylank@clinic.com")
vet2 = Vet(name="Dr. James Brown", specialization="Surgery", email="james.brown@clinic.com")
vet3 = Vet(name="Dr. Lisa Garcia", specialization="Dermatology", email="lisa.garcia@clinic.com")
vet4 = Vet(name="Dr. Emily Wilson", specialization="General", email="emily.wilson@clinic.com")

session.add_all([vet1,vet2,vet3,vet4])
session.commit()

# Owners
owner1 = Owner(name="Alice Johnson", phone="555-1111", email="alice@example.com", password="alicepass")
owner2 = Owner(name="Bob Smith", phone="555-2222", email="bob@example.com", password="bobpass")
owner3 = Owner(name="Carol Davis", phone="555-3333", email="carol@example.com", password="carolpass")

session.add_all([owner1, owner2, owner3])
session.commit()

# Pets
pet1 = Pet(name="Buddy", species="Dog", breed="Labrador", age=3, owner=owner1)
pet2 = Pet(name="Mittens", species="Cat", breed="Tabby", age=2, owner=owner1)
pet3 = Pet(name="Rex", species="Dog", breed="German Shepherd", age=5, owner=owner2)
pet4 = Pet(name="Tweety", species="Bird", breed="Canary", age=1, owner=owner2)
pet5 = Pet(name="Shadow", species="Cat", breed="Bombay", age=4, owner=owner3)
pet6 = Pet(name="Coco", species="Bird", breed="Parrot", age=6, owner=owner3)

session.add_all([pet1, pet2, pet3, pet4, pet5, pet6])
session.commit()

# Appointments
appt1 = Appointment(
    pet=pet1,
    vet=vet1,
    appointment_date=datetime.now(),
    notes="Annual checkup",
    status="Scheduled",
)

appt2 = Appointment(
    pet=pet1,
    vet=vet2,
    appointment_date=datetime.now(),
    notes="Skin rash follow-up",
)

appt3 = Appointment(
    pet=pet3,
    vet=vet1,
    appointment_date=datetime.now(),
    notes="Surgery consultation",
)

session.add_all([appt1, appt2, appt3])
session.commit()