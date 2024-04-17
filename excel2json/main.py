# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPDF, renderPM

from typing import List
from fastapi import Depends, FastAPI, File, UploadFile, Form, HTTPException, Query
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, PlainTextResponse, FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from pathlib import Path

import pandas as pd
import json
import datetime
import io
import sys
import os
import re
import yaml
import tempfile
import shutil
import requests
import zipfile

from openpyxl import load_workbook

from pandas import json_normalize

import excel2json
import exceptions

tags_metadata = [
    {
        "name": "convert",
        "description": "変換する"
    },

]


app = FastAPI(
    title="Excel 2 json",
    description="ExcelファイルをJSONに変換するAPI",
    version="0.0.1",
    # contact={
    #     "name": "Deadpoolio the Amazing",
    #     "url": "http://x-force.example.com/contact/",
    #     "email": "dp@x-force.example.com",
    # },
    # license_info={
    #     "name": "che 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    # },
    openapi_tags=tags_metadata
)




@app.post(
        "/excel2json",
        summary="変換定義（YAML）ファイルを基にExcelファイルをJSONに変換します",
        tags = ["convert"])
def excel_to_json(
    template_file: UploadFile = File(...),
    conversion_config_file: UploadFile = File(...)
    ):

    with tempfile.NamedTemporaryFile(delete=True, suffix = Path(template_file.filename).suffix) as t1,\
         tempfile.NamedTemporaryFile(delete=True, suffix = Path(conversion_config_file.filename).suffix) as t2:

        shutil.copyfileobj(template_file.file, t1)
        shutil.copyfileobj(conversion_config_file.file, t2)

        # これ実行しないとなぜか戻り値がNoneになる・・・
        y = yaml.safe_load(t2)

        item = excel2json.Excel2JSON.xls_with_yaml2json(src = t1.name, config = t2.name)
        json_compatible_item_data = jsonable_encoder(item)
        return JSONResponse(content=json_compatible_item_data)

@app.get(
        "/sample",
        summary="処理に必要な変換定義（YAML）ファイルと簡単なExcelファイルを取得します",
        tags = ["convert"])
def get_sample():

    with tempfile.NamedTemporaryFile(delete=False, dir =".", suffix = ".zip") as t1:

        with zipfile.ZipFile(t1.name, 'w') as myzip:
            myzip.write("sample/convert.yaml")
            myzip.write('sample/test.xlsx')

        return FileResponse(path=t1.name, filename="sample.zip")


