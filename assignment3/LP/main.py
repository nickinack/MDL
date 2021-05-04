# Perform Value Iteration for the given assignment
import numpy as np
import json
import cvxpy as cp
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
    return action


def probability(cur_state, next_state, action, transition_table):
    for entry in transition_table:
        if entry['cur_state'] == cur_state and entry['next_state'] == next_state and entry['action'] == action:
            return entry['prob']
    return 0


def rewards(state, next_state):
    if state["state"] == "r" and next_state["state"] == "d" and state["direction"] in ['C', 'E']:
        return -50
    return -10


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

def get_state_by_index(states, index):
    for state in states:
        if state["index"] == index:
            diction = state.copy()
            return diction

def state_action_pair(states , actions):
    '''
    Given a state and an action, creates a state action pair and indexes them
    '''
    pairs = []
    cnt = 0
    for i in range(0 , len(states)):
        cur_state = states[i]
        if cur_state["health"] == 0:
            pairs.append({"state": cur_state, "action": "none", "index": cnt})
            cnt = cnt+1
            continue
        for j in range(0 , len(actions[cur_state["direction"]])):
            if cur_state["arrow"] == 0 and actions[cur_state["direction"]][j] == "sa":
                continue
            
            if cur_state["material"] == 0 and actions[cur_state['direction']][j] == 'um':
                continue
            
            pairs.append({"state": cur_state, "action": actions[cur_state["direction"]][j], "index": cnt})                
            cnt = cnt+1
    return np.array(pairs)


def make_r(state_action_pair, transition_table):
    '''
    R-vector
    '''
    r_vector = np.array([0] * len(state_action_pair))
    for entry in state_action_pair:
        cur_state = entry['state']
        action = entry['action']
        weighted_reward = 0
        s_dash_possibles, s_dash_probabilities = get_next_state_values(cur_state, action, transition_table)
        for s_dash, prob in zip(s_dash_possibles, s_dash_probabilities):
            #if cur_state == s_dash:
            #    continue
            weighted_reward += prob * rewards(cur_state, s_dash)
        r_vector[entry['index']] = weighted_reward
    return r_vector


def make_a(state_action_pair , states, transition_table):
    '''
    A-Matrix
    '''
    a = np.zeros((len(states), len(state_action_pair)))
    for i in range(0 , len(state_action_pair)):   
        cur_state = state_action_pair[i]['state']
        action = state_action_pair[i]['action']
        action_index = state_action_pair[i]['index']
        if action == 'none':
            a[cur_state["index"]][action_index] = 1
            continue
        possible_next_states, s_dash_probabilities = get_next_state_values(cur_state, action, transition_table)
        for state, prob in zip(possible_next_states, s_dash_probabilities):
            if state == cur_state:
                continue
            a[cur_state["index"]][action_index] += prob
            a[state["index"]][action_index] -= prob
    return a
    

def get_action_index(state , action, state_action_pair):
    '''
    Get index
    '''

    for i in range(0 , len(state_action_pair)):
        if state == state_action_pair["state"] and action == state_action_pair["action"]:
            return i
    return -1


def get_state_from_diction(diction, states):
    # print('---------')
    for state in states:
        # if state["direction"] == diction["direction"] and state["material"] == diction["material"]:
        #     print("found, ", state)
        if state["direction"] == diction["direction"] and state["material"] == diction["material"] and state["arrow"] == diction["arrow"] and state["state"] == diction["state"] and state["health"] == diction["health"]:
            return state.copy()

def make_alpha(states):
    '''
    return alpha
    '''
    alpha = [0] * len(states)
    start_state = {'direction': 'C', 'material': 2, 'arrow': 3, 'state': 'r', 'health': 100}
    start_state = get_state_from_diction(start_state, states)
    alpha[start_state['index']] = 1
    return alpha
    # for i in range(0 , len(state)):
    #     alpha.append(1/len(stat))


# def lp(transition, states, actions):


states = create_states()
actions_set = actions()
transition_table = transition_function(states , actions_set)
sap = state_action_pair(states , actions_set)
r = np.array(make_r(sap , transition_table)).reshape(-1, 1)

x = cp.Variable(shape=(len(sap),), name="x")
A = np.array(make_a(sap , states , transition_table))
alpha = make_alpha(states)
constraints = [cp.matmul(A, x) == alpha, x>=0]
objective = cp.Maximize(cp.matmul(x.T , r))
problem = cp.Problem(objective, constraints)

solution = problem.solve()


def get_entries_from_state(cur_state, sap):
    to_return = []
    for entry in sap:
        if entry['state'] == cur_state:
            to_return.append(entry)
    return to_return

print(solution)

policy = []

for state in states:
    sap_entries = get_entries_from_state(state, sap)
    max_action_value = -200000
    best_action = ''
    # if state['arrow'] == 0:
    #     print('state:', state)
    for entry in sap_entries:
        # if state['arrow'] == 0:
        #     print('   action:', entry['action'], x[entry['index']].value)
        if x[entry['index']].value > max_action_value:
            max_action_value = x[entry['index']].value
            best_action = entry['action']
    # print(f"({state['direction']}, {state['material']}, {state['arrow']}, {state['state']}, {state['health']}):{best_action}<{max_action_value}>")
    # print(f"({state['direction']},{state['material']},{state['arrow']},{state['state']},{state['health']}):{convert_action_from_state(state,best_action).upper()}")
    policy.append([ (state['direction'], state['material'], state['arrow'], state['state'].upper(), state['health']), convert_action_from_state(state,best_action).upper() ])
# for i in range(0 , len(sap)):
#     print(x[i].value)
# print(x.shape)


# print(x[0].values)

output_result_dict = {
    "a": A.tolist(),
    "r": r.reshape(-1,).tolist(),
    "alpha": alpha,
    "x": list(map(lambda v: v.value, x)),
    "objective": solution,
    "policy": policy
}

with open('part_3_output.json', 'w', encoding='utf-8') as f:
   json.dump(output_result_dict, f, ensure_ascii=False)