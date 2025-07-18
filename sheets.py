import pygsheets

gc = pygsheets.authorize(service_file='credentials.json')
sheet = gc.open('Hairbot Booking')
worksheet = sheet.sheet1

print(worksheet.get_all_records())