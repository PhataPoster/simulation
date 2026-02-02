# Simulation (Class 1–2) — Answers (Based on Slides)

## 1(a) What is a System? Describe ways to study a system. (6)

**System:** A collection of entities (e.g., people, machines) that interact together toward the accomplishment of some logical end.

- What is meant by **“the system” depends on the objectives** of the study.
  - Example (bank): If the goal is teller staffing, the system may include only tellers + customers waiting/being served.
  - If the study includes loan officer and safe-deposit boxes, the system definition expands.

**Ways to study a system (as shown in slides):**

1) **Experiment with the actual system**
- If feasible and cost-effective, changing the real system and observing it is ideal (validity is not in doubt).
- Often not feasible because it can be too costly or disruptive.

2) **Experiment with a model of the system**
- Useful when real experimentation is disruptive/expensive, or when the “system” does not exist yet.

   a) **Physical model** (e.g., scaled mockups, training cockpits, etc.)

   b) **Mathematical model** (most common): represents the system via logical/quantitative relationships.

3) **Analytical solution vs Simulation (for mathematical models)**
- If the model is simple enough, an **exact analytical** solution may be possible.
- Many realistic systems are complex → analytical solution not possible → use **simulation** (numerically exercise the model and observe performance).

---

## 1(b) Desirable features of Simulation Software (6)

> Note: This item is not listed explicitly in the extracted slide text, but the slides describe the components of a discrete-event simulator. The features below align with those slide requirements.

- **Event list / event calendar support** (schedule, cancel, and process events; correct tie-breaking when events share the same time).
- **Time-advance mechanism** (simulation clock + timing routine).
- **Entity/attribute/queue/resource modeling** (e.g., server busy/idle, FIFO queues, customer arrival times as attributes).
- **Random number and random variate generation library** (exponential, uniform, discrete distributions, etc.).
- **Statistics collection & reporting** (time-average areas like \(\int Q(t)dt\), customer-average delays, multiple performance measures).
- **Experiment support** (multiple runs/replications, seed control, scenario comparison, output summaries).

---

## 2(a) Key differences between event-scheduling approach and process approach. Why is process approach better? (8)

> Note: Your slides emphasize discrete-event simulation with **event list + timing routine + event routine** (event-scheduling view). “Process approach” is the standard process-interaction alternative.

### Event-scheduling approach (slide-aligned)
- Maintain an **event list** containing next time of each event type.
- A **timing routine** selects the next event and advances the simulation clock.
- An **event routine** updates the state when that event occurs (arrival, departure, demand, order arrival, etc.).
- The modeler explicitly manages scheduling and state transitions.

### Process approach (process-interaction)
- Each entity is modeled as a **process/lifecycle** (e.g., a customer: arrive → wait in FIFO → seize server → service → depart).
- The simulation engine translates process actions into underlying events.

### Why process approach is often considered better
- **More natural modeling** for flow-based systems.
- **Modularity**: logic grouped per entity process instead of scattered among event routines.
- **Less error-prone** for complex systems: engine handles many event-scheduling details.
- **Easier to scale** to many resources/queues/branches.

---

## 2(b) Differentiate between Deterministic and Stochastic Simulation Models. (4)

- **Deterministic simulation model**: contains no random (probabilistic) components. Once inputs/relationships are fixed, output is fully determined.
- **Stochastic simulation model**: contains random inputs (e.g., interarrival times, service times). Output is also random and must be treated as an **estimate** of the true characteristics.

---

## 3(a) Why calibration and validation of models are necessary? How they are done in reality? (8)

> Note: The extracted slides focus on DES structure and examples; calibration/validation is standard simulation methodology used with those models.

### Why necessary
- To ensure the model represents the real system **well enough for the study objective**.
- Without validation, simulation results can lead to incorrect decisions.

### How done in reality
- **Data collection** from the real system (arrival/service/lead-time/demand data).
- **Calibration**: fit/estimate parameters and distributions (e.g., exponential mean, uniform bounds, discrete demand probabilities).
- **Verification**: confirm the code correctly implements the conceptual model (trace/debug, step-by-step event checking, extreme-case tests).
- **Validation**:
  - Compare model outputs to real historical performance (delays, queue lengths, utilizations, costs).
  - Expert/face validation: subject-matter experts judge reasonableness.
  - Sensitivity analysis: check robustness against key assumptions.
- Iterate until acceptable agreement for the intended use.

---

## 3(b) Defense-related simulation: Simulation Software or Programming Languages? Argue. (4)

A reasonable argument (commonly accepted):

- **Programming languages** are often more suitable for defense simulations when you need:
  - high fidelity and custom behaviors,
  - performance and real-time constraints,
  - deep integration with external systems,
  - strict security and audit requirements.

- **Simulation software** is strong for:
  - rapid prototyping, scenario building, visualization,
  - quicker development when fidelity/integration demands are moderate.

Conclusion: **for high-fidelity defense/operational simulation, programming languages are usually preferred**, while simulation software is often ideal in early prototyping/training contexts.

---

## 4(a) Describe simulation of a Single-Server Queueing System. (6)

**Model (from slides):**
- Single server, FIFO queue.
- Interarrival times \(A_1, A_2, \dots\) are IID.
- Service times \(S_1, S_2, \dots\) are IID and independent of interarrival times.
- Start in **empty-and-idle** state.

**State variables (slides):**
- Server status (idle/busy)
- Number in queue
- Arrival time of each customer waiting in queue

**Discrete-event simulation organization (slides):**
- Simulation clock
- Event list (next arrival time, next service completion time)
- Statistical counters
- Initialization routine
- Timing routine (select next event, advance time)
- Event routines (arrival, departure)
- Random variate generation routines

**Performance measures (slides):**
- Average delay in queue of \(n\) customers: \(\hat d(n)=\frac{1}{n}\sum_{i=1}^n D_i\)
- Time-average number in queue: \(\hat q(n)=\frac{\int_0^{T(n)} Q(t)\,dt}{T(n)}\)

---

## 4(b) Describe simulation of an Inventory System. (6)

**Model (from slides):**
- Monthly review for \(n\) months.
- Demand arrivals: interdemand times are IID exponential (mean 0.1 month).
- Demand size \(D\) is discrete with a given distribution.
- Lead time (delivery lag): uniform between 0.5 and 1 month.

**(s, S) policy (slides):**
- At the beginning of each month, observe inventory level \(I\).
- If \(I < s\), order \(Z=S-I\); otherwise order \(Z=0\).
- Ordering cost: \(K+iZ\) if \(Z>0\) (no cost if \(Z=0\)).

**Backlogging (slides):**
- If demand exceeds inventory, backlog occurs (inventory can become negative).
- When an order arrives, it first reduces backlog, then increases on-hand inventory.

**Costs (slides):**
- Holding cost: \(h\) per item per month on \(I^+(t)=\max(I(t),0)\)
- Backlog cost: \(\pi\) per item per month on \(I^-(t)=\max(-I(t),0)\)
- Use time-average integrals to compute average costs per month.

---

## 5(a) Compute \(\hat q(n)\). (6)

Given:
- Arrivals at times: 0.4, 1.6, 2.1, 3.8, 4.0, 5.6, 5.8, 7.2
- Departures at times: 2.4, 3.1, 3.3, 5.6, 9.0
- Simulation ends at \(T(n)=9.0\)

Recall: \(Q(t)\) counts **customers waiting in queue only** (not in service).

Queue-length intervals:
- 1.6 → 2.1: \(Q=1\)
- 2.1 → 2.4: \(Q=2\)
- 2.4 → 3.1: \(Q=1\)
- 4.0 → 5.6: \(Q=1\)
- 5.6 → 5.8: \(Q=1\)
- 5.8 → 7.2: \(Q=2\)
- 7.2 → 9.0: \(Q=3\)

Area under \(Q(t)\):
\[
\int_0^{9} Q(t)\,dt =
(0.5) + (0.6) + (0.7) + (1.6) + (0.2) + (2.8) + (5.4) = 11.8
\]

Therefore:
\[
\hat q(n)=\frac{11.8}{9.0} \approx 1.31
\]

---

## 5(b) Tandem (2 servers in series): what to estimate and how (6)

Given:
- Interarrival to server 1: IID exponential, mean 1 minute (\(\lambda=1\) per minute)
- Service at server 1: IID exponential, mean 0.5 minute (\(\mu_1=2\) per minute)
- Service at server 2: IID exponential, mean 1.0 minute (\(\mu_2=1\) per minute)

**What to estimate for each server (DES, slide-style):**

For each server \(j\in\{1,2\}\) over a run of length \(x\) minutes:

1) **Expected average delay in queue**
- Track each customer’s delay before service at that server.
- Estimator: \(\hat d_j = \frac{1}{n_j}\sum_{i=1}^{n_j} D_{j,i}\), where \(n_j\) is the number of customers whose queue delays are completed/observed at server \(j\).

2) **Expected time-average number in queue**
- Maintain area under queue-length curve: \(\int_0^x Q_j(t)dt\).
- Estimator: \(\hat q_j = \frac{1}{x}\int_0^x Q_j(t)dt\).

3) **Expected utilization**
- Track busy time of each server.
- Estimator: \(\hat \rho_j = \frac{\text{busy time of server }j}{x}\).

**Important observation from the given means:**
- Server 1 utilization (expected): \(\rho_1=\lambda/\mu_1=1/2=0.5\) → stable.
- Server 2 utilization (expected): \(\rho_2=\lambda/\mu_2=1\) → *critical loading*. In steady-state, server 2 can have very large queues; for finite \(x\), simulation gives finite-horizon estimates.

> To compute numeric estimates, the value of \(x\) must be specified, and you typically run multiple replications to estimate the expected values.
