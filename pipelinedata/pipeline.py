import time

from pipelinedata.extractor import BaseExtractor
from pipelinedata.loader import BaseLoader
from pipelinedata.transform import BaseTransform
from utils.logger import Logger


class Pipeline:

    def __init__(self, extractor, transformer, loader, name = "ETL Pipeline", logger = None):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self._run_metadata = {}
        self.name = name
        self.logger = logger or Logger(name.replace(" ", "_"))

    # Validate

        # inject shared logger into every stage
        self.extractor.logger = self.logger
        self.transformer.logger = self.logger
        if hasattr(self.loader, "logger"):
            self.loader.logger = self.logger
        if hasattr(self.loader, "loaders"):
            for l in self.loader.loaders:
                l.logger = self.logger

    def _validate_pipeline(self):
        if not isinstance(self.extractor, BaseExtractor):
            self.logger.error("The extractor must be an instance of BaseExtractor")
            raise TypeError("The extractor must be an instance of BaseExtractor")
        if not isinstance(self.transformer, BaseTransform):
            self.logger.error("The transformer must be an instance of BaseTransform")
            raise TypeError("The transformer must be an instance of BaseTransform")
        if not isinstance(self.loader, BaseLoader):
            self.logger.error("The loader must be an instance of BaseLoader")
            raise TypeError("The loader must be an instance of BaseLoader")

    def run_pipeline(self):

        self._validate_pipeline()

        print(f"\n{'═' * 50}")
        print(f"  {self.name}")
        print(f"{'═' * 50}")

        total_start_time = time.time()

        # Extract Data

        print(f"\n[1/3] Extracting...")
        t0 = time.time()
        raw_data = self.extractor.extract()
        extract_time = round(time.time() - t0, 3)

        # Transform Data

        print(f"\n[2/3] Transforming...")
        t0 = time.time()
        cleaned_data = self.transformer.transform(raw_data)
        transform_time = round(time.time() - t0, 3)


        print(f"\n[3/3] Loading...")
        t0 = time.time()
        self.loader.load(cleaned_data)
        loaded_time = round(time.time() - t0, 3)


        total_time = round(time.time() - total_start_time, 3)

        self._run_metadata ={
            "rows_extracted" : len(raw_data),
            "rows_dropped" : len(cleaned_data),
            "rows_loaded" : len(cleaned_data) - len(raw_data),
            "extract_time" : extract_time,
            "transform_time" : transform_time,
            "load_time" : loaded_time,
            "total_time" : total_time,
        }

        self._print_run_summary()
        return cleaned_data

    def _print_run_summary(self):
        m = self._run_metadata
        print(f"\n{'─' * 50}")
        print(f"  PIPELINE RUN COMPLETE")
        print(f"{'─' * 50}")
        print(f"  rows extracted  : {m['rows_extracted']}")
        print(f"  rows dropped    : {m['rows_dropped']}")
        print(f"  rows loaded     : {m['rows_loaded']}")
        print(f"{'─' * 50}")
        print(f"  extract time    : {m['extract_time']}s")
        print(f"  transform time  : {m['transform_time']}s")
        print(f"  load time       : {m['load_time']}s")
        print(f"  total time      : {m['total_time']}s")
        print(f"{'─' * 50}\n")

    def get_meta(self):
        return self._run_metadata

    def __str__(self):
        return (
            f"Pipeline: {self.name}\n"
            f"  extractor   : {self.extractor}\n"
            f"  transformer : {self.transformer.__class__.__name__}\n"
            f"  loader      : {self.loader}"
        )