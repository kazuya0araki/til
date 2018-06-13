# -*- coding:utf-8 -*-
import json
import csv
import requests
import pandas as pd
from pandas.io.json import json_normalize

URI = "https://bdash.bizreach.jp/api/queries/search"
API_KEY = "jVcY06dM5Fh9XwApEnsLofWz2IyK8DAD3ZErEH6J"


# クエリ一覧取得
def queries():
    # GETパラメーター設定
    params = {"api_key": API_KEY}
    # Re:dash API実行
    response = requests.get(URI, params=params)
    # HTTPコードで分岐させる
    if response.status_code == 200:
        # HTTPコード200の場合、CSV作成処理
        # レスポンスからJSONを取得 & 正規化
        queries_result = json_normalize(json.loads(response.text))
        # JSONから取得対象のキーを抽出
        fields = ["id", "name", "description", "created_at", "retrieved_at", "runtime", "user.name", "schedule", "is_archived", "is_draft", "query"]
        # DataFrameにJSONデータを投入
        df = pd.DataFrame(queries_result, columns=fields)
        # idでソート
        df = df.sort_values(by=["id"], ascending=True)
        # CSV出力
        df.to_csv("result.csv", index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")
    else:
        # HTTPコード200以外の場合、エラー処理
        print("ERROR: %d" % response.status_code)


if __name__ == '__main__':
    queries()
