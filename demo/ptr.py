#!/usr/bin/env python
# coding: utf-8

# In[1]:


# STP: 
# put the diamond on the blue box 
# move(, ball, to(, , 5)
# move(, ball, to(, , right(, ,  of the box)))
# how to get this from STP output

# start of subject1: (5,5)
# start of ball1: (0,5)
# start of box: (0,7)

# end state ball1: (0, 12)

# PTR: mv(xy of subject1, xy of ball1, beside(xy of subject1, xy of ball1, destination))

# look at ROS interface, and figure how to move subject 5 cords of y
# move(subject1, (0,5))
# right()
# put down()


# In[2]:


# class ConstructObj:         
#     for now x,y is of the CG
# starting CG known, also means need to know radius and other measurements
# because can't "scan"
    # def __init__(self, name, x_cord, y_cord):
    #     self.name = name
    #     self.x = x_cord
    #     self.y = y_cord
        
    # def display (self):      
    #     print("Object: %s\nCoords:(%d,%d)" %(self.name, self.x,self.y))      


# In[3]:

# Predicates
# put(, diamond, on the blue)
# put(, diamond, left(, ,  of the blue))
# put(, diamond, above(, , the blue))

# pick(, diamond, on the blue)
# pick(, diamond, left(, ,  of the blue))
# pick(, diamond, above(, , the blue))

# Subject, Object, Goal State
s1 = "move(ball,arm,right)"
# s2 = "move(arm,ball,to(sub,ob,dest))"

def extract_action(predicate):
    s = predicate
    
    elems = s1.split('(')
    
    return elems[0]

# print(extract_action(s1))


# In[4]:


# 'move(arm'
def extract_subject(s):
    elems = s.split('(')
    
    return elems[1]

# print(extract_subject('move(arm'))


# In[5]:


def extract_components(predicate):
    s = predicate
    
    elems = s.split(',')

    subject = extract_subject(elems[0])

    obj = elems[1]
    
#     [:len(elems[2])-1] for getting rid of ')'
    goal_state = elems[2][:len(elems[2])-1]
    
    return subject, obj, goal_state

extract_components(s1)


# In[6]:


def displace(subject, displacement):
    x_diff, y_diff = displacement
    
    subject.x += x_diff
    subject.y += y_diff
    print(f"{subject.name} was displaced by {displacement}")
    
    return subject


# In[7]:


def move_right(subject, obj):
    sub = subject
    
    
#     check that both objects are aligned
    if sub.x == obj.x and sub.y == obj.y:
        # if so, use subject to move object
        sub.x += 5
        obj.x += 5
        print(f"{sub.name} Moved {obj.name} right 5 units")
    
    
    # if not, align them
    else:
#         Object is reference point, we move subject to obj
        x_diff = obj.x - sub.x
        y_diff = obj.y - sub.y
        displacement = (x_diff, y_diff)
        
#         displace to align first
        displace(subject, displacement)
        
#         then move default right
        sub.x += 5
        obj.x += 5

        print(f"{sub.name} Moved {obj.name} right 5 units")


# In[8]:


verb_dict = {"put":put, "pick":pick }


# In[9]:


def ptr(predicate, construct):
    subject, obj, goal_state = extract_components(predicate)
    action = extract_action(predicate)
    
#     Checks will based on action-goal_state, so check which action first 
    search_key = action + '_' + goal_state
    
    function_from_known_actions_dict = verb_dict[search_key]
    
#         use ConstructObj 'name' prop to match objects to predicate subject-obj
    sub2 = construct[0]
    obj2 = construct[1]

    # print(sub2.name, obj2.name)
    
    # call function
    function_from_known_actions_dict(sub2, obj2)

#     check current state of both objects

#     define position to grab ball

#   if hand grabbing ball, execute action
#     what is hand grabbing ball?
#       based on current coords
#         how to match desired action based on components?
        

        
#   else make them in position


# In[10]:


# arm = ConstructObj("arm",5,0)
# ball = ConstructObj("ball",5,0)

# arm = ConstructObj("arm",5,10)
# ball = ConstructObj("ball",5,0)

# construct = [arm, ball]


# In[11]:


# for obj in construct:
#     obj.display()
#     print()


# In[12]:


# s1 = "move(ball,arm,right)"
# ptr(s1, construct)


# In[13]:


# for obj in construct:
#     obj.display()



