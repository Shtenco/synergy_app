# Federation V3 — Personal Capital domain expansion

This repository is the canonical product target for historical **Part III — Personal Capital** of the SYNERGY origin concept.

## Scope to add

1. **Income − Expenses = Delta**
   - monthly cash-flow model;
   - recurring/non-recurring income and expenses;
   - delta allocation rules.

2. **Five-account / envelope budgeting**
   - current expenses;
   - investment/capital account;
   - education/self-development;
   - large purchases/repairs;
   - leisure/discretionary spending;
   - user-configurable percentages and hard caps.

3. **Emergency reserve**
   - target 3–6+ months as a scenario, not a universal prescription;
   - reserve progress and liquidity score.

4. **Debt engine**
   - liabilities registry;
   - avalanche/snowball scenario comparison;
   - debt-service ratio;
   - no hidden leverage assumptions.

5. **Investment ladder state machine**
   `reserve → conservative assets → diversified funds → real assets/business → advanced risk assets`.

6. **Financial-freedom scenario engine**
   - target capital from user expenses and chosen withdrawal assumptions;
   - optimistic/base/pessimistic paths;
   - inflation and contribution sensitivity.

7. **Compound-capital projection**
   - monthly contributions;
   - return distributions rather than guaranteed returns;
   - drawdown/stress paths.

8. **Fund/collective-capital integration**
   - only via typed interfaces to `synergy_financial_os` / `synergy_matrix_sota`;
   - product UI must never represent internal marks as external wealth.

9. **NEXUS assistant**
   - explain and recommend;
   - no autonomous payment or investment authority by default.

## Required invariants

- `forecast != guarantee`;
- `internal valuation != settled external wealth`;
- `AI recommendation != execution`;
- every capital number must carry source/provenance and date.

## Federation dependencies

- accounting truth: `Shtenco/synergy_financial_os`;
- household model: `Shtenco/synergy_matrix_sota`;
- reasoning: `Shtenco/agi_nexus`;
- payments: `Shtenco/synergy_pay_system` only after explicit authorization.
