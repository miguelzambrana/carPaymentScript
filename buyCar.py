

def loan_calculator(tin, loan_amount, months):
    monthly_interest_rate = tin / 100 / 12
    monthly_payment = loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -months)
    print(f'Monthly payment: {monthly_payment:.2f}')

    remaining_balance = loan_amount
    for i in range(1, months + 1):
        interest_paid = remaining_balance * monthly_interest_rate
        principal_paid = monthly_payment - interest_paid
        remaining_balance -= principal_paid
        print(f'Month {i}: Interest paid: {interest_paid:.2f}, Debt paid: {principal_paid:.2f} Remaining balance: {remaining_balance:.2f}')


def remaining_balance_calculator(tin, loan_amount, total_months, paid_months):
    monthly_interest_rate = tin / 100 / 12
    monthly_payment = loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -total_months)

    remaining_balance = loan_amount
    total_principal_paid = 0

    for i in range(1, paid_months + 1):
        interest_paid = remaining_balance * monthly_interest_rate
        principal_paid = monthly_payment - interest_paid
        remaining_balance -= principal_paid
        total_principal_paid += principal_paid

    return remaining_balance

def get_load_monthly_payment(tin, loan_amount, months):
    monthly_interest_rate = tin / 100 / 12
    return loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -months)


def get_tin(monthly_payment, loan_amount, months):
    # Define the function for the monthly payment
    def f(tin):
        monthly_interest_rate = tin / 100 / 12
        return loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -months) - monthly_payment

    # Define the initial interval for the bisection method
    lower = 0
    upper = 100

    # Perform the bisection method
    while upper - lower > 1e-6:
        mid = (upper + lower) / 2
        if f(mid) > 0:
            upper = mid
        else:
            lower = mid

    return (upper + lower) / 2


question_car_model = 'What is the model of the car?? Response here: '
question_dealership = 'What is the dealership? Response here: '
question_price_car = 'How much is the price for the car (in €)? Response here: '
question_paid_by_own_car = 'How much do they pay for the delivered car (in €)? Response here: '
question_discount_loan = 'How much do you get a discount for financing or having a loan (in €)? Response here: '
question_borrowed_euro = ('How much money does the dealer lend you for the purchase of the car (total borrowed in €)? '
                          'Response here: ')
question_loan_months = 'How many years is the loan? Response here: '
question_tin_value = 'Write the TIN% of the loan if you know it, otherwise write 0? Response here: '
question_monthly_loan = 'Write the monthly payment you have to pay for the loan (in €)? Response here: '
question_cancel_loan = 'Can you pay off the loan after a few months? Write after the months you can cancel: '
question_percentage_cancel_load = 'What is the percentage to pay once the loan is paid off (in %)? Response here: '

car_model = str(input(question_car_model))
dealership = str(input(question_dealership))

# Ask the question and get the user input as a float
price_car = float(input(question_price_car))

try:
    paid_delivered_car = float(input(question_paid_by_own_car))
except Exception:
    paid_delivered_car = 0

price_car_less_delivered = (price_car - paid_delivered_car)
discount_loan = float(input(question_discount_loan))
loan_amount = float(input(question_borrowed_euro))
loan_months = int(input(question_loan_months)) * 12
loan_tin_value = 0
monthly_payment = 0
loan_amount_to_pay = 0
loan_cancel_percent_value = 0
remain_to_pay = 0

try:
    loan_tin_value = float(input(question_tin_value))
except Exception:
    loan_tin_value = 0

if loan_tin_value == 0:
    monthly_payment = float(input(question_monthly_loan))
    loan_tin_value = get_tin(monthly_payment, loan_amount, loan_months)
else:
    monthly_payment = get_load_monthly_payment(loan_tin_value, loan_amount, loan_months)

try:
    cancel_loan_months = int(input(question_cancel_loan))
except Exception:
    cancel_loan_months = 0

if cancel_loan_months > 0:
    try:
        loan_cancel_percent_value = float(input(question_percentage_cancel_load))
    except Exception:
        loan_cancel_percent_value = 0

loan_amount_to_pay = monthly_payment * loan_months

total_price_without_loan = (price_car_less_delivered + discount_loan)
total_price_with_loan = (price_car_less_delivered - loan_amount + loan_amount_to_pay)
total_price_canceling_loan = 0

if cancel_loan_months > 0:
    remain_to_pay = remaining_balance_calculator(loan_tin_value, loan_amount, loan_months, cancel_loan_months)
    total_price_canceling_loan = (price_car_less_delivered - loan_amount +
                                  (cancel_loan_months * monthly_payment) +
                                  (remain_to_pay + (remain_to_pay * (loan_cancel_percent_value / 100))))

print(f"\n\n###################################################################################")
print(f" # Car Model / Dealership:               {car_model} / {dealership}")
print(f" > Total Price Car:                      {price_car}€")
print(f" > Paid by delivered Car:                {paid_delivered_car}€")
print(f" > Total Loan Discount:                  {discount_loan}€")
print(f" > Load Information:")
print(f"   - Total amount:                       {loan_amount}€")
print(f"   - TIN % value:                        {loan_tin_value:.2f}%")
print(f"   - Monthly payment:                    {monthly_payment:.2f}€")
print(f"   - Total months to pay:                {loan_months}")
print(f"   - Total amount to pay:                {loan_amount_to_pay:.2f}€ (Interests "
      f"{(loan_amount_to_pay - loan_amount):.2f}€)")
print(f"\n\n#### Results ######################################################################")
print(f" > Total Price Car without Loan:         {total_price_without_loan}€")
print(f" > Total Price Car with Loan:            {total_price_with_loan:.2f}€")
print(f" > Total Price Car canceling Loan:       {total_price_canceling_loan:.2f}€")

if total_price_canceling_loan > 0:
    print(f"   - Load pained previous cancel:        {(cancel_loan_months * monthly_payment):.2f}€ "
          f"(First {cancel_loan_months} months)")
    print(f"   - Total to be paid upon cancellation: "
          f"{(remain_to_pay + (remain_to_pay * (loan_cancel_percent_value / 100))):.2f}€")

print(f"###################################################################################")

print(f"\n\n#### CSV FORMAT ###################################################################")
print(f"Car Model;{car_model}")
print(f"Dealership;{dealership}")
print(f"Total Price Car;{price_car}€")
print(f"Paid by delivered Car;{paid_delivered_car}€")
print(f"Total Loan Discount;{discount_loan}€")
print(f"Loan: Total amount;{loan_amount}€")
print(f"Loan: TIN % value;{loan_tin_value:.2f}%")
print(f"Loan: Monthly payment;{monthly_payment:.2f}€")
print(f"Loan: Total months to pay;{loan_months}")
print(f"Loan: Total amount to pay;{loan_amount_to_pay:.2f}€")
print(f"Loan: Interests paid;{(loan_amount_to_pay - loan_amount):.2f}€")
print(f"Total Price Car without Loan;{total_price_without_loan}€")
print(f"Total Price Car with Loan;{total_price_with_loan:.2f}€")
print(f"Total Price Car canceling Loan;{total_price_canceling_loan:.2f}€")

if total_price_canceling_loan > 0:
    print(f"Load pained previous cancel;{(cancel_loan_months * monthly_payment):.2f}€")
    print(f"Total to be paid upon cancellation;"
          f"{(remain_to_pay + (remain_to_pay * (loan_cancel_percent_value / 100))):.2f}€")
