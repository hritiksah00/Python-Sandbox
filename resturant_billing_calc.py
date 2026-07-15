# tax rate representing 13% tax
global_tax_rate = 0.13

def calculate_total_bill(subtotal):
    total_price = subtotal * global_tax_rate
    return total_price

total_price = calculate_total_bill(340)  # Example usage

print(total_price)  # Output: 44.2