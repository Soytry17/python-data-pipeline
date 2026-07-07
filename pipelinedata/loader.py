from abc import ABC, abstractmethod
import csv
import json
import os

from utils.logger import Logger


# base class handles the guard
class BaseLoader(ABC):
    def __init__(self, filepath, logger=None):
        self.filepath = filepath
        self.logger = logger or Logger("Loader")
        self._ensure_folder()

    def _ensure_folder(self):
        folder = os.path.dirname(self.filepath)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
            self.logger.info(f"[Loader] Created folder: '{folder}'")

    def load(self, rows):
        if not rows:                          # shared guard lives here
            self.logger.warning("[Loader] No rows to write — skipping.")
            return
        self._write(rows)                     # delegates to child

    @abstractmethod
    def _write(self, rows):                   # children implement _write, not load
        pass

    def __str__(self):
        return f"{self.__class__.__name__} → {self.filepath}"


# children are now much cleaner
class CSVLoader(BaseLoader):
    def _write(self, rows):
        rows = self._flatten_projects(rows)
        fieldnames = list(rows[0].keys())
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        self.logger.info(f"[Loader] Wrote {len(rows)} rows to '{self.filepath}'")


    def _flatten_projects(self, rows):
        flattened_rows = []
        for row in rows:
            row = row.copy()
            if isinstance(row.get("projects"), list):
                row["projects"] = ", ".join(row["projects"])
            flattened_rows.append(row)
        return flattened_rows


class JSONLoader(BaseLoader):
    def _write(self, rows):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
        self.logger.info(f"[Loader] Wrote {len(rows)} rows to '{self.filepath}'")

class MultiLoader(BaseLoader):

    def __init__(self, loaders):
        self.loaders = loaders

    def _write(self, rows):
        for loader in self.loaders:
            loader.load(rows)

    def __str__(self):
        targets = " + ".join(str(l) for l in self.loaders)
        return f"MultiLoader → [{targets}]"