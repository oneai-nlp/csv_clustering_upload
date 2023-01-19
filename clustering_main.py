from datetime import datetime
import itertools
import typing
import oneai
import csv


ColumnIndex = typing.Union[int, str]


def upload_csv_to_collection(
    source_file_path: str,
    collection_name: str,
    *,
    main_column: ColumnIndex = None,  # column 0 if None
    timestamp_column: ColumnIndex = None,  # ignored if None
    timestamp_format: str = "%a %b %d %H:%M:%S %Y",
    column_blacklist: list[ColumnIndex] = None,
    skills: list[str] = None,
    input_skill: str = None,
    row_range_start: int = 0,
    row_range_end: int = None,
    encoding: str = "utf-8",
):
    if input_skill is not None and input_skill not in skills:
        raise ValueError("input_skill must be in skills")

    pipeline = oneai.Pipeline(
        ([oneai.Skill(s) for s in skills] if skills else [])
        + [oneai.skills.Clustering(collection=collection_name, input_skill=input_skill)]
    )

    with open(source_file_path, "r", newline="", encoding=encoding) as inputf:
        reader = csv.reader(inputf)
        header = next(reader)
        indices = list(range(len(header)))

        column_blacklist = column_blacklist or []
        column_blacklist += [main_column, timestamp_column]
        if main_column is None:
            main_column = 0
            column_blacklist.append(0)
        elif isinstance(main_column, str):
            main_column = header.index(main_column)
            if main_column == -1:
                raise ValueError("main_column not found in header")
        if isinstance(timestamp_column, str):
            timestamp_column = header.index(timestamp_column)
            if timestamp_column == -1:
                raise ValueError("timestamp_column not found in header")
        column_blacklist = [
            header.index(c) if isinstance(c, str) else c for c in column_blacklist
        ]

        pipeline.run_batch(
            oneai.Input(
                row[main_column],
                timestamp=datetime.strptime(row[timestamp_column], timestamp_format)
                if timestamp_column is not None
                else None,
                metadata={
                    k: v
                    for (k, v, i) in zip(header, row, indices)
                    if i not in column_blacklist
                },
            )
            for row in itertools.islice(
                reader, max(row_range_start - 1, 0), row_range_end
            )
        )


oneai.api_key = "caa23bd6-068a-44f7-bf71-612f17ac4779"
oneai.multilingual = True
oneai.MAX_CONCURRENT_REQUESTS = 5
oneai.DEBUG_RAW_RESPONSES = True

# upload_csv_to_collection(
#     "./test.csv",
#     "csv_upload_test_v3",
#     row_range_end=10,
#     encoding="ISO-8859-1",
#     column_blacklist=["response"],
#     skills=["sentiments"],
# )
