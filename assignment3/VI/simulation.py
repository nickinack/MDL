import json
import numpy as np


def create_states():
    '''
    Inputs: State array (null array)
    Outputs: State array (non-null array with states)
    '''
    states = []
    direction = ['C', 'N', 'S', 'E', 'W']
    material = [0, 1, 2]
    arrow = [0, 1, 2, 3]
    state = ['d' , 'r']
    health = [0, 25, 50, 75, 100]
    index = 0
    for i in range(len(direction)):
        for j in range(len(material)):
            for k in range(len(arrow)):
                for l in range(len(state)):
                    for m in range(len(health)):
                        states.append({"direction": direction[i], "material": material[j], "arrow": arrow[k], "state": state[l], "health": health[m], "index": index})
                        index += 1
    return states

def get_state_from_diction(diction, states):
    for state in states:
        if state["direction"] == diction["direction"] and state["material"] == diction["material"] and state["arrow"] == diction["arrow"] and state["state"] == diction["state"] and state["health"] == diction["health"]:
            return state.copy()


def get_next_state_values(cur_state, action, transition_table):
    possible_next_states = []
    probability = []
    for entry in transition_table:
        # if not entry['next_state']:
        #     print('NONE FOUND--------')
        if entry['cur_state'] == cur_state and entry['action'] == action:
            possible_next_states.append(entry['next_state'])
            probability.append(entry['prob'])
    return (possible_next_states, probability)


def rewards(state, next_state):
    if state["state"] == "r" and next_state["state"] == "d" and state["direction"] in ['C', 'E']:
        return -50
    if state["health"] != 0 and next_state["health"] == 0:
        return 40
    return -10



action_set = {
    'C': ['me', 'ms', 'mn', 'mw', 'sb', 'sa', 'stay'],
    'N': ['mc', 'um', 'stay'],
    'S': ['mc', 'gm', 'stay'],
    'W': ['mc', 'sa', 'stay'],
    'E': ['mc', 'sb', 'sa', 'stay']
}

def get_next_state(state, action, states):
    new_state = state.copy()
    
    if state['state'] == 'd':
        if np.random.uniform(0, 1) <= 0.2:
            new_state['state'] = 'r'
    
    can_take_action = True
    if state['state'] == 'r':
        if np.random.uniform(0, 1) <= 0.5:
            if state['direction'] in ['C', 'E']:
                new_state['arrow'] = 0
                can_take_action = False
            new_state['state'] = 'd'
            new_state['health'] = min(100, new_state['health'] + 25)

    if can_take_action:
        if current_state['direction'] == 'C':
            if action == 'me':
                if np.random.uniform(0, 1) <= 0.85:
                    new_state['direction'] = 'E'
                else:
                    new_state['direction'] = 'E'
            if action == 'ms':
                if np.random.uniform(0, 1) <= 0.85:
                    new_state['direction'] = 'S'
                else:
                    new_state['direction'] = 'E'
            if action == 'mn':
                if np.random.uniform(0, 1) <= 0.85:
                    new_state['direction'] = 'N'
                else:
                    new_state['direction'] = 'E'
            if action == 'mw':
                if np.random.uniform(0, 1) <= 0.85:
                    new_state['direction'] = 'W'
                else:
                    new_state['direction'] = 'E'
            if action == 'stay':
                if np.random.uniform(0, 1) <= 0.85:
                    new_state['direction'] = 'C'
                else:
                    new_state['direction'] = 'E'
            if action == 'sb':
                if np.random.uniform(0, 1) <= 0.1:
                    new_state['health'] = max(0, new_state['health'] - 50)
            if action == 'sa':
                new_state['arrow'] = current_state['arrow'] - 1
                if np.random.uniform(0, 1) <= 0.9:
                    new_state['health'] = current_state['health'] - 25
        if current_state['direction'] == 'E':
            if action == 'stay':
                new_state['direction'] = 'E'
            if action == 'mc':
                new_state['direction'] = 'C'
            if action =='sb':
                if np.random.uniform(0, 1) <= 0.2:
                    new_state['health'] = max(0, current_state['health'] - 50)
            if action == 'sa':
                new_state['arrow'] = current_state['arrow'] - 1
                if np.random.uniform(0, 1) <= 0.9:
                    new_state['health'] = current_state['health'] - 25
        if current_state['direction'] == 'N':
            if action == 'mc':
                if np.random.uniform(0, 1) <= 0.85:
                    new_state['direction'] = 'C'
                else:
                    new_state['direction'] = 'E'
            if action == 'stay':
                if np.random.uniform(0, 1) <= 0.85:
                    new_state['direction'] = 'N'
                else:
                    new_state['direction'] = 'E'
            if action == 'um':
                prob = np.random.uniform(0, 1)
                if prob <= 0.15:
                    new_state['arrow'] = min(3, new_state['arrow'] + 3)
                elif prob <= 0.35:
                    new_state['arrow'] = min(3, new_state['arrow'] + 2)
                elif prob <= 0.5:
                    new_state['arrow'] = min(3, new_state['arrow'] + 1)
        if current_state['direction'] == 'S':
            if action == 'mc':
                if np.random.uniform(0, 1) <= 0.85:
                    new_state['direction'] = 'C'
                else:
                    new_state['direction'] = 'E'
            if action == 'stay':
                if np.random.uniform(0, 1) <= 0.85:
                    new_state['direction'] = 'S'
                else:
                    new_state['direction'] = 'E'
            if action == 'gm':
                if np.random.uniform(0, 1) <= 0.75:
                    new_state['material'] = min(2, new_state['material'] + 2)
        if current_state['direction'] == 'W':
            if action == 'mc':
                new_state['direction'] = 'C'
            if action == 'stay':
                new_state['direction'] = 'W'
            if action == 'sa':
                new_state['arrow'] = max(0, new_state['arrow'] - 1)
                if np.random.uniform(0, 1) <= 0.25:
                    new_state['health'] = max(0, new_state['health'] - 25)
    # print('(in get_next_state): ', new_state)
    new_state = get_state_from_diction(new_state, states)
    return new_state.copy()


f = open('utilities.json',)

# returns JSON object as 
# a dictionary
utilities = json.load(f)


f = open('transition.json', )
transition = json.load(f)

move_success = {
    'C': 0.85,
    'N': 0.85,
    'S': 0.85,
    'E': 1,
    'W': 1
}
sb_success = {
    'C': 0.1,
    'N': 0,
    'S': 0,
    'E': 0.2,
    'W': 0
}
sa_success = {
    'C': 0.5,
    'N': 0,
    'S': 0,
    'E': 0.9,
    'W': 0.25
}
um_success = {
    '1': 0.5,
    '2': 0.35,
    '3': 0.15
}
land_site = {
    'mn': 'N',
    'me': 'E',
    'ms': 'S',
    'mw': 'W',
    'mc': 'C'
}
gm_success = 0.75
max_materials = 2
max_arrows = 3

states = create_states()
current_state = {"direction": "W", "material": 0, "arrow": 0, "state": 'd', "health": 100}
current_state = get_state_from_diction(current_state, states)

while True:
    if current_state["health"] == 0:
        break

    best_action = ''
    max_utility = -1e20

    for action in action_set[current_state['direction']]:
        # print('-----------')
        # print('action = ', action)
        s_dash_possibles, s_dash_probabilities = get_next_state_values(current_state, action, transition)
        next_utility = 0
        state_rewards = 0
        if len(s_dash_possibles) == 0 and current_state["health"] != 0 :
            continue
        for s_dash, s_prob in zip(s_dash_possibles, s_dash_probabilities):
            next_utility += s_prob * (utilities[s_dash["index"]])
            state_rewards += s_prob * rewards(current_state, s_dash)
            # print(s_dash, s_prob)
        if next_utility + state_rewards > max_utility:
            max_utility = next_utility + state_rewards
            best_action = action
    new_state = get_next_state(current_state, best_action, states)
    print('Current state:', current_state)
    print('Best action:', best_action)
    print('Next state:', new_state)
    print('-----------')

    current_state = new_state.copy()


  
# Closing file
f.close()