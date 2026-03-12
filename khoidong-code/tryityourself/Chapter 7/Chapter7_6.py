# Version using an active variable (Flag)

prompt = "\nWhat topping would you like on your pizza?"
prompt += "\nEnter 'quit' when you are finished: "

active = True
while active:
    topping = input(prompt)
    
    if topping == 'quit':
        active = False
    else:
        print(f"I'll add {topping} to your pizza.")