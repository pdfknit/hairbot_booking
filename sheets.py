import pygsheets

# authorize using service account credentials
gc = pygsheets.authorize(service_file='credentials.json')
sheet = gc.open('Hairbot Booking')
worksheet = sheet.sheet1

# predefined daily time slots (can be customized)
SLOTS = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]


def get_free_slots(date_str):
    """
    returns a list of available time slots for the given date
    if the date is marked as a holiday, returns an empty list
    """
    records = worksheet.get_all_records()

    taken_slots = [r["Time"] for r in records if r["Date"] == date_str and r["Status"].lower() == "confirmed"]
    is_holiday = any(r["Date"] == date_str and r["Status"].lower() == "holiday" for r in records)

    if is_holiday:
        return []

    return [slot for slot in SLOTS if slot not in taken_slots]


def book_slot(date_str, time_str, name, phone, service):
    """
    adds a new booking record to the google sheet
    the status is set to "confirmed" and reminder to "no"
    """

    records = worksheet.get_all_records()

    # Check for holiday
    if any(r["Date"] == date_str and r["Status"].lower() == "holiday" for r in records):
        print(f"Cannot book: {date_str} is a holiday.")
        return False

    # Check if slot is taken
    if any(r["Date"] == date_str and r["Time"] == time_str and r["Status"].lower() == "confirmed" for r in records):
        print(f"Cannot book: {date_str} {time_str} is already taken.")
        return False

    worksheet.append_table([
        date_str,
        time_str,
        name,
        phone,
        service,
        "confirmed",
        "no"
    ])
    print(f"Booked {date_str} at {time_str} for {name}")
    return True


def set_holiday(date_str):
    """
    marks the given date as a holiday by adding a special row to the sheet
    """
    records = worksheet.get_all_records()

    already_set = any(
        r["Date"] == date_str and r["Status"].lower() == "holiday"
        for r in records
    )

    if already_set:
        print(f"Holiday already set for {date_str}")
        return False

    worksheet.append_table([
        date_str,
        "",  # Time (not needed)
        "",  # Client Name
        "",  # Phone Number
        "",  # Service
        "holiday",  # Status
        ""  # Notified
    ])
    print(f"Holiday set for {date_str}")
    return True


def unset_holiday(date_str):
    """
    removes the 'holiday' status from the given date, if it exists.
    """
    records = worksheet.get_all_records()
    rows = worksheet.get_all_values(include_tailing_empty_rows=False)

    for idx, row in enumerate(rows[1:], start=2):  # skip header row (1-based index)
        if row[0] == date_str and row[5].lower() == "holiday":
            worksheet.delete_rows(idx)
            print(f"Holiday removed for {date_str}")
            return True

    print(f"No holiday found for {date_str}")
    return False


def cancel_appointment(date_str, time_str):
    """
    marks the appointment for the given date and time as canceled.
    does not delete the row, only changes its status
    """
    rows = worksheet.get_all_values(include_tailing_empty_rows=False)

    for idx, row in enumerate(rows[1:], start=2):  # skip header
        if row[0] == date_str and row[1] == time_str and row[5].lower() == "confirmed":
            worksheet.update_value(f"F{idx}", "canceled")  # column F = Status
            print(f"Appointment on {date_str} at {time_str} canceled.")
            return True

    print(f"No confirmed appointment found on {date_str} at {time_str}.")
    return False


# test
if __name__ == "__main__":
    print("2025-07-20:")
    print(get_free_slots("2025-07-20"))
    # holidays
    set_holiday("2025-07-25")
    print("2025-07-25:")
    print(get_free_slots("2025-07-25"))
    # unset holiday
    unset_holiday("2025-07-25")
    print("2025-07-25:")
    print(get_free_slots("2025-07-25"))
    book_slot("2025-07-22", "10:00", "Alice", "+19998887766", "Haircut")
