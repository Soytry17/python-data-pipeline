from utils.logger import Logger
class BaseTransform:
    def __init__(self, rules=None, logger=None):
        self.rules = rules or []
        self.logger = logger or Logger("Transformer")
        self._summary = {
            "total_in": 0,
            "dropped": 0,
            "fixed": 0,
            "total_out": 0,
        }

    def transform(self, rows):
        self.logger.error("subclasses of BaseTransform must implement transform")
        raise NotImplementedError("subclasses of BaseTransform must implement transform")

    def get_summary(self):
        return self._summary


class StudentTransformer(BaseTransform):
    VALID_TYPES = {"regular", "ds"}
    SCORE_COLS = ["score1", "score2", "score3"]

    def _should_drop(self, row):

        if not row.get("name"):
            self.logger.warning(f"dropping {row}")
            return True

        score_raw = [row.get(c, "") for c in self.SCORE_COLS]

        if all(s == "" for s in score_raw):
            self.logger.info(f"  [drop] all scores missing → {row['name']}")
            return True

        return False

    def _rule_strip_whitespace(self, row):
        return {k: v.strip() if isinstance(v, str) else v
        for k, v in row.items()
        }

    def _rule_convert_scores(self, row):
        for col in self.SCORE_COLS:
            raw = row.get(col, "")
            if raw == "":
                row[col] = None
            else:
                try:
                    temp = float(raw)
                    if temp < 0 or temp > 100:
                        self.logger.warning(f"  [fix] invalid score {row['name']}")
                        temp = 0
                    row[col] = temp
                except:
                    self.logger.error(f"  [fix] unreadable score {row['name']}")
                    row[col] = None
        return row

    def _rule_fill_missing_scores(self, row):

        scores = [row[c] for c in self.SCORE_COLS if row[c] is not None]
        mean = round(sum(scores) / len(scores), 2) if scores else 0.0

        for col in self.SCORE_COLS:
            if row[col] is None:
                self.logger.warning(f"  [fix] missing {col} for '{row['name']}' → filled with mean {mean}")
                row[col] = mean

        return row

    def _rule_fix_type(self, row):

        if row.get("type", "").lower() not in self.VALID_TYPES:
            self.logger.warning(f"  [fix] unknown type '{row.get('type')}' for '{row['name']}' → set to 'regular'")
            row["type"] = "regular"

        return row

    def _rule_parse_project(self, row):

        raw = row.get("projects", "")
        if isinstance(raw, str) and raw:
            row["projects"] = [p.strip() for p in raw.split(",") if p.strip()]
        else:
            row["projects"] = []

        return row

    def _rule_add_average(self, row):

        scores = [row[c] for c in self.SCORE_COLS if row[c] is not None]
        avg = round(sum(scores) / len(scores), 2) if scores else 0.0
        row["average"] = avg

        return row

    def _rule_add_grade(self, row):
        avg = row.get("average", 0.0)
        if avg >= 90:
            row["grade"] = "A"
        elif avg >= 75:
            row["grade"] = "B"
        elif avg >= 60:
            row["grade"] = "C"
        else:
            row["grade"] = "F"

        return row

    def _print_summary(self):
        s = self._summary
        print(f"\n[Transformer] Done.")
        print(f"  rows in    : {s['total_in']}")
        print(f"  dropped    : {s['dropped']}")
        print(f"  cleaned    : {s['fixed']}")
        print(f"  rows out   : {s['total_out']}")

    def transform(self, rows):
        self._summary["total_in"] = len(rows)
        cleaned_rows = []

        for row in rows:
            row = self._rule_strip_whitespace(row)

            if self._should_drop(row):
                self._summary["dropped"] += 1
                continue

            # fix rules — repair the row in place

            row = self._rule_convert_scores(row)
            row = self._rule_fill_missing_scores(row)
            row = self._rule_fix_type(row)
            row = self._rule_parse_project(row)


            # add value

            row = self._rule_add_average(row)
            row = self._rule_add_grade(row)

            self._summary["total_in"] += 1
            cleaned_rows.append(row)
        self._summary["total_in"] = len(cleaned_rows)
        return cleaned_rows