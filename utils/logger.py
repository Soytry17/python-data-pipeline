import os
from datetime import datetime
class Logger:

    LEVELS = {"INFO": "ℹ", "WARNING": "⚠", "ERROR": "✖", "SUCCESS": "✔"}

    def __init__(self, name="Pipeline", log_dir="logs"):
        self.name    = name
        self.log_dir = log_dir
        self._logs   = []                     # in-memory log history
        self._ensure_log_dir()
        self.log_file = self._create_log_file()


    def _ensure_log_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _create_log_file(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename  = f"{self.log_dir}/{self.name}_{timestamp}.log"
        return filename


    def _log(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        icon      = self.LEVELS.get(level, "•")
        entry     = f"[{timestamp}] {icon} {level:<8} | {self.name} | {message}"

        print(entry)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry + "\n")

        self._logs.append({
            "timestamp": timestamp,
            "level":     level,
            "message":   message
        })

    def info(self, message):
        self._log("INFO", message)

    def warning(self, message):
        self._log("WARNING", message)

    def error(self, message):
        self._log("ERROR", message)

    def success(self, message):
        self._log("SUCCESS", message)

    def get_logs(self):
        return self._logs

    def summary(self):
        total    = len(self._logs)
        warnings = sum(1 for l in self._logs if l["level"] == "WARNING")
        errors   = sum(1 for l in self._logs if l["level"] == "ERROR")
        print(f"\n{'─'*50}")
        print(f"  LOG SUMMARY — {self.name}")
        print(f"{'─'*50}")
        print(f"  total entries  : {total}")
        print(f"  warnings       : {warnings}")
        print(f"  errors         : {errors}")
        print(f"  log file       : {self.log_file}")
        print(f"{'─'*50}\n")

    def __str__(self):
        return f"Logger(name={self.name}, file={self.log_file})"