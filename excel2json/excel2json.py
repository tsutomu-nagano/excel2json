import yaml
import openpyxl
import pandas as pd
import re
import json
import unicodedata
import sys
import copy

class Excel2JSON():

    @staticmethod
    def __getcell(wb, info):


        sheet = info["sheet"]
        address = info["address"]

        return(str(wb[sheet][address].value))

    @staticmethod
    def __rename_header(df, colmaps):

        # 改行コードは削除
        df.columns = [re.sub(r"(\r\n|\n|\r)", "", column) for column in df.columns.values]

        # 文字列一致で置換
        df = df.rename(columns = {colmap["ja"]["text"]:colmap["var"] for colmap in colmaps if "text" in colmap["ja"]})

        # 正規表現で置換
        headers  = df.columns.values
        patterns = {colmap["ja"]["re"]:colmap["var"] for colmap in colmaps if "re" in colmap["ja"]}
        if len(patterns) >= 1:
            for pattern, var in patterns.items():
                
                headers = [re.sub(pattern, var, h) for h in headers]
            
            df.columns = headers

        return(df)

    @staticmethod
    def __gettable(src, info):


        sheet = info["sheet"]
        address = info["address"]

        m = re.match("(?P<col>[A-Z]+)(?P<row>[0-9]+)", address)
        srow = int(m.group("row"))


        # 使用するヘッダーを決める処理
        df = pd.read_excel(src, sheet_name=sheet, skiprows=srow - 2, header = None)
        usecols = [index for index, value in enumerate(df.loc[1].tolist()) if not pd.isna(value)]
        
        df = pd.read_excel(src, sheet_name=sheet, skiprows=srow - 1,  usecols = usecols, dtype=str
                        ).fillna("")
        

        # ヘッダーの変換
        if "colmap" in info:
            colmaps = info["colmap"]

            df = Excel2JSON.__rename_header(df, colmaps)

            formats = {colmap["var"]:colmap["format"] for colmap in colmaps if "format" in colmap}

            for col_var, format in formats.items():
                if "wide_to_narrow" in format:
                    df[col_var] = df[col_var].map(lambda x : unicodedata.normalize("NFKC", x))



        return([row.to_dict() for index, row in df.iterrows()])


    @staticmethod
    def __getlist(wb, src, info):

        sheet_ptn = info["sheet"]

        # for sheet in wb.sheetnames:
        #     if re.match(sheet_ptn, sheet):
        #         print(sheet)
        #         print(copy.deepcopy(info["listitem"]))
        #         print(Excel2JSON.__xls_with_yaml2json_core(copy.deepcopy(info["listitem"]), wb, src, sheet))

        items = [Excel2JSON.__xls_with_yaml2json_core(copy.deepcopy(info["listitem"]), wb, src, sheet) for sheet in wb.sheetnames if re.match(sheet_ptn, sheet)]

        return(items)


    @staticmethod
    def __xls_with_yaml2json_core(y, wb, src, sheet = ""):
        if isinstance(y, dict):
            if "type" in y:
                conv_type = y["type"]

                if sheet != "":
                    y["sheet"] = sheet

                if conv_type == "cell":
                    y = Excel2JSON.__getcell(wb, y)
                
                if conv_type == "table":
                    y = Excel2JSON.__gettable(src, y)

                if conv_type == "list":
                    y = Excel2JSON.__getlist(wb, src, y)

            else:
                for k in y:
                    y[k] = Excel2JSON.__xls_with_yaml2json_core(y[k], wb, src, sheet)

        return(y)




    @classmethod
    def xls_with_yaml2json(cls, src, config):
        with open(config, 'r') as ymlf:
            json_ = cls.__xls_with_yaml2json_core(
                y = yaml.safe_load(ymlf),
                wb = openpyxl.load_workbook(src),
                src = src
            )
            return(json_)


if __name__ == "__main__":
    args = sys.argv

    src = args[1]
    config = args[2]
    dest = args[3]

    data = Excel2JSON.xls_with_yaml2json(src, config)
    
    with open(dest, 'w') as f:
        json.dump(data, f, indent=2)
