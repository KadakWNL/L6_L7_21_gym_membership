"""Code (line) coverage test suite for gym_membership.py.

Goal: execute every statement in gym_membership.py at least once so that the
line coverage report shows 100%.

Run:
    coverage run -m pytest CodeCoverageTest_21_gym_membership.py
    coverage report -m
"""

import pytest

from gym_membership import bmi_category, can_enter, membership_cost


# ---------------------------------------------------------------- membership_cost
def test_unknown_plan_raises():
    with pytest.raises(ValueError):
        membership_cost("weekly", 25, False, False)


def test_too_young_raises():
    with pytest.raises(ValueError):
        membership_cost("monthly", 13, False, False)


def test_plain_monthly_member():
    assert membership_cost("monthly", 30, False, False) == 1500


def test_senior_discount():
    # 25% off for age >= 60
    assert membership_cost("monthly", 65, False, False) == 1125


def test_student_discount():
    # 10% off for students below senior age
    assert membership_cost("monthly", 20, True, False) == 1350


def test_trainer_addon():
    assert membership_cost("monthly", 30, False, True) == 3500


def test_yearly_plan_with_trainer():
    # trainer add-on and the extra 500 off for the yearly plan
    assert membership_cost("yearly", 30, False, True) == 13500


# ---------------------------------------------------------------- can_enter
def test_inactive_plan_cannot_enter():
    assert can_enter(10, False, False, "M") is False


def test_cannot_enter_outside_hours():
    assert can_enter(4, True, False, "M") is False


def test_women_only_slot_allows_female():
    assert can_enter(10, True, True, "F") is True


def test_regular_slot_allows_anyone():
    assert can_enter(10, True, False, "M") is True


# ---------------------------------------------------------------- bmi_category
def test_invalid_height_raises():
    with pytest.raises(ValueError):
        bmi_category(70, 0)


def test_bmi_underweight():
    assert bmi_category(17, 1.0) == "underweight"


def test_bmi_normal():
    assert bmi_category(22, 1.0) == "normal"


def test_bmi_overweight():
    assert bmi_category(27, 1.0) == "overweight"


def test_bmi_obese():
    assert bmi_category(35, 1.0) == "obese"
