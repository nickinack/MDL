# Perform Value Iteration for the given assignment
import numpy as np
import json
# Task 1: Create States
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

def actions():
    '''
    Define a set of all possible actions for different states 
    '''
    action_set = []
    direction = ['C', 'N', 'S', 'E', 'W']
    # m+suffix = move + dir, s+suffix = shoot + blade/arrow, prefix+m = material use/gather, stay
    actions = ['mc', 'me', 'ms', 'mn', 'mw', 'sb', 'sa', 'gm', 'um' , 'stay']
    # for each of the directions, define prospective states
    action_set = {
        'C': ['me', 'ms', 'mn', 'mw', 'sb', 'sa', 'stay'],
        'N': ['mc', 'um', 'stay'],
        'S': ['mc', 'gm', 'stay'],
        'W': ['mc', 'sa', 'stay'],
        'E': ['mc', 'sb', 'sa', 'stay']
    }
    
    return action_set


def get_state_from_attribs(direction, material, arrow, MM_state, health, states):
    for state in states_copy:
        if state["direction"] == direction and state["material"] == material and state["arrow"] == arrow and state["state"] == MM_state and state["health"] == health:
            return state


def get_state_from_diction(diction, states):
    # print('---------')
    for state in states_copy:
        # if state["direction"] == diction["direction"] and state["material"] == diction["material"]:
        #     print("found, ", state)
        if state["direction"] == diction["direction"] and state["material"] == diction["material"] and state["arrow"] == diction["arrow"] and state["state"] == diction["state"] and state["health"] == diction["health"]:
            return state.copy()




# Confirm if each entry should be dict or 
def transition_function(states , actions):
    '''
    Given an list of state and actions, define a transition table
    '''

    # Define the success probabilities for various actions
    transition_table = []
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


    for i in range(len(states)):
        cur_state = states[i].copy()
        # Iterate through the actions
        # Depending on the current state, chose the action set which is iterable

        if cur_state['health'] == 0:
            continue
    
        for j in range(0 , len(actions[cur_state["direction"]])):
        
            # move 
            flag = 0  # 1 == dormant state
            mult_factor = 1
            if cur_state["state"] == "r" and (cur_state["direction"] == "C" or cur_state["direction"] == "E"):  # 0.5 chance MM attacks then goes into 'd'
                if actions[cur_state["direction"]][j] == "sa" and cur_state["arrow"] == 0:
                    continue
                mult_factor = 0.5
                next_state =  {"direction": cur_state["direction"], "material": cur_state["material"], "arrow": 0, "state": 'd', "health": min(100, cur_state["health"]+25)}
                next_state = get_state_from_diction(next_state, states)
                transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": mult_factor, "next_state": next_state})
            
            if cur_state["state"] == "r" and (cur_state["direction"] == "W" or cur_state["direction"] == "N" or cur_state["direction"] == "S"):
                flag = 2
                mult_factor = 0.5

            if cur_state["state"] == "d":
                flag = 1
            if actions[cur_state["direction"]][j] == 'me' or actions[cur_state["direction"]][j] == "mn" or actions[cur_state["direction"]][j] == "ms" or actions[cur_state["direction"]][j] == "mc" or actions[cur_state["direction"]][j] == "mw":
                # Handle success
                next_state =  {"direction": land_site[actions[cur_state["direction"]][j]], "material": cur_state["material"], "arrow": cur_state["arrow"], "state": cur_state["state"], "health": cur_state["health"]}
                next_state = get_state_from_diction(next_state, states)
                if flag == 1:
                    prob = mult_factor*move_success[cur_state["direction"]]*0.8
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    prob = mult_factor*move_success[cur_state["direction"]]*0.2
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'r'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                if flag == 0:
                    prob = mult_factor*move_success[cur_state["direction"]]
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                if flag == 2:
                    prob = mult_factor*move_success[cur_state["direction"]]
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'd'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})

                # Handle failure
                prob = mult_factor*(1-move_success[cur_state["direction"]])
                if prob <= 0:
                    continue
                next_state = cur_state.copy()
                next_state["direction"] = "E"
                next_state = get_state_from_diction(next_state, states)
                # transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                if flag == 1:
                    prob = mult_factor*(1-move_success[cur_state["direction"]])*0.8
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    prob = mult_factor*(1-move_success[cur_state["direction"]])*0.2
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'r'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                if flag == 0:
                    prob = mult_factor*(1-move_success[cur_state["direction"]])
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                if flag == 2:
                    prob = mult_factor*(1-move_success[cur_state["direction"]])
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'd'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})

            # shoot bullet
            elif actions[cur_state["direction"]][j] == "sb":
                # Handle success
                prob = sb_success[cur_state["direction"]]
                if prob == 0 or cur_state["health"] == 0:
                    continue
                next_state = cur_state.copy()
                next_state["health"] = max(0, cur_state["health"]-50)
                next_state = get_state_from_diction(next_state, states)
                if flag == 1:
                    prob = mult_factor*sb_success[cur_state["direction"]]*0.8
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    prob = mult_factor*sb_success[cur_state["direction"]]*0.2
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'r'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                if flag == 0:
                    prob = mult_factor*sb_success[cur_state["direction"]]
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                if flag == 2:
                    prob = mult_factor*sb_success[cur_state["direction"]]
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'd'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                # Handle failure
                if flag == 1:
                    prob = mult_factor*(1-sb_success[cur_state["direction"]])*0.8
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": cur_state})
                    prob = mult_factor*(1-sb_success[cur_state["direction"]])*0.2
                    next_state1 = cur_state.copy()
                    next_state1["state"] = 'r'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                if flag == 0:
                    prob = mult_factor*(1-sb_success[cur_state["direction"]])
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": cur_state})
                if flag == 2:
                    prob = mult_factor*(1-sb_success[cur_state["direction"]])
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": cur_state})
                    next_state1 = cur_state.copy()
                    next_state1["state"] = 'd'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
            
            # shoot arrows 
            elif actions[cur_state["direction"]][j] == "sa":
                # Handle success
                if cur_state["arrow"] == 0 or sa_success[cur_state["direction"]] == 0 or cur_state["health"] == 0:
                    continue
                next_state = cur_state.copy()
                next_state["arrow"] = cur_state["arrow"]-1
                next_state["health"] = max(0, cur_state["health"]-25)
                next_state = get_state_from_diction(next_state, states)
                prob = mult_factor*sa_success[cur_state["direction"]]
                if flag == 1:
                    prob = mult_factor*sa_success[cur_state["direction"]]*0.8
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    prob = mult_factor*sa_success[cur_state["direction"]]*0.2
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'r'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                if flag == 0:
                    prob = mult_factor*sa_success[cur_state["direction"]]
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                if flag == 2:
                    prob = mult_factor*sa_success[cur_state["direction"]]
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'd'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                # Handle failure
                next_state = cur_state.copy()
                next_state["arrow"] -= 1
                next_state = get_state_from_diction(next_state, states)
                prob = mult_factor*(1-sa_success[cur_state["direction"]])
                if flag == 1:
                    prob = mult_factor*(1-sa_success[cur_state["direction"]])*0.8
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    prob = mult_factor*(1-sa_success[cur_state["direction"]])*0.2
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'r'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                if flag == 0:
                    prob = mult_factor*(1-sa_success[cur_state["direction"]])
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                if flag == 2:
                    prob = mult_factor*(1-sa_success[cur_state["direction"]])
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'd'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})

            # use material
            elif actions[cur_state["direction"]][j] == "um":
                # Handle success
                next_state = cur_state.copy()
                if cur_state["material"] >= 1:
                    next_state["material"] = next_state["material"]-1
                    # print("next_state: ", next_state)
                    next_state = get_state_from_diction(next_state, states)
                    # print("after get_state_from", next_state)
                    if flag == 1:
                        prob = mult_factor*um_success['1']*0.8
                        next_state["arrow"] = min(cur_state["arrow"]+1 , max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                        prob = mult_factor*um_success['2']*0.8
                        next_state["arrow"] = min(cur_state["arrow"]+2 , max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                        prob = mult_factor*um_success['3']*0.8
                        next_state["arrow"] = min(cur_state["arrow"]+3, max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                        
                        next_state1 = next_state.copy()
                        next_state1["state"] = 'r'
                        prob = mult_factor*um_success['1']*0.2
                        next_state1["arrow"] = min(cur_state["arrow"]+1 , max_arrows)
                        next_state1 = get_state_from_diction(next_state1, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                        prob = mult_factor*um_success['2']*0.2
                        next_state1["arrow"] = min(cur_state["arrow"]+2 , max_arrows)
                        next_state1 = get_state_from_diction(next_state1, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                        prob = mult_factor*um_success['3']*0.2
                        next_state1["arrow"] = min(cur_state["arrow"]+3, max_arrows)
                        next_state1 = get_state_from_diction(next_state1, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                    if flag == 0:
                        prob = mult_factor*um_success['1']
                        next_state["arrow"] = min(cur_state["arrow"]+1 , max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                        prob = mult_factor*um_success['2']
                        next_state["arrow"] = min(cur_state["arrow"]+2 , max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                        prob = mult_factor*um_success['3']
                        next_state["arrow"] = min(cur_state["arrow"]+3, max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    if flag == 2:
                        prob = mult_factor*um_success['1']
                        next_state["arrow"] = min(cur_state["arrow"]+1 , max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                        prob = mult_factor*um_success['2']
                        next_state["arrow"] = min(cur_state["arrow"]+2 , max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                        prob = mult_factor*um_success['3']
                        next_state["arrow"] = min(cur_state["arrow"]+3 , max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})

                        next_state["state"] = 'd'
                        next_state = get_state_from_diction(next_state, states)

                        prob = mult_factor*um_success['1']
                        next_state["arrow"] = min(cur_state["arrow"]+1 , max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                        prob = mult_factor*um_success['2']
                        next_state["arrow"] = min(cur_state["arrow"]+2 , max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                        prob = mult_factor*um_success['3']
                        next_state["arrow"] = min(cur_state["arrow"]+3 , max_arrows)
                        next_state = get_state_from_diction(next_state, states)
                        transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})

            # gather material
            elif actions[cur_state["direction"]][j] == "gm":
                # Handle success
                next_state = cur_state.copy()
                next_state["material"] = min(cur_state["material"]+1 , max_materials)
                next_state = get_state_from_diction(next_state, states)
                if flag == 1:
                    prob = mult_factor*0.75*0.8
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    prob = mult_factor*0.75*0.2
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'r'
                    next_state1 = get_state_from_diction(next_state1, states)

                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                if flag == 0:
                    prob = mult_factor*0.75
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                if flag == 2:
                    prob = mult_factor*0.75
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'd'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                # Handle failure
                if flag == 1:
                    prob = mult_factor*0.25*0.8
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": cur_state})
                    prob = mult_factor*0.25*0.2
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'r'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                if flag == 0:
                    prob = mult_factor*0.25
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": cur_state})
                if flag == 2:
                    prob = mult_factor*0.25
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": cur_state})
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'd'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})

            # stay
            elif actions[cur_state["direction"]][j] == "stay":
                # Handle success
                next_state = cur_state.copy()
                if flag == 1:
                    prob = mult_factor*move_success[cur_state["direction"]]*0.8
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    prob = mult_factor*move_success[cur_state["direction"]]*0.2
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'r'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                if flag == 0:
                    prob = mult_factor*move_success[cur_state["direction"]]
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                if flag == 2:
                    prob = mult_factor*move_success[cur_state["direction"]]
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'd'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                # transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                # Handle failure
                next_state = cur_state.copy()
                next_state["direction"] = "E"
                next_state = get_state_from_diction(next_state, states)
                prob = (1-move_success[cur_state["direction"]])
                if prob == 0:
                    continue
                if flag == 1:
                    prob = mult_factor*(1-move_success[cur_state["direction"]])*0.8
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    prob = mult_factor*(1-move_success[cur_state["direction"]])*0.2
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'r'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                if flag == 0:
                    prob = mult_factor*(1-move_success[cur_state["direction"]])
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                if flag == 2:
                    prob = mult_factor*(1-move_success[cur_state["direction"]])
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                    next_state1 = next_state.copy()
                    next_state1["state"] = 'd'
                    next_state1 = get_state_from_diction(next_state1, states)
                    transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state1})
                
    # Transition between ready and dormant state
    '''
    for i in range(0 , len(states)):
        cur_state = states[i]
        for i in range(0 , len(actions[cur_state["direction"]])):
            if cur_state["state"] == 'd':
                prob = 0.2
                next_state = cur_state
                next_state["state"] = 'r'
                transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                prob = 0.8
                transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": cur_state})
            
            if cur_state["state"] == 'r':
                prob = 0.5
                next_state = cur_state
                next_state["state"] = 'd'
                transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": next_state})
                prob = 0.5
                transition_table.append({"cur_state": cur_state, "action": actions[cur_state["direction"]][j], "prob": prob, "next_state": cur_state})
    '''
    return transition_table




def probability(cur_state, next_state, action, transition_table):
    for entry in transition_table:
        if entry['cur_state'] == cur_state and entry['next_state'] == next_state and entry['action'] == action:
            return entry['prob']
    return 0


def rewards(state, next_state, action):
    factor = 0
    if action == "stay":
        factor = 10
    if state["state"] == "r" and next_state["state"] == "d" and state["direction"] in ['C', 'E']:
        return -50+factor
    if state["health"] != 0 and next_state["health"] == 0:
        return 40+factor
    return -10+factor


def get_next_states(cur_state, action, transition_table):
    possible_next_states = []
    for entry in transition_table:
        if entry['cur_state'] == cur_state and entry['action'] == action:
            possible_next_states.append(entry['next_state'])
    return possible_next_states

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



def convert_action_from_state(state, action):
    if action == 'sb':
        return 'HIT'
    if action == 'sa':
        return 'SHOOT'
    if action == 'gm':
        return 'GATHER'
    if action == 'um':
        return 'CRAFT'
    if state['direction'] == 'C':
        if action == 'mn':
            return 'UP'
        if action == 'ms':
            return 'DOWN'
        if action == 'mw':
            return 'LEFT'
        if action == 'me':
            return 'RIGHT'
    if state['direction'] == 'W':
        if action == 'mc':
            return 'RIGHT'
    if state['direction'] == 'E':
        if action == 'mc':
            return 'LEFT'
    if state['direction'] == 'N':
        if action == 'mc':
            return 'DOWN'
    if state['direction'] == 'S':
        if action == 'mc':
            return 'UP'
    return action.upper()





def value_iteration(states, action_set, transition_table, gamma, epsilon):
    utilities = [0] * len(states)
    utilities_dash = [0] * len(states)

    for state in states:
        utilities[state['index']] = 0
        utilities_dash[state['index']] = 0
    
    state_to_check = {"direction": 'C', "material": 2, "arrow": 3, "state": 'r', "health": 50}
    state_to_check = get_state_from_diction(state_to_check, states)
    
    delta = -1e3
    start = True
    iter_no = 0
    # while start or delta >= (epsilon * (1 - gamma)) / gamma:
    while start or delta >= epsilon:
        # print('iter delta:') 
        # print(delta)
        start = False

        print("iteration=", iter_no)
        iter_no += 1
        
        utilities = utilities_dash.copy()
        delta = 0

        # print('--------')
        for i in range(len(states)):
            state = states[i]
            # if state == state_to_check:
            #     print('checking')
            max_next_utility = -1e30
            best_action = 'NONE'
            for action in action_set[state["direction"]]:
                s_dash_possibles, s_dash_probabilities = get_next_state_values(state, action, transition_table)
                if len(s_dash_possibles) == 0 and state["health"] != 0 :
                    continue
                elif len(s_dash_possibles) == 0 and state["health"] == 0:
                    utilities[state["index"]] = 0
                    max_next_utility = max(max_next_utility, 0)
                    continue
                next_utility = 0
                state_rewards = 0
                for s_dash, s_prob in zip(s_dash_possibles, s_dash_probabilities):
                    # if action == 'ms' and state == state_to_check:
                    #     print('    s_dash', s_dash)
                    #     print('      s_prob', s_prob)
                    #     print('      utils_', utilities[s_dash["index"]])
                    #     print('      reward', rewards(state, s_dash))
                    # next_utility += probability(state, s_dash, action, transition_table) * (utilities[s_dash["index"]] + rewards(state, s_dash))
                    next_utility += gamma * s_prob * (utilities[s_dash["index"]])
                    state_rewards += s_prob * rewards(state, s_dash, action)
                if next_utility + state_rewards > max_next_utility:
                    max_next_utility = next_utility + state_rewards
                    best_action = action
                # if action == 'ms' and state == state_to_check:
                #     print('next_util, state_rewards:', next_utility, state_rewards)
                #     print('action ms has util', next_utility + state_rewards)
                #     print('------------')
            utilities_dash[state["index"]] = max_next_utility

            print(f"({state['direction']},{state['material']},{state['arrow']},{state['state'].upper()},{state['health']}):{convert_action_from_state(state,best_action)}=[{max_next_utility:.3f}]")

            # print(utilities_dash[state["index"]], utilities[state["index"]], delta,  (epsilon * (1 - gamma)) / gamma)
            if abs(utilities_dash[state["index"]] - utilities[state["index"]]) > delta:
                # print("max diff: ", state)
                delta = abs(utilities_dash[state["index"]] - utilities[state["index"]])

        # print(utilities)
        # print('--')
        # print(utilities_dash)
    return utilities


def get_state_by_index(states, index):
    for state in states:
        if state["index"] == index:
            diction = state.copy()
            return diction

states = create_states()
states_copy = states.copy()
# print(states)  # {'direction': 'N', 'material': 0, 'arrow': 3, 'state': 'r', 'health': 0, 'index': 195}
actions = actions()
transition = transition_function(states , actions)
# print(actions)
utilities = value_iteration(states, actions, transition, 0.999, 1e-3)
with open('utilities.json', 'w', encoding='utf-8') as f:
   json.dump(utilities, f, ensure_ascii=False, indent=4)

# state = {'direction': 'E', 'material': 0, 'arrow': 1, 'state': 'd', 'health': 100}
# state = get_state_from_diction(state , states)
# flag = 1
# time = 0
# while flag == 1:
#     if state["health"] == 0:
#         print("Done!")
#         break
#     next_utility = -1e30
#     next_state = ''
#     best_act = ''
#     #print('cur state: ', state)
#     for action in actions[state["direction"]]:
#         # print('action:', action)
#         s_dash_possibles = get_next_states(state, action, transition)
#         # print(state , action)
#         # print('s_dashpossibles:', s_dash_possibles)
#         for s_dash in s_dash_possibles:
#             # print('sdash: ', s_dash)
#             # print('    util: ', utilities[s_dash['index']])
#             cur_utility =  probability(state, s_dash, action, transition) * (utilities[s_dash["index"]] + rewards(state, s_dash))
#             if next_utility < cur_utility and ((state["state"] == s_dash["state"])):
#                 next_utility = cur_utility
#                 next_state = s_dash
#                 best_act = action
#     print('after time step:')
#     print(state)
#     print(best_act)
#     print(next_state)
#     print("-----------------------------")
#     time += 1
#     if time >= 10:
#         break
#     state = next_state



# for entry in transition:
#     # E, 1, 0, r, 25
#     if entry["cur_state"]["direction"] == 'E' and entry["cur_state"]["arrow"] == 0 and entry["cur_state"]["material"] == 0 and entry["cur_state"]["state"] == 'r':
#         print(entry)


# for state in states:
#     for action_list in actions.values():
#         # print(action_list)
#         for action in action_list:
#             next_states = get_next_states(state, action, transition)
#             # print(next_states)
#             prob = 0
#             for next_state in next_states:
#                 prob += probability(state, next_state, action, transition)
#             print(prob, state, action)


# dic = {'direction': 'C', 'material': 1, 'arrow': 2, 'state': 'd', 'health': 50}
# st = get_state_from_diction(dic, states)
# print(st)
# print(actions)
# for action in actions['C']:
#     next_states = get_next_states(st, action, transition)
#     # print('============')
#     # print('action: ', action)
#     prob = 0
#     for c in next_states:
#         val = probability(st, c, action, transition)
#         prob += val
#         # print('for state', c)
#         # print('prob:', val)
#     print('sum of action:', prob)
#     # print(next_states)


# for state in states:
#     for action in actions[state['direction']]:
#         next_states, probs = get_next_state_values(state, action, transition)
#         prob = sum(probs)
#         print('action:', action)
#         print('prob', prob)

#         if abs(1 - prob) >= 0.001 and prob != 0:
#             print('boo')
#             quit()


# for entry in transition:
#     print(entry)