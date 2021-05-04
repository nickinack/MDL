# Part 2: Value Iteration

Abhishekh Sivakumar

Karthik Viswanathan

Team 103

## Introduction

In this part of the assignment, we performed value iteration for a more complex set of state-action pairs. The cardinality of the state space was 600 and hence, our transition function had 6216 entries. The goal was to find an optimal policy taking into consideration of the following:

- Train the agent (Indiana Jones) in such a way that Indiana Jones, when in a state takes the best action out of all the possible actions which can lead him to the final state most optimally.
- The environment can cause a transfer from one state to the other, and Indiana Jones does not have a say in this. Since Indiana Jones cannot control the shift of states due to environment change, we train him to take actions which takes into consideration the changes in the environment.
- The trace involves the best action Indiana Jones can take at any given point of time for an Iteration, i. The value of i ranges from zero to the k, where k is the iteration when the utilities converge.

# Task 1

## Inferences

The constants assigned for us in this assignment are as follows:

$$\gamma = 0.999 \\
\delta = 10^{-3} \\
s = -10$$

$\gamma$ represents the discount factor, $\delta$ represents the Bellman error and $s$ represents the step cost. When we ran the value iteration algorithm for the given state space, transition function and these constants, we were able to draw the following inferences.

1. The number of iterations our algorithm took to converge was **118**. The convergence condition can be imposed by limiting the change in utilities at time step T ( $U_{T}$) and time step T+1 ($U_{T+1}$) such that the absolute of difference between them $|U_{T+1} +U_{T}|$ is less than the Bellman error, $\delta$.
2. The utilities converge in such a way that the best actions when my monster's state is 'r' is different from that of the utilities when my monster state is 'd'. We observe that depending on the number of arrows  $(a)$  and materials $(m)$ Indiana Jones has, if the monster's health is $(h)$, we have the following conditions: 
- In general, Indiana Jones tends to move towards South if he has no materials in the case of $(m) = 0$ and $(a) = 0$. Once collecting materials, he stays till the state is 'd' and moves towards North in order to collect arrows and shoot when $(h)$ is 25, 50 or 75. Since the step cost is high, when the monster health is 100, Indiana Jones moves to the centre and prefers to shoot two bullets.
- In general, Indiana Jones tends to not stay when my state is 'd'. This can be attributed to the fact that the step cost for staying and moving are the same. Hence, Indiana prefers to make moves which can reduce the health of the monster and hence acquire a reward of +50.
- When the state of monster is 'r' , Indiana tends to be more risk averse in general. He tends to move towards the north or south in order to gain materials and stay so that when the ready state switches to the dormant state, Indiana can use the materials/arrows he collected in order to make further moves to destroy the monster.
- When the state of monster is 'd', Indiana tends to be more risk seeking. In the absence of arrows and materials, Indiana tends to move towards the east and shoot bullets on the monster even though the probability of success is $0.2$.
- Indiana Jones, after the performance of value Iteration tends to balance between the health of the monster and risk averse nature at some cases. For example, when $(h) = 100$, Indiana tends to seek risk, even if he is in the ready state. This is valid for very few cases.

We will now draw some inferences on the change in policy from the results we got after performing value iteration.

## Simulation

Running a simulation with start state as `(W, 0, 0, d, 100)` gives us the following:

```markdown
Current state: {'direction': 'W', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 484}
Best action: mc
Next state: {'direction': 'C', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 4}
-----------
Current state: {'direction': 'C', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 4}
Best action: me
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 100, 'index': 369}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 100, 'index': 369}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 364}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 100, 'index': 369}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 100, 'index': 369}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 50, 'index': 367}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 50, 'index': 367}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 75, 'index': 363}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 75, 'index': 363}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 361}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 361}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 361}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 361}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 361}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 361}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 361}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 361}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 25, 'index': 366}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 25, 'index': 366}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 25, 'index': 366}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 25, 'index': 366}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 25, 'index': 366}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 25, 'index': 366}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 362}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 362}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 362}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 362}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 362}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 362}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 362}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 362}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 362}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 362}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 0, 'index': 365}
-----------
```

Observations:

- The environment switches between MM's state as ready and dormant with a probability of 0.5, with the transition from ready to dormant state results in boosting MM's health by 25.
- Agent has 0 arrows. It relies on the fifty damage dealt by the blade per hit on MM's health.
- Agent traverses from the `West` location to `Center` where the probability of blade hitting MM and dealing fifty damage is 0.1.
- Agent makes one further move to the `East` location since the probability of hitting MM with blade is 0.2 (higher than at location `Center`).
- The agent relies on continuous blade hits to bring the health of MM down to zero and reach terminating state.

Simulation with starting state as `C, 2, 0, R, 100` results in the following sequence of decisions made by the agent:

```markdown
Current state: {'direction': 'C', 'material': 2, 'arrow': 0, 'state': 'r', 'health': 100, 'index': 89}
Best action: mn
Next state: {'direction': 'N', 'material': 2, 'arrow': 0, 'state': 'r', 'health': 100, 'index': 209}
-----------
Current state: {'direction': 'N', 'material': 2, 'arrow': 0, 'state': 'r', 'health': 100, 'index': 209}
Best action: um
Next state: {'direction': 'N', 'material': 1, 'arrow': 0, 'state': 'd', 'health': 100, 'index': 204}
-----------
Current state: {'direction': 'N', 'material': 1, 'arrow': 1, 'state': 'd', 'health': 100, 'index': 204}
Best action: um
Next state: {'direction': 'N', 'material': 0, 'arrow': 3, 'state': 'd', 'health': 100, 'index': 214}
-----------
Current state: {'direction': 'N', 'material': 20, 'arrow': 3, 'state': 'd', 'health': 100, 'index': 234}
Best action: mc
Next state: {'direction': 'E', 'material': 0, 'arrow': 3, 'state': 'd', 'health': 100, 'index': 474}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 3, 'state': 'd', 'health': 100, 'index': 474}
Best action: sa
Next state: {'direction': 'E', 'material': 0, 'arrow': 2, 'state': 'd', 'health': 75, 'index': 463}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 2, 'state': 'd', 'health': 75, 'index': 463}
Best action: sa
Next state: {'direction': 'E', 'material': 0, 'arrow': 1, 'state': 'd', 'health': 75, 'index': 453}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 1, 'state': 'd', 'health': 75, 'index': 453}
Best action: sa
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 442}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 442}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 50, 'index': 447}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 50, 'index': 447}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 75, 'index': 443}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 75, 'index': 443}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 75, 'index': 443}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 75, 'index': 443}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 441}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 441}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 441}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 25, 'index': 441}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 25, 'index': 446}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 25, 'index': 446}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 442}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 442}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 442}
-----------
Current state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'd', 'health': 50, 'index': 442}
Best action: sb
Next state: {'direction': 'E', 'material': 0, 'arrow': 0, 'state': 'r', 'health': 0, 'index': 445}
-----------
```

Observations:

- Unlike the previous case, here, we start out with two materials and the monster already in ready state.
- Agent can escape the `-40` reward that accompanies MM's hits on IJ when IJ is on location `Center` or `East` as well as utilize the two materials by moving to the `North` location.
- Upon reaching `North`, the 2 materials are utilized to gather arrows.
- Monster being in 100 health leads the agent to create maximum number of arrows. So, it performs `CRAFT` action twice.
- An interesting observation to be made (but was not captured in the simulation) was the behavior of the agent at state `N, 0, 3, r, 100` . The best action recommended by the policy is to "stay" at that state. Moving to center results in exposure to possible attacks, and `CRAFT` is not viable due to insufficient material count. Hence, the agent waits for the MM transition from ready to dormant state before making the move to `Center` location.
- Once at center, the agent shoots arrows and hits blade from the `East` location (due to higher probabilities of hitting MM).

# Task 2

### Case 1

We introduce a new action which can be performed when the agent is present in the east state. Before the introduction of this new action, the possible actions which can be taken when the agent is present in the 'E' state are as follows:

$$A(E) = [center, arrow, bullet, stay]$$

The new dictionary after the introduction of the new action is as follows:

$$A'(E) = [arrow, bullet, stay, west]$$

The inferences are as follows:

- The number of iterations our algorithm took to converge was **120**. The convergence condition can be imposed by limiting the change in utilities at time step T ( $U_{T}$) and time step T+1 ($U_{T+1}$) such that the absolute of difference between them $|U_{T+1} +U_{T}|$ is less than the Bellman error, $\delta$.
- In the presence of no arrows and no materials, Indiana Jones, in general tends to move to the east and shoot bullets irrespective of the monster's health in order to compensate for the high step cost. When $(h)$ is considerably high (75, 100), and the state transition occurs from 'd' to 'r', Indiana Jones teleports from East to West. But if $(h)$ is considerably small (25, 50), Indiana Jones takes the risk of shooting arrows.
- Since the action space has been increased, it is evident that the magnitude of the utilities are more negative compared to that of Task 1. This is because the action space has to account for an extra action which contributes a -10 step cost.

### Case 2

The change we introduce in the second state is reducing the cost of the STAY action to zero. Previously, in Task 1, the cost of the STAY action was given as follows:

$$C(STAY) = -10$$

In this case, our stay cost is given as follows:

$$C'(STAY) = 0$$

The inferences are as follows:

- The number of iterations our algorithm took to converge was 57. The convergence condition can be imposed by limiting the change in utilities at time step T ( $U_{T}$) and time step T+1 ($U_{T+1}$) such that the absolute of difference between them $|U_{T+1} +U_{T}|$ is less than the Bellman error, $\delta$.
- The possible reason for the quick convergence could be attributed to the fact that it is most likely cheaper for the agent to perform `Stay` action rather due to the zero step cost.
- This also results in possible cop-outs by the agent, because now the agent has the option to locate to a safe square (such as the `West` location) and `Stay` there indefinitely, irrespective of MM's state) without accumulating negative rewards (which would otherwise push the agent away from making such a decision as noticed from part 2).
- When the monster is in the 'r' state, in general, Indiana Jones tends to stay in North/South/West locations instead of collecting/using materials. In west, if arrows are present and the monster is in 'r' state, Indiana Jones tends to stay and wait for ready to dormant transition so IJ can move to the centre and attack as shooting from centre/east has better success rate than shooting from west.
- The utility values are less compared to that of the previous cases. This can be attributed to the fact that the stay action has a cost of 0.
- The optimal policy enforces Indiana Jones to be more Risk Averse than Risk seeking, since the agent finds `West` location to be a comfortable spot to camp out forever.

### Case 3

In this case, we experiment with the discount factor. The discount factor in Task 1 was given as follows:

$$\gamma = 0.999$$

In this case, the discount factor is given as follows:

$$\gamma = 0.25$$

The inferences are as follows:

- The number of iterations our algorithm took to converge was 8. The convergence condition can be imposed by limiting the change in utilities at time step T ( $U_{T}$) and time step T+1 ($U_{T+1}$) such that the absolute of difference between them $|U_{T+1} +U_{T}|$ is less than the Bellman error, $\delta$.
- The reason for the early convergence can be attributed to the discount factor. Due to lower discount factor, the values converge early. This gives the agent only short term considerations and ignores the occurrences in long term.
- Even in the presence of materials, Indiana Jones tends to gather materials and tends to exhaust the materials even after the maximum arrow count has been attained. This is because Indiana can only witness the foreseeable future and not long term results.
- It can also be observed that the range of the values of convergences for most of the states are very similar (-13 for most and 20-25 for some states).

## Details on trace and simulations

The trace and the simulations have been attached along with the report as a part of the submission folder. We have tried to perform a real time simulation where depending on the environment, an action can fail and pass (Probabilities of success and failure of an action have been taken in account). We have restricted Indiana Jones from deliberately moving from one state with monster state 'r' to 'd' and vice versa as only the environment can lead to such changes.
