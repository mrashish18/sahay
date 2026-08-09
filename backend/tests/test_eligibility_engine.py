import pytest
from app.services.eligibility_engine import EligibilityEngine, eligibility_engine
from app.models.eligibility import (
    RuleCondition, RuleGroup, RuleOperator, LogicalOperator, PeriodType,
    CriterionStatus
)
from app.models.schemas import EligibilityStatus

def test_scenario_1_all_criteria_satisfied():
    rules = {
        "logical_operator": "AND",
        "conditions": [
            {"field": "employment_status", "operator": "==", "value": "unemployed", "description": "Must be unemployed"},
            {"field": "household_income", "operator": "<=", "value": 250000, "description": "Household income <= ₹250,000"}
        ]
    }
    user_facts = {
        "employment_status": "unemployed",
        "household_income": 180000
    }
    res = eligibility_engine.evaluate_scheme("SCH-TEST-01", rules, user_facts)
    assert res.status == EligibilityStatus.LIKELY_ELIGIBLE
    assert len(res.matching_criteria) == 2
    assert len(res.unmet_criteria) == 0

def test_scenario_2_mandatory_criterion_failed():
    rules = {
        "logical_operator": "AND",
        "conditions": [
            {"field": "employment_status", "operator": "==", "value": "unemployed", "description": "Must be unemployed"},
            {"field": "household_income", "operator": "<=", "value": 250000, "description": "Household income <= ₹250,000"}
        ]
    }
    user_facts = {
        "employment_status": "employed",  # Fails requirement
        "household_income": 180000
    }
    res = eligibility_engine.evaluate_scheme("SCH-TEST-02", rules, user_facts)
    assert res.status == EligibilityStatus.INELIGIBLE
    assert len(res.unmet_criteria) >= 1

def test_scenario_3_required_info_missing():
    rules = {
        "logical_operator": "AND",
        "conditions": [
            {"field": "household_income", "operator": "<=", "value": 250000, "description": "Household income <= ₹250,000"}
        ]
    }
    user_facts = {}  # Empty facts
    res = eligibility_engine.evaluate_scheme("SCH-TEST-03", rules, user_facts)
    assert res.status == EligibilityStatus.UNCERTAIN

def test_scenario_4_partially_satisfied_some_missing():
    rules = {
        "logical_operator": "AND",
        "conditions": [
            {"field": "employment_status", "operator": "==", "value": "unemployed", "description": "Must be unemployed"},
            {"field": "household_income", "operator": "<=", "value": 250000, "description": "Household income <= ₹250,000"}
        ]
    }
    user_facts = {
        "employment_status": "unemployed"
        # household_income missing
    }
    res = eligibility_engine.evaluate_scheme("SCH-TEST-04", rules, user_facts)
    assert res.status == EligibilityStatus.POTENTIALLY_ELIGIBLE
    assert len(res.matching_criteria) == 1

def test_scenario_5_or_group_one_branch_satisfied():
    rules = {
        "logical_operator": "OR",
        "conditions": [
            {"field": "age", "operator": ">=", "value": 60, "description": "Senior citizen age >= 60"},
            {"field": "disability_status", "operator": "==", "value": True, "description": "Disability status true"}
        ]
    }
    user_facts = {
        "age": 65,  # Satisfies branch 1
        "disability_status": False
    }
    res = eligibility_engine.evaluate_scheme("SCH-TEST-05", rules, user_facts)
    assert res.status == EligibilityStatus.LIKELY_ELIGIBLE

def test_scenario_6_or_group_all_branches_failed():
    rules = {
        "logical_operator": "OR",
        "conditions": [
            {"field": "age", "operator": ">=", "value": 60, "description": "Senior citizen age >= 60"},
            {"field": "disability_status", "operator": "==", "value": True, "description": "Disability status true"}
        ]
    }
    user_facts = {
        "age": 30,
        "disability_status": False
    }
    res = eligibility_engine.evaluate_scheme("SCH-TEST-06", rules, user_facts)
    assert res.status == EligibilityStatus.INELIGIBLE

def test_scenario_7_nested_and_or_conditions():
    rules = {
        "logical_operator": "AND",
        "conditions": [
            {"field": "household_income", "operator": "<=", "value": 300000, "description": "Income <= 300000"}
        ],
        "subgroups": [
            {
                "logical_operator": "OR",
                "conditions": [
                    {"field": "age", "operator": ">=", "value": 60, "description": "Senior citizen"},
                    {"field": "disability_status", "operator": "==", "value": True, "description": "Disabled"}
                ]
            }
        ]
    }
    # Case A: Income ok + senior ok -> LIKELY_ELIGIBLE
    facts_a = {"household_income": 200000, "age": 62, "disability_status": False}
    res_a = eligibility_engine.evaluate_scheme("SCH-TEST-07", rules, facts_a)
    assert res_a.status == EligibilityStatus.LIKELY_ELIGIBLE

    # Case B: Income ok + neither senior nor disabled -> INELIGIBLE
    facts_b = {"household_income": 200000, "age": 30, "disability_status": False}
    res_b = eligibility_engine.evaluate_scheme("SCH-TEST-07", rules, facts_b)
    assert res_b.status == EligibilityStatus.INELIGIBLE

def test_scenario_8_currency_and_period_normalization():
    engine = EligibilityEngine()
    
    # Target rule: annual income <= 300,000 INR
    cond = RuleCondition(
        field="monthly_income",
        operator=RuleOperator.LTE,
        value=300000.0,
        description="Annual household income <= ₹300,000",
        period=PeriodType.ANNUAL
    )
    
    # User provides monthly income of 20,000 INR (annualized = 240,000 INR <= 300,000 INR -> SATISFIED)
    user_facts = {
        "monthly_income": 20000.0,
        "monthly_income_period": "monthly"
    }
    trace = engine.evaluate_condition(cond, user_facts)
    assert trace.status == CriterionStatus.SATISFIED

    # User provides monthly income of 30,000 INR (annualized = 360,000 INR > 300,000 INR -> NOT_SATISFIED)
    user_facts_high = {
        "monthly_income": 30000.0,
        "monthly_income_period": "monthly"
    }
    trace_high = engine.evaluate_condition(cond, user_facts_high)
    assert trace_high.status == CriterionStatus.NOT_SATISFIED

def test_scenario_9_jurisdiction_mismatch():
    rules = {
        "logical_operator": "AND",
        "conditions": [
            {"field": "state", "operator": "==", "value": "Bihar", "description": "State must be Bihar"}
        ]
    }
    user_facts = {"state": "Delhi"}
    res = eligibility_engine.evaluate_scheme("SCH-TEST-09", rules, user_facts)
    assert res.status == EligibilityStatus.INELIGIBLE

def test_scenario_10_inferred_fact_distinction():
    rules = {
        "logical_operator": "AND",
        "conditions": [
            {"field": "displacement", "operator": "==", "value": True, "description": "Displaced by disaster"}
        ]
    }
    # Inferred fact should return UNCERTAIN, preventing unconfirmed eligibility claims
    user_facts = {
        "displacement": True,
        "_inferred": {"displacement": True}
    }
    res = eligibility_engine.evaluate_scheme("SCH-TEST-10", rules, user_facts)
    assert res.status == EligibilityStatus.UNCERTAIN
