import csv


def read_question_csv(file_path, encoding="utf-8-sig", add_index=True):
    print(file_path)
    rows = []
    with open(file_path, encoding=encoding) as f:
        header = [x.strip() for x in next(f).split(",")]
        reader = csv.reader(f, delimiter=",")
        for i, row in enumerate(reader):
            if add_index:
                row.insert(0, f"{i + 1}")
            rows.append(row)
    return header, rows


def init_result_file(save_path, results_header):
    save_path.parent.mkdir(exist_ok=True)
    with open(save_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(results_header)


def record_result(save_path, result):
    with open(save_path, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(result)
