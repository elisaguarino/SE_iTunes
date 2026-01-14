from dataclasses import dataclass
@dataclass
class Traccia:
    id:int
    name:str
    album_id:int
    media_type_id:int
    genre_id:int
    composer:str
    milliseconds:float
    bytes:int
    unit_price:float

    def __str__(self):
        return f"{self.id},{self.name},{self.album_id}"
    def __repr__(self):
        return f"{self.id},{self.name},{self.album_id}"
    def __hash__(self):
        return hash(self.id)