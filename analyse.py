import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import os, argparse, time, logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s",
    handlers = [
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

parser = argparse.ArgumentParser()
parser.add_argument("--region", default=None, help="篩選地區，例如 HK 或 TW")
args = parser.parse_args()

load_dotenv()

df = pd.read_csv("data.csv")
if args.region:
    df = df[df["region"] == args.region]
    print(f"📍 篩選地區：{args.region}")

df["revenue"] = df["price"] * df["sold"]
df["stock_left"] = df["stock"] - df["sold"]

print(df)

# 按類別統計
category_summary = df.groupby("category").agg(
    total_revenue = ("revenue", "sum"),
    avg_sold = ("sold", "mean"),
    total_stock_left = ("stock_left", "sum")
).reset_index()

print(category_summary)

# 庫存預警：stock_left 少於 5 的產品
low_stock = df[df["stock_left"] < 5].sort_values("stock_left")

print("\n庫存預警：")
print(low_stock[["product","region","stock_left"]])


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

analysis_text = f"""
以下是供應鏈分析數據：

各類別表現：
{category_summary.to_string()}

庫存預警產品：
{low_stock[["product", "region", "stock_left"]].to_string()}
"""


def call_api_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="baidu/qianfan-ocr-fast:free",
                messages=messages
            )
            logging.info("API 呼叫成功")
            return response.choices[0].message.content
        except Exception as e:
            wait = 2 ** attempt
            logging.warning(f"第{attempt+1}次失敗，等待{wait}秒後重試... 錯誤：{e}")
            time.sleep(wait)
    raise Exception("重試次數已用完")

messages = [
    {"role": "system", "content": "你是一個供應鏈分析師，用繁體中文給出簡潔的業務建議。"},
    {"role": "user", "content": f"請根據以下數據給出分析報告和建議：\n{analysis_text}"}
]
report = call_api_with_retry(messages)

with open("report.md", "w", encoding="utf-8") as f:
    f.write("# 供應鏈分析報告\n\n")
    f.write("## 各類別表現\n\n")
    f.write(category_summary.to_string())
    f.write("\n\n## 庫存預警\n\n")
    f.write(low_stock[["product", "region", "stock_left"]].to_string())
    f.write("\n\n## AI 建議\n\n")
    f.write(report)

print("\n✅ 報告已儲存至 report.md")