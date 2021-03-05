from openpyxl import Workbook

def exportar_resultados_a_xlsx(keywords):
    workbook= Workbook()
    sheet = workbook.active
    sheet.append(("keywords","Posicion"))

    for kw in keywords:
        sheet.append(kw)
    workbook.save(filename="keywords.xlsx")

    