"""Tests for calendar integration (availability and booking)."""
from calendar_api import list_events, get_free_slots, book_slot, set_holiday, unset_holiday


# choose any date, format: YYYY-MM-DD
TEST_DATE = "2025-07-25"

# test connections
# events = list_events(test_date)
# print(f"Events on {test_date}:")
# for e in events:
#     print("-", e.get("summary"), "|", e.get("start"), "→", e.get("end"))

# # test free slots
# slots = get_free_slots("2025-07-30")
# print("Free slots on 2025-07-30:")
# for s in slots:
#     print("-", s)
#
# #test booking
# book_slot("2025-07-30", "11:00", "Alice", "Haircut")
#
# slots = get_free_slots("2025-07-30")
# print("Free slots on 2025-07-30:")
# for s in slots:
#     print("-", s)
# set_holiday("2025-08-01")
# set_holiday("2025-08-02")
# unset_holiday("2025-08-02")

# test free slots
slots = get_free_slots("2025-08-01")
print("Free slots on 2025-08-01:")
for s in slots:
    print("-", s)