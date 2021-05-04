import numpy as np
import json


# List of all states
physical_states = []
for i in range(0, 2):
    for j in range(0, 4):
        physical_states.append([i,j])
# List of all actions
actions = ["stay", "up", "down", "left", "right"]
call_actions = ["call", "turnoff"]
# List of possible actions for a given state
state_action_dict = {}
# Actual states
states = []
st_ind = 0
for i in range(0, 2):
    for j in range(0, 4):
        agent_pos = [i,j]
        for a in range(0, 2):
            for b in range(0, 4):
                target_pos = [a,b]
                states.append([agent_pos, target_pos, 0, st_ind])
                st_ind += 1
                states.append([agent_pos, target_pos, 1, st_ind])
                st_ind += 1


def transition_function(states, actions):
    target_probabilities = {
        "stay": 0.6,
        "up": 0.1,
        "down": 0.1,
        "left": 0.1,
        "right": 0.1
    }
    call_probabilities = {
        "call": 0.5,
        "turnoff": 0.1
    }
    # x = 1 - (((LastFourDigitsOfRollNumber)%30 + 1) / 100)
    x = 1 - ((1031%30 + 1)/100)
    # x = 0.86
    # x = 0.84
    agent_probabilities = {
        "stay": 1,
        "up": x,
        "down": x,
        "left": x,
        "right": x
    }
    transition_function = []
    for s in states:
        cur_agent_pos = s[0].copy()
        cur_target_pos = s[1].copy()
        cur_call = s[2]
        # change agent position based on actions
        # 5 actions , 5 actions , 2 call_actions (a, b, c)
        for agent_action in actions:
            for target_action in actions:
                next_call_actions = call_actions.copy()
                if cur_agent_pos == cur_target_pos and cur_call == 1:
                    next_call_actions = ['turnoff']
                for call_action in next_call_actions:
                    next_agent_states = [cur_agent_pos.copy(), cur_agent_pos.copy()]
                    agent_prob = []
                    next_target_states = [cur_target_pos.copy()]
                    target_prob = []
                    next_call_states = [cur_call, cur_call]
                    call_prob = []
                    if agent_action == "left":
                        next_agent_states[0][1] = cur_agent_pos[1] + 1
                        next_agent_states[1][1] = cur_agent_pos[1] - 1

                    if agent_action == "right":
                        next_agent_states[0][1] = cur_agent_pos[1] - 1
                        next_agent_states[1][1] = cur_agent_pos[1] + 1
                    
                    if agent_action == "stay":
                        next_agent_states.pop()

                    if agent_action == "up":
                        next_agent_states[0][0] = cur_agent_pos[0] - 1                        
                        next_agent_states[1][0] = cur_agent_pos[0] + 1
                        
                    if agent_action == "down":
                        next_agent_states[0][0] = cur_agent_pos[0] + 1
                        next_agent_states[1][0] = cur_agent_pos[0] - 1

                    agent_prob.append(agent_probabilities[agent_action])
                    agent_prob.append(1 - agent_probabilities[agent_action])
                    

                    if target_action == "left":
                        next_target_states[0][1] = cur_target_pos[1] + 1
                    
                    if target_action == 'right':
                        next_target_states[0][1] = cur_target_pos[1] - 1
                    
                    if target_action == 'up':
                        next_target_states[0][0] = cur_target_pos[0] - 1

                    if target_action == 'down':
                        next_target_states[0][0] = cur_target_pos[0] + 1
                    
                    
                    target_prob.append(target_probabilities[target_action])


                    if check_boundary(next_agent_states[0]):
                        next_agent_states[0] = cur_agent_pos
                    if len(next_agent_states) > 1:
                        if check_boundary(next_agent_states[1]):
                            next_agent_states[1] = cur_agent_pos
                    
                    if check_boundary(next_target_states[0]):
                        next_target_states[0] = cur_target_pos


                    allowed_call = 0

                    if cur_call == 1 and s[0] == s[1]:
                        allowed_call = 2
                        call_action = "turnoff"
                        call_prob.append(1)
                        next_call_states[0] = 0
                        next_call_states.pop()

                    elif call_action == "call" and cur_call == 0:
                        allowed_call = 1
                        next_call_states[0] = 1
                        next_call_states[1] = 0

                    elif call_action == "turnoff" and cur_call == 1:
                        allowed_call = 1
                        next_call_states[0] = 0
                        next_call_states[1] = 1
                    
                    if allowed_call == 1:
                        call_prob.append(call_probabilities[call_action])
                        call_prob.append(1 - call_probabilities[call_action])

                    elif allowed_call == 0:
                        call_prob.append(0)
                        call_prob.append(0)
                    
                    
                    
                    # check for s == [[0, 1], [0, 0], 1] and action == 'left'
                    # if s == [[0, 0], [0, 0], 0] and agent_action == 'stay':
                    #     print('next_target:', next_target_states)
                    #     print('target_action:', target_action)
                    for i in range(0, len(next_agent_states)):
                        for j in range(0, len(next_target_states)):
                            for k in range(0, len(next_call_states)):
                                next_state = [next_agent_states[i], next_target_states[j], next_call_states[k]]
                                next_actual_state = get_state(next_state, states)
                                prob = agent_prob[i] * target_prob[j] * call_prob[k]
                                # if s == [[0, 0], [0, 0], 1, 1] and agent_action == 'stay':
                                #     print('cur_state:', s)
                                #     print('next_state:', next_state)
                                #     print('action:', agent_action)
                                #     print('targetaction:', target_action)
                                #     print('call_action:', call_action)
                                #     print('len(next_target_states):', len(next_target_states))
                                #     print('len(next_agent_states):', len(next_agent_states))
                                #     print('len(next_call_states):', len(next_call_states))
                                #     print('prob:', prob)
                                #     print('-----')
                                ind = get_transition_index(s, next_actual_state, agent_action, transition_function)
                                if ind == -1 and prob > 0:
                                    transition_function.append({"cur_state": s, "action": agent_action, "prob": prob, "next_state": next_actual_state})
                                elif prob > 0: 
                                    transition_function[ind]['prob'] += prob

    return transition_function


def get_transition_index(cur, new_state, action, transition):
    for i in range(len(transition)):
        if transition[i]["cur_state"] == cur and transition[i]["action"] == action and transition[i]["next_state"] == new_state:
            return i
    return -1


def check_boundary(new_position):
    if new_position[0] == -1 or new_position[0] >= 2 or new_position[1] == -1 or new_position[1] >= 4:
        return True
    return False


def get_state(state, states):
    for s in states:
        if s[0] == state[0] and s[1] == state[1] and s[2] == state[2]:
            return s.copy()
    raise Exception("SOMETHING WENT TERRIBLE WRONG OMG OHNO", state)
    return None


def check_prob(cur_state, agent_action, transition):
    additives = 0.0
    for t in transition:
        if t["cur_state"] == cur_state and t["action"] == agent_action:
            additives += t["prob"]
    return additives





transition = transition_function(states, actions)
discount = 0.5
state_count = len(states)
action_count = len(actions)
cnt_observations = 6
observations = [0] * state_count
for state in states:
    if state[0] == state[1]:
        observations[state[3]] = 0
    elif state[0][1] == state[1][1] + 1 and state[0][0] == state[1][0]:
        observations[state[3]] = 1
    elif state[0][0] == state[1][0] - 1 and state[0][1] == state[1][1]:
        observations[state[3]] = 2
    elif state[0][1] == state[1][1] - 1 and state[0][0] == state[1][0]:
        observations[state[3]] = 3
    elif state[0][0] == state[1][0] + 1 and state[0][1] == state[1][1]:
        observations[state[3]] = 4
    else:
        observations[state[3]] = 5


def get_next_states(st, action):
    to_ret = []
    for entry in transition:
        if entry['cur_state'] == st and entry['action'] == action:
            to_ret.append(entry['next_state'].copy())
    return to_ret


action_indices = dict()
for i in range(len(actions)):
    action_indices[actions[i]] = i


reward_tuple = []
reward = ((2019101014) % 90) + 10
reward = ((2019101031) % 90) + 10
# reward = 93
step_cost = -1
for s1 in states:
   for a in actions:
       next_states = get_next_states(s1, a)
       for state in next_states:
            if observations[state[3]] == 0 and state[2] == 1:
                reward_tuple.append({"cur_state": s1[3], "action": action_indices[a], "next_state": state[3], "observation": 0, "reward": reward+step_cost})
            else:
                if a != 'stay':
                    reward_tuple.append({"cur_state": s1[3], "action": action_indices[a], "next_state": state[3], "observation": observations[state[3]], "reward": -1})
                else:
                    reward_tuple.append({"cur_state": s1[3], "action": action_indices[a], "next_state": state[3], "observation": observations[state[3]], "reward": 0})

index_transition = []
for i in range(0, len(transition)):
    index_transition.append({'cur_state': transition[i]["cur_state"][3], 'action': action_indices[transition[i]["action"]], 'next_state': transition[i]['next_state'][3], 'prob': transition[i]['prob']})


start_states = []
start_states_verbose = []
for state in states:
    if state[1] == [1,0] and (state[0] != [1,0] and state[0] != [1, 1] and state[0] != [0, 0]):
        start_states.append(state[3])
        start_states_verbose.append(state)

print(f'discount: 0.5')
print('values: reward')
print(f'states: {len(states)}')
print(f'actions: {len(actions)}')
print(f'observations: {6}')
print(f"start include: {' '.join([str(x) for x in start_states])}")

cnt = 0
for entry in index_transition:
    cnt += 1
    print(f"T: {entry['action']} : {entry['cur_state']} : {entry['next_state']} {entry['prob']}")

for i in range(0, len(states)):
    print(f"O : * : {states[i][3]} : {observations[states[i][3]]} 1.0")

for entry in reward_tuple:
    print(f"R: {entry['action']} : {entry['cur_state']} : {entry['next_state']} : {entry['observation']} {entry['reward']}")

