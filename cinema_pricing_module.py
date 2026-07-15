# 1. We put the parameters in the parentheses so they can be changed dynamically
def calculate_ticket_cost(ticket_price, quantity):
    
    # 2. We do the math to get the total
    total = ticket_price * quantity
    
    # 3. We print the final calculated cost
    print(f"Total cost for {quantity} tickets is ${total}")

# 4. The call is completely un-indented! 
# We pass the numbers (10.0 and 5) directly into the function here.
calculate_ticket_cost(10.0, 5)

# The beauty of parameters is that you can now call it again with totally different numbers!
calculate_ticket_cost(15.50, 2)