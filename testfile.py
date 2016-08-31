import xlsxwriter

workbook = xlsxwriter.Workbook('arrays.xlsx')
worksheet = workbook.add_worksheet()

array = [['a1', 'a2', 'a3'],
         ['a4', 'a5', 'a6'],
         ['a7', 'a8', 'a9'],
         ['a10', 'a11', 'a12', 'a13', 'a14']]

row = 0

for col, data in enumerate(array):
    worksheet.write_column(row, col, data)

workbook.close()