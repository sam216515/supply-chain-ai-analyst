# 📦 Supply Chain AI Analyst

A Python CLI tool that analyses supply chain data using pandas and automatically generates business reports powered by AI.

## 🎯 What It Does

1. Reads inventory and sales data from CSV
2. Calculates revenue, stock levels, and low-stock alerts using pandas
3. Sends the analysis to an LLM API
4. AI generates a structured business report with recommendations
5. Saves the report as a Markdown file

## 🚀 Quick Start

```bash
# Install dependencies
pip install pandas python-dotenv openai

# Set up API key
cp .env.example .env
# Add: OPENROUTER_API_KEY=your_key_here

# Run full analysis
python analyse.py

# Filter by region
python analyse.py --region HK
python analyse.py --region TW
```

## 📊 Sample Output

```
📍 篩選地區：HK
      product     category region  price  stock  sold  revenue  stock_left
0       Apple        Fruit     HK     10     50    45      450           5
...

⚠️ 庫存預警：
      product region  stock_left
5  Headphones     HK           0
3      Laptop     HK           1

2026-05-09 16:46:00 [INFO] API 呼叫成功
✅ 報告已儲存至 report.md
```

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| pandas | Data analysis — groupby, agg, filtering |
| OpenRouter API | LLM access (baidu/qianfan-ocr-fast:free) |
| argparse | CLI region filter (`--region HK`) |
| logging | Console + file logging (`app.log`) |
| python-dotenv | Secure API key management |

## 📁 File Structure

```
supply-chain-ai-analyst/
├── analyse.py      # Main script
├── data.csv        # Supply chain data
├── report.md       # Generated report (auto-created)
├── app.log         # Log file (auto-created)
├── .env            # API key (not committed)
├── .env.example    # API key template
└── README.md
```

## ⚙️ Engineering Patterns

- **Exponential backoff retry** — auto-retries on API failure (1s → 2s → 4s)
- **Dual-handler logging** — simultaneous console and `app.log` output
- **argparse CLI** — filter by region without changing code
- **Modular analysis** — pandas groupby + agg for multi-metric summaries

## 📌 Part of

This project is part of my [26-week AI Engineer Journey](https://github.com/sam216515/ai-engineer-journey).
