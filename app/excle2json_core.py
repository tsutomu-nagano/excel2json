import yaml
import openpyxl
import pandas as pd
import re
import json




def getcell(wb, info):


    sheet = info["sheet"]
    address = info["address"]

    return(wb[sheet][address].value)

def gettable(src, info):


    sheet = info["sheet"]
    address = info["address"]


    m = re.match("(?P<col>[A-Z]+)(?P<row>[0-9]+)", address)
    srow = int(m.group("row"))


    # 使用するヘッダーを決める処理
    df = pd.read_excel(src, sheet_name=sheet, skiprows=srow - 2, header = None)
    usecols = [index for index, value in enumerate(df.loc[1].tolist()) if not pd.isna(value)]
    
    df = pd.read_excel(src, sheet_name=sheet, skiprows=srow - 1,  usecols = usecols
                    ).ffill(
                    ).fillna("")
    
    if "colmap" in info.keys():
        df = df.rename(columns = {colmap["ja"]:colmap["var"] for colmap in info["colmap"]})

    return([row.to_dict() for index, row in df.iterrows()])


def getlist(wb, src, info):

    sheet_ptn = info["sheet"]
    listitem = info["listitem"]

    return([xls_with_yaml2json_core(listitem, wb, src, sheet) for sheet in wb.sheetnames if re.match(sheet_ptn, sheet)])


def xls_with_yaml2json_core(y, wb, src, sheet = ""):
    if isinstance(y, dict):
        if "type" in y.keys():
            conv_type = y["type"]

            if sheet != "":
                y["sheet"] = sheet

            if conv_type == "cell":
                y = getcell(wb, y)
            
            if conv_type == "table":
                y = gettable(src, y)

            if conv_type == "list":
                y = getlist(wb, src, y)

        else:
            for k in y.keys():
                y[k] = xls_with_yaml2json_core(y[k], wb, src, sheet)

    return(y)




def xls_with_yaml2json(src, config):
    with open(config, 'r') as ymlf:
        json_ = xls_with_yaml2json_core(
            y = yaml.safe_load(ymlf),
            wb = openpyxl.load_workbook(src),
            src = src
        )
        return(json_)

