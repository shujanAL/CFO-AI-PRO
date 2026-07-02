from utils.import_engine import validate_excel

status, message = validate_excel("templates/cfo_ai_template.xlsx")

print(status)
print(message)