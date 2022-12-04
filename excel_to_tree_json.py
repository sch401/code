import pandas as pd
import re


dat = pd.read_excel("dataone.xlsx")

f = open("name.txt", mode="w")


def rollup2(x):
    return x.set_index(["latin_name"])[["option_one"]].to_dict(orient="records")


def rollup3(x):
    return (
        x.groupby(["latin_name"]).apply(rollup2).reset_index().to_dict(orient="records")
    )


def rollup4(x):
    return (
        x.groupby(["common_name"])
        .apply(rollup3)
        .reset_index()
        .to_dict(orient="records")
    )


df = dat.groupby(["category"]).apply(rollup4)

res = df.reset_index().to_dict(orient="records")
reschar0 = str(res)
reschar = re.sub("'category'", "value: 'category',\"label\"", reschar0)
reschar = re.sub("'common_name'", "value: 'common_name',\"label\"", reschar)
reschar = re.sub("'latin_name'", "value: 'latin_name',\"label\"", reschar)
reschar = re.sub("'option_one'", "value: 'option_one',\"label\"", reschar)
reschar2 = re.sub("0:", "children:", reschar)
reschar3 = re.sub(r"(children: \{\'option_one\'\:)", r"value:", reschar2)
reschar4 = re.sub("\{\{", "\{", reschar3)
reschar5 = re.sub("\}\}", "}", reschar4)
reschar6 = re.sub("children", '"children"', reschar5)
reschar7 = re.sub("value", '"value"', reschar6)
reschar8 = re.sub("'", '"', reschar7)

f.write(reschar8)
f.close()
