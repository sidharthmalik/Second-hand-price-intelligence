"""Product classes (CO1, CO3: classes, objects, inheritance)."""
from dataclasses import dataclass, asdict
from datetime import date


@dataclass
class Product:
    product_id: str
    brand: str
    model: str
    category: str
    release_year: int
    purchase_year: int
    condition: str
    processor: str
    ram_gb: int
    storage_gb: int
    original_price: float
    listed_price: float

    @property
    def age(self) -> int:
        return date.today().year - self.release_year

    def to_dict(self) -> dict:
        return asdict(self)

    def summary(self) -> str:
        return f"{self.brand} {self.model} ({self.condition})"


class Laptop(Product):
    def summary(self) -> str:
        return (f"{self.brand} {self.model} | {self.processor}, "
                f"{self.ram_gb}GB RAM, {self.storage_gb}GB | {self.condition}")


class Smartphone(Product):
    def summary(self) -> str:
        return (f"{self.brand} {self.model} | {self.ram_gb}GB/{self.storage_gb}GB "
                f"| {self.condition}")


class Tablet(Smartphone):
    pass


CATEGORY_CLASSES = {"Laptop": Laptop, "Smartphone": Smartphone, "Tablet": Tablet}


def product_from_dict(data: dict) -> Product:
    """Factory: build the right subclass from a dict/row."""
    cls = CATEGORY_CLASSES.get(data.get("category"), Product)
    fields = Product.__dataclass_fields__.keys()
    return cls(**{k: data[k] for k in fields})
