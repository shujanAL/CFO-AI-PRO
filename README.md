# CFO AI PRO

An AI-powered financial decision platform that helps SMEs analyze Excel data, understand financial health, assess financing readiness, forecast performance, and simulate decisions before implementation.

Built by **Shujaan Almutairi** for the AMAD 2026 Hackathon.

## Why CFO AI PRO?

Financial analysis, bank-readiness assessment, forecasting, and decision simulation are often performed manually or across disconnected tools. CFO AI PRO brings the complete workflow into one bilingual platform.

## Main Features

- Excel and CSV data import with validation
- Arabic and English interface
- Executive financial dashboard
- Financial Health Score
- Bank Financing Readiness Score
- Sales, expense, and cash-flow forecasting
- Risk detection and evidence-based insights
- Decision simulator and option ranking
- Executive recommendations
- PDF financial reports

## Project Flow

`Upload Excel` → `Data Validation` → `Financial Analysis` → `Health & Financing Scores` → `Forecast` → `Decision Simulation` → `Executive Recommendation`

## Supported Data

- Sales
- Expenses
- Employees
- Invoices
- Customers
- Financial statements

Sample Excel files are available in [`templates/`](templates/).

## Technology Stack

- Python
- Streamlit
- Pandas and NumPy
- Plotly
- Scikit-learn
- SQLite
- OpenPyXL
- ReportLab

## Run Locally

```bash
git clone https://github.com/shujanAL/CFO-AI-PRO.git
cd CFO-AI-PRO
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies and start the application:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501`.

## Presentation

The final hackathon presentation and project screenshot are available in [`docs/`](docs/).

## Privacy

Uploaded company data is processed locally. Local database files, generated reports, environment files, and secrets are excluded from Git through `.gitignore`.

## Disclaimer

CFO AI PRO is a decision-support prototype. Its results do not replace professional accounting, banking, investment, or legal advice.

## Author

**Shujaan Almutairi — شجعان المطيري**
