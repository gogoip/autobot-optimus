# Demo Walkthrough (10 Minutes)

## Setup
- Start backend and UI.
- Load seeded baseline data.

## Step 1: Baseline
Ask agent: "Show current batch KPIs for last 7 days."
Expected:
- Batch window around 3h
- Peak contention around 01:00
- 1-2 recurring SLA misses

## Step 2: Diagnosis
Ask agent: "Diagnose top bottlenecks and root causes."
Expected findings:
- High spool + skew in one transform job
- Artificial serialization in dependency graph
- Concurrency overload in heavy class jobs

## Step 3: Plan
Ask agent: "Propose an optimization plan with risk and expected impact."
Expected actions:
- Shift two heavy jobs earlier
- Add heavy-class concurrency cap
- Remove one non-essential dependency edge
- Generate two stats collection statements

## Step 4: Approval + Execution
Approve recommended actions in UI.
Expected:
- Agent executes simulator actions
- Audit records created for every action

## Step 5: Verification
Ask agent: "Compare before vs after and summarize impact."
Expected:
- Lower peak utilization
- Shorter overall batch window
- Fewer SLA misses

## Step 6: Reflection
Ask agent: "What should be the next best action?"
Expected:
- One incremental recommendation with rationale and confidence

