from utils.import_engine import validate_excel
from utils.database_builder import build_database_from_excel

excel_path = "templates/cfo_ai_template.xlsx"

status, message = validate_excel(excel_path)
print(status)
print(message)

if status:
    db_path = build_database_from_excel(excel_path)
    print(f"Database created successfully: {db_path}")