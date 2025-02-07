from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class Credentials(BaseModel):
    login: str
    password: str

class Address(BaseModel):
    street: str
    extra: Optional[str] = None
    city: str
    state: str
    zipCode: str

class Company(BaseModel):
    name: str
    designator: str
    address: Address

class Contact(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    mobile: str

class Member(BaseModel):
    isIndividual: bool
    firstName: str
    lastName: str
    companyName: Optional[str] = None
    percentOfOwnership: int
    address: Address

class Agent(BaseModel):
    isIndividual: bool
    firstName: str
    lastName: str
    companyName: Optional[str] = None
    address: Address

class Organizer(BaseModel):
    isIndividual: bool
    firstName: str
    lastName: str
    middleName: Optional[str] = None
    companyName: Optional[str] = None
    email: EmailStr
    phone: str
    addressStreet: str
    addressExtra: Optional[str] = None
    addressState: str
    addressCity: str
    addressZipCode: str
    addressCountry: str
    addressCounty: str

class FormData(BaseModel):
    entityType: str
    entityState: str
    activityType: str
    company: Company
    contact: Contact
    members: List[Member]
    agent: Agent
    organizer: Organizer

class RequestResponse(BaseModel):
    credentials: Credentials
    state: str = Field(..., min_length=2, max_length=2, description="Двухбуквенное обозначение штата, например, OR")
    data: FormData
