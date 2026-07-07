import os

from pipelinedata.extractor import JSONExtractor, CSVExtractor
from pipelinedata.loader import MultiLoader, CSVLoader, JSONLoader
from pipelinedata.pipeline import Pipeline
from pipelinedata.transform import StudentTransformer


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print("═" * 50)
    print("   ETL Student Data Pipeline")
    print("═" * 50)


def pick_extractor():
    print("\n── Input source ──────────────────────────")
    print("  1. CSV file  (default: data/raw/students_raw.csv)")
    print("  2. JSON file  (default: data/raw/students_raw.JSON)")
    choice = input("\nPick source [1/2] (default 1): ").strip() or "1"

    if choice == "2":
        path = input("JSON path (default: data/raw/students_raw.json): ").strip()
        path = path or "data/raw/students_raw.json"
        print(path)
        return JSONExtractor(path)
    else:
        path = input("CSV path (default: data/raw/students_raw.csv): ").strip()
        path = path or "data/raw/students_raw.csv"
        return CSVExtractor(path)


def pick_loader():
    print("\n── Output format ─────────────────────────")
    print("  1. CSV only")
    print("  2. JSON only")
    print("  3. Both CSV + JSON  (default)")
    choice = input("\nPick format [1/2/3] (default 3): ").strip() or "3"

    csv_path  = "data/output/students_clean.csv"
    json_path = "data/output/students_clean.json"

    if choice == "1":
        return CSVLoader(csv_path)
    elif choice == "2":
        return JSONLoader(json_path)
    else:
        return MultiLoader([CSVLoader(csv_path), JSONLoader(json_path)])


def run_pipeline():
    clear()
    print_banner()

    try:
        extractor   = pick_extractor()
        loader      = pick_loader()
        transformer = StudentTransformer()

        pipeline = Pipeline(
            extractor   = extractor,
            transformer = transformer,
            loader      = loader,
            name        = "Student Data Pipeline"
        )

        print("\n── Pipeline config ───────────────────────")
        print(f"  extractor  : {extractor}")
        print(f"  transformer: {transformer}")
        print(f"  loader     : {loader}")

        confirm = input("\nRun pipeline? [y/n] (default y): ").strip().lower() or "y"
        if confirm != "y":
            print("Cancelled.")
            return

        pipeline.run_pipeline()

        meta = pipeline.get_meta()
        print(f"Drop rate : {meta['rows_dropped']}/{meta['rows_extracted']} rows dropped")
        print(f"Output    : data/output/")
        print(f"Logs      : logs/\n")

    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("Check your file path and try again.\n")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}\n")


def show_logs():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        print("\nNo logs found yet — run the pipeline first.\n")
        return

    logs = sorted(os.listdir(log_dir), reverse=True)
    if not logs:
        print("\nNo log files found.\n")
        return

    print(f"\n── Recent logs ───────────────────────────")
    for i, log in enumerate(logs[:5], 1):      # show last 5 runs
        print(f"  {i}. {log}")

    choice = input("\nView a log? Enter number (or press Enter to skip): ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(logs):
            filepath = os.path.join(log_dir, logs[idx])
            print(f"\n── {logs[idx]} ────────────────────────")
            with open(filepath, "r", encoding="utf-8") as f:
                print(f.read())


def main():
    while True:
        clear()
        print_banner()
        print("\n  1. Run pipeline")
        print("  2. View logs")
        print("  3. Exit")
        choice = input("\nPick an option [1/2/3]: ").strip()

        if choice == "1":
            run_pipeline()
            input("Press Enter to continue...")
        elif choice == "2":
            show_logs()
            input("Press Enter to continue...")
        elif choice == "3":
            print("\nBye!\n")
            break
        else:
            print("Invalid option — try again.")


if __name__ == "__main__":
    main()