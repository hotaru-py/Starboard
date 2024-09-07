from pydantic import BaseModel


class Factors(BaseModel):
    slider1: int
    slider2: int
    slider3: int
    slider4: int
    slider5: int


class Locations(BaseModel):
    from_location: str
    to_location: str
