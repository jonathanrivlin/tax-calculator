tax_levels_2022 = [[6_450, 0.1], [9_240, 0.14], [14_840, 0.2], [20_620, 0.31], [42_910, 0.35], [float('inf'), 0.47]]
credit_point_value = 223


def level_gen(levels):
    for level in levels:
        yield level


tax_levels = level_gen(tax_levels_2022)
omitted = 0
tax = 0


def calc_tax(income, credit_points):
    global omitted
    global tax
    current_level = next(tax_levels)
    if income > current_level[0]:
        if not omitted:
            tax += current_level[0] * current_level[1]
            omitted += current_level[0]
            return calc_tax(income, credit_points)
        elif omitted:
            tax += (current_level[0] - omitted) * current_level[1]
            omitted += (current_level[0] - omitted)
            return calc_tax(income, credit_points)
    elif income == current_level[0]:
        tax += current_level[0] * current_level[1]
    else:
        tax += (income - omitted) * current_level[1] - (credit_points * credit_point_value)
        tax = round(tax)
        if tax >= 0:
            return tax
        else:
            return

user_income = input("Please enter the total sum of income: ")
user_credit_points = input("Please enter the number of credit points: ")
print(f"\nEstimated tax to be deducted from salary: \
{calc_tax(int(user_income) if user_income else 0 , float(user_credit_points) if user_credit_points else 0)} ILS!")
