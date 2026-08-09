from typing import Dict, Any, List, Tuple, Optional
from app.models.schemas import EligibilityItem, EligibilityStatus
from app.models.eligibility import (
    RuleCondition, RuleGroup, RuleOperator, LogicalOperator, PeriodType,
    CriterionStatus, CriterionTrace, DetailedEligibilityTrace
)

class EligibilityEngine:
    """
    Deterministic Rule Engine for Sahay.
    Evaluates structured criteria against user facts using recursive logic,
    monetary/period normalization, explicit fact verification, and transparent trace generation.
    Zero LLM interference in eligibility decisions.
    """

    def normalize_monetary_value(
        self, user_val: float, user_period: PeriodType, target_period: PeriodType
    ) -> float:
        """
        Normalizes currency values between monthly and annual periods to prevent unit mismatch.
        """
        if user_period == target_period or target_period == PeriodType.UNKNOWN or user_period == PeriodType.UNKNOWN:
            return user_val

        if user_period == PeriodType.MONTHLY and target_period == PeriodType.ANNUAL:
            return user_val * 12.0

        if user_period == PeriodType.ANNUAL and target_period == PeriodType.MONTHLY:
            return user_val / 12.0

        return user_val

    def evaluate_condition(
        self, condition: RuleCondition, user_facts: Dict[str, Any]
    ) -> CriterionTrace:
        field_name = condition.field
        user_val = user_facts.get(field_name)

        # Check if fact is missing
        if user_val is None:
            return CriterionTrace(
                criterion=condition.description,
                field=field_name,
                status=CriterionStatus.MISSING,
                user_value=None,
                required_value=condition.value,
                reason=f"Required fact '{field_name}' is missing."
            )

        # Check if fact is marked as inferred signal rather than explicit fact
        is_inferred = False
        if isinstance(user_facts.get("_inferred"), dict) and user_facts["_inferred"].get(field_name):
            is_inferred = True

        # Perform period/currency normalization for numeric facts
        eval_user_val = user_val
        if isinstance(user_val, (int, float)) and isinstance(condition.value, (int, float)):
            user_period = user_facts.get(f"{field_name}_period", PeriodType.UNKNOWN)
            if isinstance(user_period, str):
                try:
                    user_period = PeriodType(user_period)
                except ValueError:
                    user_period = PeriodType.UNKNOWN
            eval_user_val = self.normalize_monetary_value(float(user_val), user_period, condition.period)

        # Operator evaluation
        op = condition.operator
        satisfied = False

        if op == RuleOperator.EQ:
            satisfied = (eval_user_val == condition.value)
        elif op == RuleOperator.NE:
            satisfied = (eval_user_val != condition.value)
        elif op == RuleOperator.GT:
            satisfied = (eval_user_val > condition.value)
        elif op == RuleOperator.GTE:
            satisfied = (eval_user_val >= condition.value)
        elif op == RuleOperator.LT:
            satisfied = (eval_user_val < condition.value)
        elif op == RuleOperator.LTE:
            satisfied = (eval_user_val <= condition.value)
        elif op == RuleOperator.IN:
            if isinstance(condition.value, list):
                satisfied = eval_user_val in condition.value
            else:
                satisfied = str(eval_user_val) in str(condition.value)
        elif op == RuleOperator.NOT_IN:
            if isinstance(condition.value, list):
                satisfied = eval_user_val not in condition.value
            else:
                satisfied = str(eval_user_val) not in str(condition.value)

        if is_inferred and satisfied:
            # Inferred facts require user verification
            return CriterionTrace(
                criterion=condition.description,
                field=field_name,
                status=CriterionStatus.UNCERTAIN,
                user_value=user_val,
                required_value=condition.value,
                reason=f"Inferred fact '{field_name}' matches requirement but requires explicit confirmation."
            )

        if satisfied:
            return CriterionTrace(
                criterion=condition.description,
                field=field_name,
                status=CriterionStatus.SATISFIED,
                user_value=user_val,
                required_value=condition.value,
                reason=f"Requirement satisfied: {eval_user_val} {op.value} {condition.value}."
            )
        else:
            return CriterionTrace(
                criterion=condition.description,
                field=field_name,
                status=CriterionStatus.NOT_SATISFIED,
                user_value=user_val,
                required_value=condition.value,
                reason=f"Requirement not met: {eval_user_val} failed condition {op.value} {condition.value}."
            )

    def evaluate_group(
        self, group: RuleGroup, user_facts: Dict[str, Any]
    ) -> tuple[CriterionStatus, List[CriterionTrace]]:
        traces: List[CriterionTrace] = []
        
        # Evaluate simple conditions
        cond_statuses: List[CriterionStatus] = []
        for cond in group.conditions:
            tr = self.evaluate_condition(cond, user_facts)
            traces.append(tr)
            cond_statuses.append(tr.status)

        # Evaluate nested subgroups recursively
        for sub in group.subgroups:
            sub_status, sub_traces = self.evaluate_group(sub, user_facts)
            traces.extend(sub_traces)
            cond_statuses.append(sub_status)

        if not cond_statuses:
            return CriterionStatus.SATISFIED, traces

        op = group.logical_operator
        if op == LogicalOperator.AND:
            if any(s == CriterionStatus.NOT_SATISFIED for s in cond_statuses):
                return CriterionStatus.NOT_SATISFIED, traces
            elif any(s in (CriterionStatus.MISSING, CriterionStatus.UNCERTAIN) for s in cond_statuses):
                return CriterionStatus.MISSING, traces
            else:
                return CriterionStatus.SATISFIED, traces

        elif op == LogicalOperator.OR:
            if any(s == CriterionStatus.SATISFIED for s in cond_statuses):
                # When an OR group is SATISFIED by one branch, mark alternative failed/missing branches as NOT_APPLICABLE
                adjusted_traces: List[CriterionTrace] = []
                for tr in traces:
                    if tr.status != CriterionStatus.SATISFIED:
                        adjusted_traces.append(CriterionTrace(
                            criterion=tr.criterion,
                            field=tr.field,
                            status=CriterionStatus.NOT_APPLICABLE,
                            user_value=tr.user_value,
                            required_value=tr.required_value,
                            reason="Alternative OR branch satisfied."
                        ))
                    else:
                        adjusted_traces.append(tr)
                return CriterionStatus.SATISFIED, adjusted_traces
            elif all(s == CriterionStatus.NOT_SATISFIED for s in cond_statuses):
                return CriterionStatus.NOT_SATISFIED, traces
            else:
                return CriterionStatus.MISSING, traces

        elif op == LogicalOperator.NOT:
            first = cond_statuses[0]
            if first == CriterionStatus.SATISFIED:
                return CriterionStatus.NOT_SATISFIED, traces
            elif first == CriterionStatus.NOT_SATISFIED:
                return CriterionStatus.SATISFIED, traces
            else:
                return first, traces

        return CriterionStatus.UNCERTAIN, traces

    def evaluate_scheme(
        self, scheme_id: str, rules: Dict[str, Any], user_facts: Dict[str, Any]
    ) -> EligibilityItem:
        """
        Evaluates a scheme's rules against user facts, returning transparent EligibilityItem with trace metadata.
        Enforces strict jurisdiction boundaries before evaluating secondary eligibility criteria.
        """
        user_country = user_facts.get("country", "IN")
        user_state = user_facts.get("state")
        rule_country = rules.get("country") or user_facts.get("rule_country", "IN")

        # 1. Country Jurisdiction Check
        if rules.get("country") and user_country and rules["country"] != user_country:
            return EligibilityItem(
                scheme_id=scheme_id,
                status=EligibilityStatus.INELIGIBLE,
                matching_criteria=[],
                unmet_criteria=[f"Country Jurisdiction Mismatch: Scheme applies to {rules['country']}, user is in {user_country}."],
                reasoning=f"Ineligible due to jurisdiction boundary: Scheme is restricted to {rules['country']}."
            )

        # 2. State Jurisdiction Check
        if rules.get("state") and user_state and rules["state"].lower() != user_state.lower():
            return EligibilityItem(
                scheme_id=scheme_id,
                status=EligibilityStatus.INELIGIBLE,
                matching_criteria=[],
                unmet_criteria=[f"State Jurisdiction Mismatch: Scheme applies to {rules['state']}, user is in {user_state}."],
                reasoning=f"Ineligible due to jurisdiction boundary: Scheme is restricted to {rules['state']}."
            )

        if not rules:
            return EligibilityItem(
                scheme_id=scheme_id,
                status=EligibilityStatus.UNCERTAIN,
                matching_criteria=[],
                unmet_criteria=[],
                reasoning="No structured eligibility rules defined for this scheme. Official verification required."
            )

        # Parse rule schema (dictionary or RuleGroup structure)
        rule_group = self._parse_rules_to_group(rules)
        _, traces = self.evaluate_group(rule_group, user_facts)

        matching_criteria: List[str] = []
        unmet_criteria: List[str] = []
        failed_count = 0
        missing_count = 0
        satisfied_count = 0

        for tr in traces:
            desc = f"{tr.criterion} (User: {tr.user_value})"
            if tr.status == CriterionStatus.SATISFIED:
                satisfied_count += 1
                matching_criteria.append(tr.criterion)
            elif tr.status == CriterionStatus.NOT_SATISFIED:
                failed_count += 1
                unmet_criteria.append(f"{tr.criterion} - {tr.reason}")
            elif tr.status in (CriterionStatus.MISSING, CriterionStatus.UNCERTAIN):
                missing_count += 1
                unmet_criteria.append(f"{tr.criterion} - {tr.reason}")

        # Deterministic State Resolution Algorithm
        if failed_count > 0:
            status = EligibilityStatus.INELIGIBLE
            reasoning = f"Ineligible: {failed_count} mandatory criteria were not satisfied."
        elif missing_count > 0 and satisfied_count > 0:
            status = EligibilityStatus.POTENTIALLY_ELIGIBLE
            reasoning = f"Potentially Eligible: Satisfies {satisfied_count} criteria, but {missing_count} required details are missing or unconfirmed."
        elif missing_count > 0 and satisfied_count == 0:
            status = EligibilityStatus.UNCERTAIN
            reasoning = f"Uncertain: Required criteria details ({missing_count} fields) are missing from provided facts."
        elif satisfied_count > 0:
            status = EligibilityStatus.LIKELY_ELIGIBLE
            reasoning = f"Likely Eligible: Satisfies all {satisfied_count} evaluated mandatory criteria based on provided information."
        else:
            status = EligibilityStatus.UNCERTAIN
            reasoning = "Uncertain: Insufficient data to evaluate eligibility criteria."

        return EligibilityItem(
            scheme_id=scheme_id,
            status=status,
            matching_criteria=matching_criteria,
            unmet_criteria=unmet_criteria,
            reasoning=reasoning
        )

    def _parse_rules_to_group(self, rules: Dict[str, Any]) -> RuleGroup:
        """
        Converts rule JSON dictionary into structured RuleGroup.
        """
        conditions: List[RuleCondition] = []
        subgroups: List[RuleGroup] = []
        logical_op = LogicalOperator.AND

        if "logical_operator" in rules:
            logical_op = LogicalOperator(rules["logical_operator"])

        if "conditions" in rules and isinstance(rules["conditions"], list):
            for c in rules["conditions"]:
                op = RuleOperator(c.get("operator", "=="))
                period = PeriodType(c.get("period", "unknown"))
                conditions.append(
                    RuleCondition(
                        field=c["field"],
                        operator=op,
                        value=c["value"],
                        description=c.get("description", f"{c['field']} {op.value} {c['value']}"),
                        period=period,
                        currency=c.get("currency"),
                        is_mandatory=c.get("is_mandatory", True)
                    )
                )

        if "subgroups" in rules and isinstance(rules["subgroups"], list):
            for sub in rules["subgroups"]:
                subgroups.append(self._parse_rules_to_group(sub))

        # Legacy simple key-value dict fallback parsing
        if not conditions and not subgroups:
            for k, v in rules.items():
                if k.startswith("_") or k in ("logical_operator",):
                    continue
                if isinstance(v, bool):
                    conditions.append(RuleCondition(field=k, operator=RuleOperator.EQ, value=v, description=f"Must satisfy {k}"))
                elif isinstance(v, (int, float)):
                    if "max" in k or "limit" in k:
                        conditions.append(RuleCondition(field=k, operator=RuleOperator.LTE, value=v, description=f"{k} must not exceed {v}"))
                    else:
                        conditions.append(RuleCondition(field=k, operator=RuleOperator.GTE, value=v, description=f"{k} must be at least {v}"))
                else:
                    conditions.append(RuleCondition(field=k, operator=RuleOperator.EQ, value=v, description=f"{k} must equal {v}"))

        return RuleGroup(logical_operator=logical_op, conditions=conditions, subgroups=subgroups)

eligibility_engine = EligibilityEngine()
