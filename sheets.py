import pygsheets

# authorize using service account credentials
gc = pygsheets.authorize(service_file='credentials.json')
sheet = gc.open('Hairbot Booking')
worksheet = sheet.sheet1

# predefined daily time slots (can be customized)
SLOTS = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

def get_free_slots(date_str):
    """
    returns a list of available time slots for the given date.
    if the date is marked as a holiday, returns an empty list.
    """
    records = worksheet.get_all_records()

    taken_slots = [r["Time"] for r in records if r["Date"] == date_str and r["Status"].lower() == "confirmed"]
    is_holiday = any(r["Date"] == date_str and r["Status"].lower() == "holiday" for r in records)

    if is_holiday:
        return []

    return [slot for slot in SLOTS if slot not in taken_slots]

def book_slot(date_str, time_str, name, phone, service):
    """
    adds a new booking record to the google sheet.
    the status is set to "confirmed" and reminder to "no".
    """
    worksheet.append_table([
        date_str,
        time_str,
        name,
        phone,
        service,
        "confirmed",
        "no"
    ])

# Тестирование
if __name__ == "__main__":
    print("2025-07-20:")
    print(get_free_slots("2025-07-20"))