"""Behavioral - Template Method: data ETL pipelines.

Statement: https://courses.dallard.tech/sys_design/behavioral_pattern/
Run: python3 template_method_etl.py

Problems with the original code:
1. Validation is written 3 times, cleanup 3 times, load 3 times (~70% duplicate code).
2. Adding logging (or changing the workflow order) means editing all 3 classes.
3. Nothing forces a new pipeline to validate or clean up - a step can be forgotten.
4. The only real differences (source, extraction, transformation, required fields)
   are buried inside one long run() method, so they can't be tested alone.
"""
from __future__ import annotations

import time
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class DataPipeline(ABC):
    """Abstract base class. run() is the template method: it fixes the order."""

    source_type: str = "source"
    required_fields: tuple[str, ...] = ()
    delay: float = 0.5               # simulated network/disk latency

    def __init__(self, source: str) -> None:
        self.source = source
        self.data: list[dict] | None = None

    # ---- the template method: final workflow, not meant to be overridden ----
    def run(self) -> str:
        self.before_run()            # hook
        self.connect()
        self.data = self.extract()
        print(f"Extracted {len(self.data)} records")
        print(f"Transforming {self.source_type} data...")
        self.data = [self.transform(record) for record in self.data]
        print("Transformation complete")
        self.validate()
        self.load()
        self.cleanup()
        self.after_run()             # hook
        return f"{self.source_type} Pipeline finished"

    # ---- steps every subclass MUST implement (what is unique) ----
    @abstractmethod
    def extract(self) -> list[dict]: ...

    @abstractmethod
    def transform(self, record: dict) -> dict: ...

    # ---- common steps, written once ----
    def connect(self) -> None:
        print(f"Connecting to {self.source_type}: {self.source}")
        time.sleep(self.delay)
        print(f"{self.source_type} connection established")

    def validate(self) -> None:
        print("Validating data...")
        for record in self.data:
            if any(field not in record for field in self.required_fields):
                raise ValueError("Invalid record structure")
        print("Validation passed")

    def load(self) -> None:
        print("Loading data to destination...")
        time.sleep(self.delay)
        print(f"Loaded {len(self.data)} records successfully")

    def cleanup(self) -> None:
        print("Cleaning up resources...")
        self.data = None
        print("Cleanup complete")

    # ---- hooks: optional, empty by default ----
    def before_run(self) -> None:
        pass

    def after_run(self) -> None:
        pass


class CSVPipeline(DataPipeline):
    source_type = "CSV"
    required_fields = ("id", "name")

    def extract(self) -> list[dict]:
        print("Extracting data from CSV...")
        return [{"id": 1, "name": "Alice", "age": 30}, {"id": 2, "name": "Bob", "age": 25}]

    def transform(self, record: dict) -> dict:
        return {**record, "age": int(record["age"]), "name": record["name"].upper()}


class APIPipeline(DataPipeline):
    source_type = "API"
    required_fields = ("user_id", "username")

    def extract(self) -> list[dict]:
        print("Extracting data from API...")
        return [{"user_id": 101, "username": "charlie", "score": 85},
                {"user_id": 102, "username": "diana", "score": 92}]

    def transform(self, record: dict) -> dict:
        score = int(record["score"])
        return {**record, "score": score, "username": record["username"].lower(),
                "grade": "A" if score >= 90 else "B"}


class DatabasePipeline(DataPipeline):
    source_type = "Database"
    required_fields = ("product_id", "price")

    def extract(self) -> list[dict]:
        print("Extracting data from database...")
        return [{"product_id": 501, "product_name": "Laptop", "price": 1200},
                {"product_id": 502, "product_name": "Mouse", "price": 25}]

    def transform(self, record: dict) -> dict:
        price = float(record["price"])
        return {**record, "price": price,
                "product_name": record["product_name"].title(), "tax": price * 0.2}


# New pipeline: only the XML-specific parts are written
class XMLPipeline(DataPipeline):
    source_type = "XML"
    required_fields = ("order_id", "amount")
    SAMPLE = """<orders>
        <order><order_id>9001</order_id><customer>eve</customer><amount>59.90</amount></order>
        <order><order_id>9002</order_id><customer>frank</customer><amount>12.50</amount></order>
    </orders>"""

    def extract(self) -> list[dict]:
        print("Extracting data from XML...")
        root = ET.fromstring(self.SAMPLE)
        return [{child.tag: child.text for child in order} for order in root]

    def transform(self, record: dict) -> dict:
        return {"order_id": int(record["order_id"]),
                "customer": record["customer"].capitalize(),
                "amount": float(record["amount"])}

    def before_run(self) -> None:           # using a hook
        print(f"[hook] XML pipeline starting at {time.strftime('%H:%M:%S')}")


if __name__ == "__main__":
    for title, pipeline in [("CSV", CSVPipeline("data/users.csv")),
                            ("API", APIPipeline("https://api.example.com/users")),
                            ("DATABASE", DatabasePipeline("postgresql://localhost/mydb")),
                            ("XML (NEW!)", XMLPipeline("data/orders.xml"))]:
        print(f"RUNNING {title} PIPELINE")
        print("=" * 70)
        result = pipeline.run()
        print(f"\n{result}\n")
