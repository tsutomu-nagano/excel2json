
from excel2json import Excel2JSON

import os
import json

def test_標準的な変換処理():

    src = "tests/resource/001/test.xlsx"
    config = "tests/resource/001/convert.yaml"
    with open("tests/resource/001/expected.json") as f:
        expected = json.load(f)

    ret = Excel2JSON.xls_with_yaml2json(src, config)

    assert ret == expected

def test_table変換する際の列名にブランク列が途中に含まれる場合():

    src = "tests/resource/002/test.xlsx"
    config = "tests/resource/002/convert.yaml"
    with open("tests/resource/002/expected.json") as f:
        expected = json.load(f)

    ret = Excel2JSON.xls_with_yaml2json(src, config)

    assert ret == expected


def test_table変換する際の列名に改行コードが含まれる場合():

    src = "tests/resource/003/test.xlsx"
    config = "tests/resource/003/convert.yaml"
    with open("tests/resource/003/expected.json") as f:
        expected = json.load(f)

    ret = Excel2JSON.xls_with_yaml2json(src, config)

    assert ret == expected


def test_table変換する際の列名を正規表現で一致させて置換する場合():

    src = "tests/resource/004/test.xlsx"
    config = "tests/resource/004/convert.yaml"
    with open("tests/resource/004/expected.json") as f:
        expected = json.load(f)

    ret = Excel2JSON.xls_with_yaml2json(src, config)

    assert ret == expected



