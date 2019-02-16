
import argparse

class DFA:
    def __init__(self, alphabet, initial_state, final_states, transitions, states, labels, actions):
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions
        self.states = states
        self.labels = labels
        self.actions = actions


def read_dfa_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
        states = lines[0].split(',')
        states = [state.strip() for state in states]
        alphabet = lines[1].split(',')
        if ' ' in alphabet:
            alphabet.remove(' ')
        alphabet = [char.strip() for char in alphabet]
        initial_state = lines[2].strip()
        final_states = [state.strip() for state in lines[3].split(',')]
        transitions = list()
        for transition_tuple in lines[4].replace(" ","").replace("),(", "|").replace("(", "").replace(")","").split("|"):
            splitted_tuple = [element.strip() if element != '' else ' ' for element in transition_tuple.split(",")]
            transition = {
                'arc_from': splitted_tuple[0],
                'arc_condition': splitted_tuple[1],
                'arc_to': splitted_tuple[2]
            }
            transitions.append(transition)

        labels = dict()

        for label_tuple in lines[5].replace(' ', '').replace('\n','').replace("),(", "MYNAMEISMENIAWYSTOPLOOKINGATMYCODE").replace("(", "").replace(")","").split("MYNAMEISMENIAWYSTOPLOOKINGATMYCODE"):
            splitted_tuple = [element for element in label_tuple.split(",")]
            labels[splitted_tuple[0]] = splitted_tuple[1]

        actions = dict()
        for action_tuple in lines[6].replace(' ', '').replace('\n','').replace("),(", "MYNAMEISMENIAWYSTOPLOOKINGATMYCODE").replace("(", "").replace(")","").split("MYNAMEISMENIAWYSTOPLOOKINGATMYCODE"):
            splitted_tuple = [element for element in action_tuple.split(",")]
            actions[splitted_tuple[0]] = splitted_tuple[1]


        return DFA(alphabet, initial_state, final_states, transitions, states, labels, actions)


def check_string(dfa, string):
    res = ''
    l = r = 0
    latest_accept_idx = -1
    latest_accept_state = -1
    
    while(True):
        if l >= len(string):
            break

        latest_accept_idx = -1
        latest_accept_state = -1
        current_state = dfa.initial_state
        for idx in range(l, len(string)):
            for transition in dfa.transitions:
                if string[idx] == transition['arc_condition'] and current_state == transition['arc_from']:
                    current_state = transition['arc_to']
                    if transition['arc_to'] in dfa.final_states:
                        latest_accept_idx = idx
                        latest_accept_state = transition['arc_to']
                    break

        if latest_accept_idx == -1:
            res = string + ', ' + dfa.actions[dfa.labels['DEAD']]
            break
        else:
            chunk = string[l:latest_accept_idx + 1]
            res = res + chunk + ', ' + dfa.actions[dfa.labels[latest_accept_state]] + '\n'
            l = latest_accept_idx + 1

    return res





if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--dfa-file', action="store", help="path of file to take as input to construct DFA", nargs="?", metavar="dfa_file")
    parser.add_argument('--input-file', action="store", help="path of file to take as input to test strings in on DFA", nargs="?", metavar="input_file")
    
    args = parser.parse_args()

    loaded_dfa = read_dfa_from_file(args.dfa_file)

    output_file = open('task_3_1_result.txt', 'w+')

    with open(args.input_file, "r") as file:
        for string in file.readlines():
            res = check_string(loaded_dfa, string.strip())
            print(res)
            output_file.write(res)
