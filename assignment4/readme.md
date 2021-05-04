# Part 1 and 2: Belief and SARSOP Solver

Abhishekh Sivakumar: 2019101014

Karthik Viswanathan: 2019103015

## Introduction

In this part of the assignment, we calculate beliefs in order for the following observations:

1. Agent took the action Right and observed Green.
2. Agent took the action Left and observed Red.
3. Agent took the action Left and observed Green.

The formula required to calculate the new belief, $b'(s')$ from the existing state $b$ given observation $o$ is as follows:

$$b'(s') = \frac{O(s',a,o).\sum(T(s,a,s')b(s))}{P(o|a,b)}$$

The values of $x$ and $y$ derived from roll number are as follows:

$$RollNumber = 2019101014\\
x = 0.75 \\
y = 3$$

The initial beliefs, $b$ can be formulated as an array as follows:

$$b = (\frac{1}{3}, 0, \frac{1}{3}, 0, 0, \frac{1}{3})$$

## Calculation

### Step 1

If the agent took action right and observed green. Probability that my observation is green given that I take an action right is probability that my observation is green and my state is green plus my observation is green and my state is red. But these need to be multiplied by the probabilities of the success and failures of my state being in red and green.

$P(s=s1,a=right, s'=s2) = 0.75$ 

$P(s=s1, a=right,s'=s1)=0.25$

From the table, we get the following probabilities:

$P(observation=green|state=green)=0.9$

$P(observation=red|state=red)=0.85$

$P(observation=green|state=red)=0.15$

$P(observation=red|state=green)=0.1$

From state $s_1$,

$b'(s1) = 0.25 * 0.15*\frac{1}{3}=0.0125$

$b'(s2) = 0.75*0.9*\frac{1}{3}=0.225$

$b(s_2)=0$ hence we can skip calculating the associated actions for the state $s_2$

From state $s_3$

$P(s=s_3,a=right,s'=s_4)=0.75$

$P(s=s_3, a=right,s'=s_2)=0.25$

$b'(s_2)=0.25*0.9*\frac{1}{3}=0.075$

$b'(s_4)=0.75*0.9*\frac{1}{3}=0.225$

State $s_4$ has $b(s_4)=0$ hence we skip calculating the associated actions for this state.

The same applies for state $s_5$ so we skip its associated actions.

For state $s_6$,

$P(s=s_6,a=right,s'=s_6)=0.75$

$P(s=s_6,a=right,s'=s_5)=0.25$

$b'(s_6)=0.75*0.15*\frac{1}{3}=0.0375$

$b'(s_5)=0.25*0.9*\frac{1}{3}=0.075$

The new unnormalized beliefs can be written as follows:

$$ub = (0.0125, \\
0.3, \\
0, \\
0.225, \\
0.075,\\
0.0375)$$

The new beliefs is thus as follows:

$$b = (0.01923077, 0.46153846, 0.        , 0.34615385, 0.11538462,
       0.05769231)$$

### Step 2

We use the new beliefs in order to calculate the new beliefs for step two. The agent took the action left and observed red. Let us evaluate the new beliefs of the states as follows:

At state $s_{1}$,

$$P(s=s_{1}, a=left, s'=s_{1})=0.75 \\
P(s=s_{1}, a=left, s'=s_{2})=0.25$$

$$P(observation=red|state=red) = 0.85 \\
P(observation=red|state=green)=0.1$$

$$b'(s_{1}) = 0.75*0.85*0.019230769230769235= 0.012259615384615386$$

$$b'(s_{2}) = 0.25*0.1*0.019230769230769235= 0.0004807692307692308$$

At state $s_{2}$,

$$P(s=s_{2}, a=left, s'=s_{1})=0.75 \\
P(s=s_{2}, a=left, s'=s_{3})=0.25$$

$$P(observation=red|state=red)=0.9$$

$$b'(s_{1})=0.75*0.85*0.46153846153846156= 0.294230769230769$$

$$b'(s_{3})=0.25*0.85*0.46153846153846156 =0.09807692307692308$$

We do not have to calculate for $s_{3}$ as the belief is zero.

At state $s_{4}$,

$$P(s=s_{4},a=left,s'=s_{3})=0.75 \\
P(s=s_{4},a=left,s'=s_{5})=0.25$$

$$P(observation=red|state=green)=0.15 \\
P(observation=red|state=red)=0.9$$

$$b'(s_{3})=0.75*0.85*0.3461538461538462= 0.22067307692307694$$

$$b'(s_{5})=0.25*0.1*0.3461538461538462=0.008653846153846153$$

At state $s_{5}$,

$$P(s=s_{5},a=left,s'=s_{4})=0.75 \\
P(s=s_{5},a=left,s'=s_{6})=0.25$$

$$P(observation=red|state=green)=0.15 \\
P(observation=red|state=red)=0.9$$

$$b'(s_{4})=0.75*0.1*0.1153846153846= 0.008653846153846153$$

$$b'(s_{6})=0.25*0.85*0.11538461538461539=0.02451923076923077$$

At state $s_{6}$,

$$P(s=s_{6},a=left,s'=s_{5})=0.75 \\
P(s=s_{6},a=left,s'=s_{6})=0.25$$

$$P(observation=red|state=green)=0.15 \\
P(observation=red|state=red)=0.9$$

$$P(observation=red|action=left)=0.75*0.15+0.9*0.25=0.3375$$

$$b'(s_{5})=0.75*0.1*0.05769230769230771= 0.004326923076923077$$

$$b'(s_{6})=0.25*0.85*0.05769230769230771=0.012259615384615388$$

The new unnormalized beliefs can be assigned as follows:

$$ub = (0.30649038, 0.00048077, 0.31875,    0.00865385, 0.01298077,
 0.03677885)$$

Hence, the new belief is thus,

$$b = (0.44799719, 0.00070274, 0.46591708, 0.01264933,
       0.018974  , 0.05375966)$$

### Step 3

We use the new beliefs in order to calculate the new beliefs for step two. The agent took the action left and observed green. Let us evaluate the new beliefs of the states as follows:

At state $s_{1}$,

$$P(s=s_{1},a=left,s'=s_{1})=0.75 \\
P(s=s_{1},a=left,s'=s_{2})=0.25$$

$$P(observation=green|state=green)=0.9 \\
P(observation=green|state=red)=0.15$$

$$b'(s_{1})=0.75*0.15*0.4479971890372453=0.0503996837666901$$

$$b'(s_{2})=0.25*0.9*0.4479971890372453=0.10079936753338019$$

At state $s_{2}$,

$$P(s=s_{2},a=left,s'=s_{1})=0.75 \\
P(s=s_{2},a=left,s'=s_{3})=0.25$$

$$b'(s_{1})=0.75*0.15*0.0007027406886858749=7.905832747716094e-05$$

$$b'(s_{3})=0.25*0.15*0.0007027406886858749=2.6352775825720312e-05$$

At state $s_{3}$,

$$P(s=s_{3},a=left,s'=s_{2})=0.75 \\
P(s=s_{3},a=left,s'=s_{4})=0.25$$

$$P(observation=green|state=green)=0.9 \\
P(observation=green|state=red)=0.15$$

$$b'(s_{2})=0.75*0.9*0.4659170765987351= 0.3144940267041462$$

$$b'(s_{4})=0.25*0.9*0.465917076598735= 0.1048313422347154$$

At state $s_{4}$,

$$P(s=s_{4},a=left,s'=s_{3})=0.75 \\
P(s=s_{4},a=left,s'=s_{5})=0.25$$

$$P(observation=green|state=green)=0.9 \\
P(observation=green|state=red)=0.15$$

$$b'(s_{3})=0.75*0.15*0.012649332396345747=0.0014230498945888967$$

$$b'(s_{5})=0.25*0.9*0.01264933239634574=0.0028460997891777934$$

At state $s_{5}$,

$$P(s=s_{5},a=left,s'=s_{4})=0.75 \\
P(s=s_{5},a=left,s'=s_{6})=0.25$$

$$P(observation=green|state=green)=0.9 \\
P(observation=green|state=red)=0.15$$

$$b'(s_{4})=0.75*0.9*0.01897399859451862=0.01280744905130007$$

$$b'(s_{6})=0.25*0.1*0.01897399859451862=0.0007115249472944483$$

At state $s_{6},$

$$P(s=s_{6},a=left,s'=s_{5})=0.75 \\
P(s=s_{6},a=left,s'=s_{6})=0.25$$

$$P(observation=green|state=green)=0.9 \\
P(observation=green|state=red)=0.15$$

$$b'(s_{5})=0.75*0.9*0.05375966268446943= 0.03628777231201687$$

$$b'(s_{6})=0.25*0.15*0.05375966268446943=0.002015987350667604$$

The new unnormalized beliefs can be assigned as follows:

$$b = (0.05047874, 0.41529339, 0.0014494,  0.11763879, 0.03913387,
 0.00272751)
$$

Hence, the new beliefs are

$$b = (0.08054411, 0.66264402, 0.00231267, 0.18770499,
       0.06244218, 0.00435203)$$

## Introduction

In this part of the assignment, we use the SARSOP solver in order to get an optimal policy for the problem mentioned. The roll number being used in order to solve the problems is **2019101014**. We started our by creating appropriate transition functions, indexed the state and actions, created the rewards matrix and plugged them all into the POMDP file. We ran the SARSOP file and we have answered the questions below.

## Steps

The following steps were followed while writing the code:

1. Initially, we started out by creating the states, as follows. The states were of the following format: $[(a,b), (c,d), c']$ where the first list represented the position of the agent, the second list represented the position of the target and third entity was to represent the call status (on/off). After creating the states, we indexed each of them. 
2. The actions for state set was written as a dictionary and then each of the action were also indexed.
3. The transition function was branched according to the target actions and was the entities were the indexed current states, next states and the actions.
4. The reward was calculated for a $(start, action, next, observation)$ tuple and since the accuracy of the observation was 100 percent, the reward was unique for the given tuple.
5. Once all of these were created, all of these were dumped into a file and then we ran the solver and simulated according to the questions.

## Questions

1. The policy has been attached along with this report as a part of the submission. Initially, the belief states of all the states other than the states of the following format were zero: $s = [(a,b), (1,0), 0/1]$ where $a$ and $b$ represented the coordinates for the nearest neighboring states of $(1,0)$. For state indexed as $s$, the probabilities were distributed equally as $0.1$. The states were indexed as follows: 

    $$s = [24 \ 25 \ 40 \ 41 \ 56 \ 57 \ 104 \ 105 \ 120 \ 121]$$

    Initial Belief state is:

    ```bash
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.1, 0, 0, 0, 0, 0, 0)
    ```

2. For the following states indexed, the beliefs are $1/4$. For the other states, the beliefs are 0. 

    $$s = [82 \ 88 \ 90 \ 92]$$

    Initial Belief state is:

    ```bash
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0, 0, 0, 0, 0, 0.25, 0, 0.25, 0, 0.25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    ```

3. The expected utility given the initial belief states for $q1$ is $0.610055$ and for $q2$ is $10.9865$.

     The simulation for the first questions is as follows:

    ![Part%201%20and%202%20Belief%20and%20SARSOP%20Solver%20426b37b02c1c49ef812199224c6aaf56/Untitled.png](Part%201%20and%202%20Belief%20and%20SARSOP%20Solver%20426b37b02c1c49ef812199224c6aaf56/Untitled.png)

    The simulation for the second question is as follows:

    ![Part%201%20and%202%20Belief%20and%20SARSOP%20Solver%20426b37b02c1c49ef812199224c6aaf56/Untitled%201.png](Part%201%20and%202%20Belief%20and%20SARSOP%20Solver%20426b37b02c1c49ef812199224c6aaf56/Untitled%201.png)

4. The approach we took for this question was to sum up the probabilities of start states having the same observation $o$ and selected the observation with the maximum probability value. The results we got are: observation $6$ with net probability $0.75$. The reason for this is likely that since the accuracy of the observation is $1$ and majority of the target states are not neighbouring to the agent states, observation $6$ is the most observed.  The sum of observations are as follows:

    $$P(O) = [0,0.1,0,0.15,0,0.75]$$

5. The formula for calculating the number of trees is as follows:

$$T = A^{\frac{(O^{H}-1)}{(O-1)}}$$

![Part%201%20and%202%20Belief%20and%20SARSOP%20Solver%20426b37b02c1c49ef812199224c6aaf56/Untitled%202.png](Part%201%20and%202%20Belief%20and%20SARSOP%20Solver%20426b37b02c1c49ef812199224c6aaf56/Untitled%202.png)

 $O$ is the number of observations, $A$  is the number of actions and $H$ is the horizon value (number of trials = $37$). Hence the number of policy trees are:

$$T = 5^{1.6040993e+31}$$

![Part%201%20and%202%20Belief%20and%20SARSOP%20Solver%20426b37b02c1c49ef812199224c6aaf56/Untitled%203.png](Part%201%20and%202%20Belief%20and%20SARSOP%20Solver%20426b37b02c1c49ef812199224c6aaf56/Untitled%203.png)
