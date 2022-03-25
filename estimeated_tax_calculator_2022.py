from typing import Any, Generator, List, Union


pension_worker_deduct_rate: float = 0.06
credit_point_value: int = 223
tax_level = List[Union[int, float]]
income_tax_2022: list[tax_level] = [[6_450, 0.1], [9_240, 0.14], [14_840, 0.2], [20_620, 0.31], [42_910, 0.35],
                                    [float('inf'), 0.47]]
national_insurance_worker_2022: list[tax_level] = [[6_331, 0.035], [45_075, 0.12], [float('inf'), 0]]


def level_gen(levels: list) -> Generator[tax_level, None, None]:
    for level in levels:
        yield level


income_tax_levels: Generator[tax_level, None, None] = level_gen(income_tax_2022)
national_insurance_levels: Generator[tax_level, None, None] = level_gen(national_insurance_worker_2022)
omitted: Union[int, float] = 0
tax: Union[int, float] = 0


def tax_to_deduct_from_salary(income: Union[int, float],
                              tax_levels: Generator[tax_level, None, None], credit_points: Union[int, float] = 0)\
        -> Union[int, float]:
    global omitted
    global tax
    current_level: tax_level = next(tax_levels)
    if income >= current_level[0]:
        if not omitted:
            tax += current_level[0] * current_level[1]
            omitted += current_level[0]
            return tax_to_deduct_from_salary(income, tax_levels, credit_points)
        elif omitted:
            tax += (current_level[0] - omitted) * current_level[1]
            omitted += (current_level[0] - omitted)
            return tax_to_deduct_from_salary(income, tax_levels, credit_points)
    else:
        tax += (income - omitted) * current_level[1] - (credit_points * credit_point_value)
        tax = round(tax)
        if tax >= 0:
            return tax
    return 0


user_income: Any = input("Please enter the total sum of income: ")
user_credit_points: Any = input("Please enter the number of credit points: ")

national_insurance_deduction: Union[int, float] =\
    tax_to_deduct_from_salary(int(user_income) if user_income else 0, national_insurance_levels)

income_tax_deduction: Union[int, float] =\
    tax_to_deduct_from_salary(int(user_income) if user_income else 0, income_tax_levels,
                              float(user_credit_points) if user_credit_points else 0)

pension_deduction: float = pension_worker_deduct_rate * float(user_income)

print(f"""
Gross Salary: {user_income}
National Insurance Deduction: {national_insurance_deduction}
Income Tax Deduction: {income_tax_deduction}
Pension Deduction : {pension_deduction}

Net Salary: {float(user_income) - float(national_insurance_deduction)
             - (income_tax_deduction if income_tax_deduction else 0) - pension_deduction}

""")
