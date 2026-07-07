from pipelinedata.extractor import CSVExtractor
from pipelinedata.loader import MultiLoader, CSVLoader, JSONLoader
from pipelinedata.pipeline import Pipeline
from pipelinedata.transform import StudentTransformer

pipeline = Pipeline(
    extractor   = CSVExtractor("../data/raw/students_raw.csv"),
    transformer = StudentTransformer(),
    loader      = MultiLoader([
        CSVLoader("../data/output/students_clean.csv"),
        JSONLoader("../data/output/students_clean.json"),
    ]),
    name = "Student Data Pipeline"
)

pipeline.run_pipeline()