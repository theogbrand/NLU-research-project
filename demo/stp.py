#!/usr/bin/env python
# coding: utf-8

# ## Sentence to Predicate (STP) Converter
# 
# 

# In[1]:


# Step 1: Tokenize words
# Step 2: find subject (first noun/prp), verb, object (first noun after subject), goal-state (PP)
# these will be arg1-4
# Step 3: check if goal state is atomic, if not, process it 
# Step 4: check whether has noun predicate, if have process it
# Step 5: output noun + verb predicate


# In[2]:


import nltk
from nltk import word_tokenize

# download StanfordCoreNLP latest version from website and put it in same package as this file
from stanfordcorenlp import StanfordCoreNLP


# In[3]:


# Types of Instructions to Process

# Testing spatio predicates
s1 = "move the ball to the right of the box"
s2 = "move the ball to beside the box"
s3 = "move the ball above the box"

# Testing verb predicates
s4 = "align the robot claw to the ball"
s5 = "lift the ball"
s6 = "carry the ball to the box"
s7 = "pick up the diamond on the blue"


# In[4]:


# for debugging nltk parser
tk = nltk.pos_tag(word_tokenize(s7))
# print(tk)


# In[5]:


def get_parse_tree(sentence):
    nlp = StanfordCoreNLP('stanford-corenlp-4.2.2/', lang='en', memory='8g')
    
    parse_tree = nlp.parse(sentence)
    return parse_tree


# In[6]:


# print(get_parse_tree("put down the ball"))
# print(get_parse_tree("put the ball down"))

# system needs to do the same thing


# In[7]:


sentences = [s1, s2, s3, s4, s5, s6]

import re

# Step 1: Parser
for s in sentences:
    tree = get_parse_tree(s)
#     print(tree)
    
#     elem_list = tree.split("\n")
    elem_list = tree.split("\n")
#     print(elem_list)
    
    for e in elem_list:
        e = e.strip()
#         print(e)

    
#     print()


# In[8]:


##  get the goal
# p7 = """
# (ROOT
#   (S
#     (VP (VB pick)
#       (NP (DT the) (NN ball))
#       (PRT (RP up)))))
#       """

# p8 = """
# (ROOT
#   (S
#     (VP (VB pick)
#       (PRT (RP up))
#       (NP (DT the) (NN ball)))))
#       """
s7 = """
(ROOT
  (S
    (VP (VB put)
      (NP (DT the) (NN diamond))
      (PP (IN to)
        (NP
          (NP (DT the) (NN front))
          (PP (IN of)
            (NP (DT the) (JJ blue) (NN box))))))))"""

def get_goal(parsed_text):
    # split by first occurance of PP
    if "PP" in parsed_text:
        goal = parsed_text.split('PP', 1)[1]
    elif "PRT" in parsed_text:
        goal = parsed_text.split('PRT', 1)[1]
    else:
        goal = None
    return goal

# print(get_goal(s7))


# In[9]:


# 2: extract feature from parser before passing to function
def extract_feature(token):
    output = ''
    output_index = 0
    if token == None:
        return None
    for c in token:
        if c.islower() or c.isdigit():
            output += c
            output_index += 1
        elif c == ')':
            if output[output_index-1] != " ":
                output += ' '
                output_index += 1
    return output.strip()

# after split('\n') is called
# print(extract_feature(get_goal(s7)))


# In[10]:


# Attempt to put together goal state from NLTK
def get_goal_index(goal, sentence):
    start_index = sentence.find(goal)
    first_half = sentence[:start_index]
  
    first_half_length = len(first_half.split(" "))
    goal_length = len(goal.split(" ")) 

    goal_index = []
    starting_index = first_half_length - 1
    for i in range(0, goal_length):
        goal_index.append(starting_index)
        starting_index += 1
  
    return goal_index

# print(s1)
# print(get_goal_index('front the blue box', "put the ball to the front of the blule box"))


# In[11]:


# print(nltk.pos_tag(word_tokenize("Pick up the ball")))
# print(nltk.pos_tag(word_tokenize("Put the ball")))
# print(nltk.pos_tag(word_tokenize("Place the ball on the")))
# print(nltk.pos_tag(word_tokenize("put the ball to the right of the blule box")))


# In[14]:


def process_goal(extracted_feature):
    front = "to the front of"
    back = "to the back of"
    if front in extracted_feature: 
        extracted_feature = extracted_feature.replace(front, "front")
    if back in extracted_feature: 
        extracted_feature = extracted_feature.replace(back, "back")
    return extracted_feature
#     print(sentence)
    
# print(process_goal("to the front of the blue box"))


# In[15]:


# intermediate function to segment all features in sentence to 
# Subject (if contained), Object, Verb, Goal State

def get_feature_dict(sentence):
#     required because Pick up and pick up will return different pos_tag
# see example above
    sentence = sentence.lower()
    ls = nltk.pos_tag(word_tokenize(sentence))
    
    dict_keywords_position = {}
    
#     go through all token pairs and sieve out first Subject, Object and Verb
    for index, word_pair in enumerate(ls):
        word = word_pair[1]
        if word == 'PRP' and dict_keywords_position.get('S') == None:
            dict_keywords_position['S'] = [index, word_pair[0]]
        if word == 'NN'  and dict_keywords_position.get('O') == None:
            dict_keywords_position['O'] = [index, word_pair[0]]
        if (word == 'VB' or word == 'VBP' or word == 'VBD' or word == 'IN' or word =='VP') and dict_keywords_position.get('V') == None:
            dict_keywords_position['V'] = [index, word_pair[0]]
    
# #     Get goal state using extract_feature, get_goal, get_goal_index from StanfordCoreNLP output
    parse_tree = get_parse_tree(sentence)

    if extract_feature(get_goal(parse_tree)) != None:
        # print(extract_feature(get_goal(parse_tree)))
        processed_goal = process_goal(extract_feature(get_goal(parse_tree)))
        # print(processed_goal)
        dict_keywords_position['G'] = [get_goal_index(processed_goal, sentence),processed_goal]

    return dict_keywords_position


# print(get_feature_dict('put ball to the front of the blue box'))


# In[16]:


# Defining knowledge base for verb and noun predicates
verb_predicate_functions = {'place':'place','put':'put','pick':'pick','move':'move', 'carry':['lift', 'hold'], 'position':'position', 'close':'close', 'rotate':'rotate', 'appear':'appear', 'go':'move', 'close':'close','open':'open', 'hold':'hold', 'lift':'lift', 'align':'align'}
noun_predicate_functions = {'on':'on', 'down': 'down','align':'align','to':'to', 'left':'left', 'right':'right', 'above':'above','below':'below', 'next to':'next to', 'centre':'centre', 'front':'front', 'back':'back', 'forward':'front', 'backward':'back', 'overlap':'overlap', 'beside':'beside', 'coincides':'overlap', 'at':'at', 'parallel':'parallel', 'up':'up'}

# Test verb_predicate reference to use below
features = get_feature_dict('move the ball to the right of the box')
first_verb = features['V'][1]
atomic_verb_predicate_function = verb_predicate_functions[first_verb]

# print(atomic_verb_predicate_function)
# print(verb_predicate_functions[get_feature_dict(s1)['V'][1]])


# In[17]:


# 3: check if goal state is atomic, if not, process it 

# functions should be independent for each of the checks

# check whether is the verb in base form 
def base_form_check(feature_dict):
    predicate_output = ''
    if feature_dict.get('G') != None:
        final_goal = feature_dict["G"][1].split(' ')
    
#     check whether action is in dictionary
    if verb_predicate_functions.get(feature_dict['V'][1]) == None:
        print('I do not understand this verb')
        exit()

# check wheter in base form
    elif feature_dict['V'][1] == verb_predicate_functions[feature_dict['V'][1]]:
        print(f"{feature_dict['V'][1]} is an atomic verb")
#         check whether has subject, object and goal
#         check whther goal contains noun predicate
        if feature_dict.get('S') == None:
            if feature_dict.get('O') == None:
                predicate_output = (f'{feature_dict["V"][1]}(,,')
    #         check whether has goal
            elif feature_dict.get('G') == None:
                predicate_output = (f'{feature_dict["V"][1]}(,{feature_dict["O"][1]},')
            else:
                predicate_output = (f'{feature_dict["V"][1]}(,{feature_dict["O"][1]},')
    
                for w in final_goal:
                    if noun_predicate_functions.get(w) != None:
#                     if w in noun_predicate_functions:
                        predicate_output = predicate_output + noun_predicate_functions[w] +'(,,' 
                        final_goal = final_goal[final_goal.index(w):]
                        final_goal.remove(w)
                predicate_output = predicate_output + ' '.join(final_goal)
            

        else:
            if feature_dict.get('O') == None:
                predicate_output = (f'{feature_dict["V"][1]}({feature_dict["S"][1]},,')
    #         check whether has goal
            elif feature_dict.get('G') == None:
                predicate_output = (f'{feature_dict["V"][1]}({feature_dict["S"][1]},{feature_dict["O"][1]},)')

    #             check whether goal has noun predicate   
            else:
                predicate_output = (f'{feature_dict["V"][1]}({feature_dict["S"][1]},{feature_dict["O"][1]},')
                for w in final_goal:
                    if noun_predicate_functions.get(w) != None:
#                     if w in noun_predicate_functions:
                        predicate_output = predicate_output + noun_predicate_functions[w] +'(,,'
                        final_goal = final_goal[final_goal.index(w):]
                        final_goal.remove(w)
                predicate_output = predicate_output + ' '.join(final_goal)
            
        closure = ''
        for c in predicate_output:
            if c == '(':
                closure = closure + ')'
        predicate_output = predicate_output + closure
        
# convert into atomic form if verb predicate not in base form

    elif feature_dict['V'][1] != verb_predicate_functions[feature_dict['V'][1]]:
        print("The verb is not in atomic form")
#         check whether has subject, object and goal
#         check whther goal contains noun predicate

        if feature_dict.get('S') == None:
            if feature_dict.get('O') == None:
                predicate_output = (f'{verb_predicate_functions[feature_dict["V"][1]][0]}(,,{verb_predicate_functions[feature_dict["V"][1]][1]}(,,')
    #         check whether has goal
            elif feature_dict.get('G') == None:
                predicate_output = (f'{verb_predicate_functions[feature_dict["V"][1]][0]}(,{feature_dict["O"][1]},{verb_predicate_functions[feature_dict["V"][1]][1]}(,,')
            else:
                predicate_output = (f'{verb_predicate_functions[feature_dict["V"][1]][0]}(,{feature_dict["O"][1]},{verb_predicate_functions[feature_dict["V"][1]][1]}(,,')
                for w in final_goal:
                    if noun_predicate_functions.get(w) != None:
#                     if w in noun_predicate_functions:
                        predicate_output = predicate_output + noun_predicate_functions[w] +'(,,'
                        final_goal = final_goal[final_goal.index(w):]
                        final_goal.remove(w)
                predicate_output = predicate_output + ' '.join(final_goal)
            
        else:
            if feature_dict.get('O') == None:
                predicate_output = (f'{verb_predicate_functions[feature_dict["V"][1]][0]}({feature_dict["S"][1]},,{verb_predicate_functions[feature_dict["V"][1]][1]}(,,')
    #         check whether has goal
            elif feature_dict.get('G') == None:
                predicate_output = (f'{verb_predicate_functions[feature_dict["V"][1]][0]}({feature_dict["S"][1]},{feature_dict["O"][1]},{verb_predicate_functions[feature_dict["V"][1]][1]}(,,')

    #             check whether goal has noun predicate   
            else:
                predicate_output = (f'{verb_predicate_functions[feature_dict["V"][1]][0]}({feature_dict["S"][1]},{feature_dict["O"][1]},{verb_predicate_functions[feature_dict["V"][1]][1]}(,,')
                for w in final_goal:
                    if noun_predicate_functions.get(w) != None:
#                     if w in noun_predicate_functions:
                        predicate_output = predicate_output + noun_predicate_functions[w] +'(,,'
                        final_goal = final_goal[final_goal.index(w):]
                        final_goal.remove(w)
                predicate_output = predicate_output + ' '.join(final_goal)
            
        closure = ''
        for c in predicate_output:
            if c == '(':
                closure = closure + ')'
        predicate_output = predicate_output + closure
    
    return predicate_output 


# In[19]:


def stp_converter(instruction):
    feature_dict = get_feature_dict(instruction)
    
    return base_form_check(feature_dict)


# In[33]:


# print(stp_converter("pick up the diamond on the blue box"))
# print()
# print(stp_converter("pick up the diamond below the blue box"))
# print()
# print(stp_converter("put the diamond to the front of the blue box"))
# print()
# print(stp_converter("put the diamond to the back of the blue box"))
# print()





