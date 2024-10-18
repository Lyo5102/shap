import secrets
import string

import pandas as pd

###定数###
N = 100  # 被験者数


###パスワード生成関数###
def pass_gen(size=12):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(secrets.choice(chars) for x in range(size))


###idとパスワードを生成###
passwords = pd.DataFrame(columns=["id", "password"])

for i in range(N):
    id = "user" + str(i + 1)
    password = pass_gen(6)
    passwords = passwords.append({"id": id, "password": password}, ignore_index=True)
# print(passwords)

###csvファイルへ書き込み###
passwords.to_csv("logininfo.csv", index=False)
