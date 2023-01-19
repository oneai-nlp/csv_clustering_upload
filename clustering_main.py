from datetime import datetime
import itertools
import oneai
import csv


def upload_csv_to_collection(
    source_file_path: str,
    collection_name: str,
    *,
    main_column: str = None,  # column 0 if None
    timestamp_column: str = None,  # ignored if None
    timestamp_format: str = "%a %b %d %H:%M:%S %Y",
    skills: list[str] = None,
    input_skill: str = None,
    row_range_start: int = 0,
    row_range_end: int = None,
    encoding: str = "utf-8",
):
    if input_skill is not None and input_skill not in skills:
        raise ValueError("input_skill must be in skills")

    pipeline = oneai.Pipeline(
        list(skills.map(oneai.Skill.__new__) if skills else [])
        + [oneai.skills.Clustering(collection=collection_name, input_skill=input_skill)]
    )

    with open(source_file_path, "r", newline="", encoding=encoding) as inputf:
        reader = csv.reader(inputf)
        header = next(reader)
        indices = list(range(len(header)))
        if main_column is None:
            main_column = 0
        elif isinstance(main_column, str):
            main_column = header.index(main_column)
            if main_column == -1:
                raise ValueError("main_column not found in header")
        if isinstance(timestamp_column, str):
            timestamp_column = header.index(timestamp_column)
            if timestamp_column == -1:
                raise ValueError("timestamp_column not found in header")

        batch = [
            oneai.Input(
                row[main_column],
                timestamp=datetime.strptime(row[timestamp_column], timestamp_format)
                if timestamp_column is not None
                else None,
                metadata={
                    k: v
                    for (k, v, i) in zip(header, row, indices)
                    if i not in (main_column, timestamp_column)
                },
            )
            for row in itertools.islice(
                reader, max(row_range_start - 1, 0), row_range_end
            )
        ]
        pipeline.run_batch(batch)


oneai.api_key = "9595c022-b1f7-496e-a215-c5ee0ff9d65d"
oneai.URL = "https://staging.oneai.com"
oneai.multilingual = True
oneai.MAX_CONCURRENT_REQUESTS = 5

upload_csv_to_collection(
    "./test.csv", "csv_upload_test_v1", row_range_end=10, encoding="ISO-8859-1"
)
