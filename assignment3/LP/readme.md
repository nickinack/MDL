# Part 3: Linear Programming

## Introduction

In this part of the assignment, we used Linear programming in order to solve the same problem. We used `cvxpy` library in order to calculate the results of linear programming. Similar to the previous assignment, our number of states were 600 and our transition function had 6216 entries. In this part of the assignment, in we had to create a list which stores the state action pairs and index them. The state action pair function, `sap` stores a list of states $S$ and the accessible actions when present in that state, represented by the set $A_{s}$. Once the state action pairs have been created, we used this to create the A and R matrix.

## A-Matrix

The dimensions of the A-Matrix is given by the following tuple:

$$s = (S_{s} , S_{sap})$$

where $S_{s}$  represents the size of the state list and $S_{sap}$ represents the size of the state action pair. The A-matrix keeps track of the inflow and outflow probabilities from a state for a state action pair. In order to understand how we fill in an index in the A-matrix, let us take an example.

![Part%203%20Linear%20Programming%20cff8d323d84b4f99afb1652e2263100e/Untitled.png](Part%203%20Linear%20Programming%20cff8d323d84b4f99afb1652e2263100e/Untitled.png)

Consider an action, indexed by $a_{1}$, causes the flow from state $S_{1}$ to $S_{2},S_{3},S_{4}$ with probabilities $P_{1},P_{2}, P_{3}$ respectively. In order to fill in $A[1][1]$, we calculate the total outflow from state $S_{1}$ caused by the state action pair $x_{1}$. It is calculated as follows:

$$A[1][1] = Outflow_{x_{11}} - Inflow_{x_{11}} \\
A[1][1] = P_{1} + P_{2} + P_{3} - P_{3} \\
A[1][1] = P_{1} + P_{2}$$

Similarly, $A[2][1]$  can be filled as follows:

$$A[2][1] = Outflow_{x_{21}} - Inflow_{x_{21}} \\
A[2][1] = -P_{1} - 0 \\
A[2][1] = -P_{1} $$

We have used this method in order to fill in all the values in the A-matrix. For the terminal state, we have considered a $Noop$ operation. In such cases, the value for a terminal state indexed by $S_{t}$ and state action pair $x_{(t,noop)}$ in A-matrix has been assigned with the value 1.

## Procedure to obtain policy

We have followed the following procedure to obtain the policy.

- We first calculated the reward matrix as follows:

$$R(sap) = \sum_{next}R(S_{current} , S_{next})*P(S_{next}|a)$$

- We then calculated the A-matrix by basing our implementation on the steps explained in the previously. The $\alpha$ matrix was calculated by uniformly distributing the probability of start states.
- We modelled the Linear Programming problem as follows:

$$Maximize: rx \\
Constraints: \\
Ax = \alpha \\
x >= 0
$$

- Once the LPP is solved, it provides us the x-matrix. We select the action with maximum expected value for that state and this gives us the optimal policy denoted by $\pi^{*}$.
- Our results are very similar to that of our Value iteration results even though the rewards when monster transfers from state with $h=n$ to $h = 0$.
- In general, Indiana Jones tends to not stay when my state is 'd'. This can be attributed to the fact that the step cost for staying and moving are the same. Hence, Indiana prefers to make moves which can reduce the health of the monster and hence acquire a reward of +50.
- When the state of monster is 'd', Indiana tends to be more risk seeking. In the absence of arrows and materials, Indiana tends to move towards the east and shoot bullets on the monster even though the probability of success is 0.20.
- Indiana Jones, after the performance of value Iteration tends to balance between the health of the monster and risk averse nature at some cases. For example, when $(h) = 100$, Indiana tends to seek risk, even if he is in the ready state. This is valid for very few cases﻿.

 

## Multiple Policies

There can be multiple policies. Some of the scenarios have been presented below:

- By changing the $\alpha$-matrix, we can change the probabilities of start states. This can lead to a different policy.
- If two actions for a state has the same value (and maximum) in the $x$-matrix, this can also provide us with two different policies as we can choose to take any one of the actions.
- A different step cost can alter the value of $r$-matrix which can ultimately change the $x$-matrix as the maxima for the LPP can give varied results.
- If the probabilities of each of the success/failure of an action is changed, this can also bring in a change in the $r$-matrix, leading to a different policy.
- Precision errors in calculation can also lead to multiple policies.
