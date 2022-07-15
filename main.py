from typing import Any, Generator, List, Union
from flask import Flask


app = Flask(__name__)

tax_level = List[Union[int, float]]


PENSION_WORKER_DEDUCT_RATE: float = 0.06
CREDIT_POINT_VALUE: int = 223
INCOME_TAX_2022: list[tax_level] = [[6_450, 0.1], [9_240, 0.14], [14_840, 0.2], [20_620, 0.31], [42_910, 0.35],
                                    [float('inf'), 0.47]]
NATIONAL_INSURANCE_WORKER_2022: list[tax_level] = [[6_331, 0.035], [45_075, 0.12], [float('inf'), 0]]


def level_gen(levels: list) -> Generator[tax_level, None, None]:
    for level in levels:
        yield level


def invalid_value(num):
    try:
        float(num)
        return False

    except ValueError:
        return True


@app.errorhandler(404)
def page_not_found(e):
    return {"Detail": "Unknown Route"}


@app.route("/calc/<user_income>/<user_credit_points>")
def calc_api(user_income, user_credit_points) -> dict:

    if invalid_value(user_income) or invalid_value(user_credit_points):
        return {"Detail": "Invalid Value"}

    omitted: Union[int, float] = 0
    tax: Union[int, float] = 0

    income_tax_levels: Generator[tax_level, None, None] = level_gen(INCOME_TAX_2022)
    national_insurance_levels: Generator[tax_level, None, None] = level_gen(NATIONAL_INSURANCE_WORKER_2022)

    national_insurance_deduction: Union[int, float] =\
        tax_to_deduct_from_salary(float(user_income) if user_income else 0, national_insurance_levels, omitted, tax)

    income_tax_deduction: Union[int, float] =\
        tax_to_deduct_from_salary(float(user_income) if user_income else 0, income_tax_levels,
                                omitted, tax, float(user_credit_points) if user_credit_points else 0)

    pension_deduction: float = PENSION_WORKER_DEDUCT_RATE * float(user_income)

    return {"Gross Salary": float(user_income), "National Insurance Deduction": national_insurance_deduction,
            "Income Tax Deduction": income_tax_deduction, "Pension Deduction": pension_deduction,
            "Net Salary": (float(user_income) - float(national_insurance_deduction)
                - (income_tax_deduction if income_tax_deduction else 0) - pension_deduction)}



def tax_to_deduct_from_salary(income: Union[int, float], tax_levels: Generator[tax_level, None, None],
                               omitted_value, tax_value, credit_points: Union[int, float] = 0)\
        -> Union[int, float]:

    current_level: tax_level = next(tax_levels)

    if income >= current_level[0]:

        if not omitted_value:
            tax_value += current_level[0] * current_level[1]
            omitted_value += current_level[0]
            return tax_to_deduct_from_salary(income, tax_levels, omitted_value, tax_value, credit_points)

        tax_value += (current_level[0] - omitted_value) * current_level[1]
        omitted_value += (current_level[0] - omitted_value)
        return tax_to_deduct_from_salary(income, tax_levels, omitted_value, tax_value, credit_points)


    tax_value += (income - omitted_value) * current_level[1] - (credit_points * CREDIT_POINT_VALUE)
    tax_value = round(tax_value)

    if tax_value >= 0:
        return tax_value

    return 0


if __name__ == '__main__':
    app.run()