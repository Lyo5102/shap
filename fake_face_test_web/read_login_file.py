import csv


def read_login_file(filename="logininfo.csv"):
    datadic = {}
    with open(filename, newline="") as f:
        c = csv.reader(f)
        header = next(c)  # ヘッダを読み飛ばす
        for i in c:
            datadic[i[0]] = i[1]
    f.close()
    return datadic
