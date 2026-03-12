from random import choice

lottery_pool = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'a', 'b', 'c', 'd', 'e']
winning_ticket = []

print("Selecting winning numbers...")
# We use a loop to ensure we get exactly 4 unique items
while len(winning_ticket) < 4:
    pulled_item = choice(lottery_pool)
    if pulled_item not in winning_ticket:
        winning_ticket.append(pulled_item)

print(f"Any ticket matching these 4 items wins a prize: {winning_ticket}")