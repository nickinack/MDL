states = [
    ((agent_x, agent_y), (target_x, target_y), call)
    for agent_x in range(4)
    for agent_y in range(2)
    for target_x in range(4)
    for target_y in range(2)
    for call in range(2)
]
state_mnemonic = lambda x : chr(x[0][0] + 5 * x[0][1] + ord("A")) + chr(x[1][0] + 5 * x[1][1] + ord("A")) + str(x[2]) if x in states else (x if x[0] == "o" else (x + "A"))

X_prob = 1 - ((1031 % 30 + 1) / 100)
reward = (2019101031 % 90) + 10
step_cost = -1

print("discount: 0.5")
print("values: reward")
print("states: ", " ".join([state_mnemonic(x) for x in states]))
print("actions: UA DA LA RA SA")
print("observations: o1 o2 o3 o4 o5 o6")

part1 = True
print("start include: ", end="")
for state in states:
    if (part1 and state[1] == (0, 1) and state[0] not in [(0, 0), (1, 1), (0, 1)]) or (not part1 and state[0] == (1, 1) and state[1] in [(1, 1), (2, 1), (1, 0), (0, 1)] and state[2] == 0):
        print(state_mnemonic(state), end=" ")
print()

def move_entity(state, action, success_prob, stay_prob):
    if action == "S":
        return state, stay_prob
    if action == "U":
        if state[1] <= 0:
            return state, success_prob
        return (state[0], state[1] - 1), success_prob
    if action == "D":
        if state[1] >= 1:
            return state, success_prob
        return (state[0], state[1] + 1), success_prob
    if action == "L":
        if state[0] <= 0:
            return state, success_prob
        return (state[0] - 1, state[1]), success_prob
    if action == "R":
        if state[0] >= 3:
            return state, success_prob
        return (state[0] + 1, state[1]), success_prob

action_opposites = {
    "U": "D",
    "D": "U",
    "R": "L",
    "L": "R"
}

len = 0
transitions = {}
def add_transition(status, prob):
    global len
    if status in transitions.keys():
        transitions[status] += prob
    else:
        transitions[status] = prob
        len += 1

for state in states:
    # Perform actions for the agent
    for action_agent in list("UDLRS"):
        agent_success_state, prob_agent_action = move_entity(state[0], action_agent, X_prob, 1.0)
        agent_failure_state = None
        if agent_success_state != state and action_agent != "S":
            agent_failure_state, prob_agent_failure_action = move_entity(state[0], action_opposites[action_agent], 1 - X_prob, 1.0)
        # Perfom actions for the target
        for action_target in list("UDLRS"):
            target_state, prob_target_action = move_entity(state[1], action_target, 0.1, 0.6)
            
            if state[0] == state[1] and state[2] == 1:
                prob_final = prob_target_action * prob_agent_action
                add_transition((action_agent, state, (agent_success_state, target_state, 0)), prob_final)
                if agent_failure_state is not None:
                    prob_final = prob_target_action * prob_agent_failure_action
                    add_transition((action_agent, state, (agent_failure_state, target_state, 0)), prob_final)
                continue
            
            C = state[2]
            prob_final = prob_target_action * prob_agent_action * (0.5 if state[2] == 0 else 0.9)
            add_transition((action_agent, state, (agent_success_state, target_state, C)), prob_final)
            if agent_failure_state is not None:
                prob_final = prob_target_action * prob_agent_failure_action * (0.5 if state[2] == 0 else 0.9)
                add_transition((action_agent, state, (agent_failure_state, target_state, C)), prob_final)
            
            C = 1 - state[2]
            prob_final = prob_target_action * prob_agent_action * (0.5 if state[2] == 0 else 0.1) # 0 is off , 1 is on
            add_transition((action_agent, state, (agent_success_state, target_state, C)), prob_final)
            if agent_failure_state is not None:
                prob_final = prob_target_action * prob_agent_failure_action * (0.5 if state[2] == 0 else 0.1)
                add_transition((action_agent, state, (agent_failure_state, target_state, C)), prob_final)

for transition, prob in transitions.items():
    print("T:", " : ".join([state_mnemonic(x) for x in transition]), prob)

# Observation Table
observations = {}
for transition in transitions.keys():
    end = transition[2]
    if end[0] == end[1]:
        observations[(transition[0], end)] = "o1"
    elif end[0] == (end[1][0] - 1, end[1][1]):
        observations[(transition[0], end)] = "o2"
    elif end[0] == (end[1][0], end[1][1] - 1):
        observations[(transition[0], end)] = "o3"
    elif end[0] == (end[1][0] + 1, end[1][1]):
        observations[(transition[0], end)] = "o4"
    elif end[0] == (end[1][0], end[1][1] + 1):
        observations[(transition[0], end)] = "o5"
    else:
        observations[(transition[0], end)] = "o6"

for state, obs in observations.items():
    print(f"O: {state[0]}A : {state_mnemonic(state[1])} : {obs} 1.0")
    
# Rewards table
rewards = {}
for transition in transitions.keys():
    start = transition[1]
    end = transition[2]
    obs = observations[(transition[0], end)]
    
    if obs == "o1" and end[2] == 1:
        rewards[(transition[0], start, end, obs)] = reward + step_cost
    else:
        if transition[0] != "S":
            rewards[(transition[0], start, end, obs)] = step_cost
        else:
            rewards[(transition[0], start, end, obs)] = 0

for state, reward in rewards.items():
    print("R:", " : ".join([state_mnemonic(x) for x in state]), reward)