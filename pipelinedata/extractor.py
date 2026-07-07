import csv
import json
import os
from abc import ABC, abstractmethod

from utils.logger import Logger


class BaseExtractor(ABC):
    def __init__(self, filepath, logger=None):
        self.filepath = filepath
        self.logger = logger or Logger("Extractor")
        self._file_validation()

    # Validate File Path

    def _file_validation(self):
        if not os.path.exists(self.filepath):
            self.logger.error(f"File not found: {self.filepath}")
            raise FileNotFoundError(f"File not found: {self.filepath}")

    # extract abs method
    @abstractmethod
    def extract(self): # need to implement in other class
        pass

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.filepath}"

class CSVExtractor(BaseExtractor):
    def extract(self):
        rows = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean_row = {k: v.strip() for k, v in row.items()}
                rows.append(clean_row)
        self.logger.info(f"{len(rows)} rows were extracted")
        return rows

class JSONExtractor(BaseExtractor):
    """Extracts rows from a JSON file (expects a list of objects)"""

    def extract(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            self.logger.error("JSON must contain a list at top level")
            raise ValueError("JSON file must contain a list of objects at the top level.")
        self.logger.info(f"[Extractor] Extracted {len(data)} rows from '{self.filepath}'")
        return data