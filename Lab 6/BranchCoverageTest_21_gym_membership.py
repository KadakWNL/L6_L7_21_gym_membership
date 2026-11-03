"""Branch coverage test suite for gym_membership.py.

Goal: drive every decision (if / elif) in gym_membership.py to both its True
and False outcome, including boundary values, so that the branch coverage
report shows 100%.

Run:
    coverage run --branch -m pytest BranchCoverageTest_21_gym_membership.py
    coverage report -m
"""

import pytest

from gym_membership import bmi_category, can_enter, membership_cost


# ---------------------------------------------------------------- membership_cost
def test_unknown_plan_raises():
    with pytest.raises(ValueError):
        membership_cost("weekly", 25, False, False)


@pytest.mark.parametrize("age", [0, 13])
def test_age_below_fourteen_raises(age):
    with pytest.raises(ValueError):
        membership_cost("monthly", age, False, False)


def test_age_boundary_fourteen_is_allowed():
    assert membership_cost("monthly", 14, False, False) == 1500


# branch: age >= 60  True
def test_senior_monthly():
    assert membership_cost("monthly", 60, False, False) == 1125


# branch: age >= 60  False -> elif is_student False
def test_adult_non_student_monthly():
    assert membership_cost("monthly", 59, False, False) == 1500


# branch: age >= 60  False -> elif is_student True
def test_adult_student_monthly():
    assert membership_cost("monthly", 59, True, False) == 1350


# branch: age >= 60 True wins over student discount
def test_senior_student_gets_senior_discount_only():
    assert membership_cost("monthly", 60, True, False) == 1125


# branch: with_trainer False
def test_no_trainer():
    assert membership_cost("quarterly", 30, False, False) == 4000


# branch: with_trainer True -> plan == "yearly" False
def test_trainer_on_non_yearly_plan():
    assert membership_cost("quarterly", 30, False, True) == 6000


# branch: with_trainer True -> plan == "yearly" True
def test_trainer_on_yearly_plan():
    assert membership_cost("yearly", 30, False, True) == 13500


def test_every_plan_price_is_used():
    assert membership_cost("monthly", 30, False, False) == 1500
    assert membership_cost("quarterly", 30, False, False) == 4000
    assert membership_cost("yearly", 30, False, False) == 12000


# ---------------------------------------------------------------- can_enter
# branch: not plan_active True
def test_inactive_plan_cannot_enter():
    assert can_enter(10, False, False, "M") is False


# branch: not plan_active False, short-circuit: hour < 5 True
def test_before_opening_time_cannot_enter():
    assert can_enter(4, True, False, "M") is False


# branch: hour < 5 False -> hour > 22 True
def test_after_closing_time_cannot_enter():
    assert can_enter(23, True, False, "M") is False


@pytest.mark.parametrize("hour", [5, 22])
def test_opening_and_closing_boundaries_are_allowed(hour):
    assert can_enter(hour, True, False, "M") is True


# branch: is_women_only_slot True -> gender == "F" True
def test_women_only_slot_allows_female():
    assert can_enter(10, True, True, "F") is True


# branch: is_women_only_slot True -> gender == "F" False
def test_women_only_slot_blocks_male():
    assert can_enter(10, True, True, "M") is False


# branch: is_women_only_slot False
@pytest.mark.parametrize("gender", ["M", "F"])
def test_regular_slot_allows_everyone(gender):
    assert can_enter(10, True, False, gender) is True


# ---------------------------------------------------------------- bmi_category
@pytest.mark.parametrize("height", [0, -1.5])
def test_invalid_height_raises(height):
    with pytest.raises(ValueError):
        bmi_category(70, height)


@pytest.mark.parametrize(
    "weight, expected",
    [
        (18.49, "underweight"),  # bmi < 18.5            True
        (18.5, "normal"),        # bmi < 18.5            False, bmi < 25 True
        (24.99, "normal"),       # still normal
        (25.0, "overweight"),    # bmi < 25              False, bmi < 30 True
        (29.99, "overweight"),
        (30.0, "obese"),         # bmi < 30              False
        (45.0, "obese"),
    ],
)
def test_bmi_boundaries(weight, expected):
    assert bmi_category(weight, 1.0) == expected
