from karel.stanfordkarel import *
import stp
import copy

def turn_right():
    for i in range(3):
        turn_left()
    

def displace(displacement):
#     assume Karel facing RIGHT

    # reach the origin first, then from origin go to destination

    # go up first
    turn_left()
    for j in range(displacement[1]):
        move()

    turn_right()
    for i in range(displacement[0]):
        move()


def update_location(k,dest):
    x , y = copy.deepcopy(dest)
    k[0] = x
    k[1] = y

    return k

def get_displacement(start, end):
    x_diff = end[0] - start[0]
    y_diff = end[1] - start[1]
    return (x_diff, y_diff)


def back_to_origin(karel):
    # Karel starting face right
    origin = [1,1]

    x_diff = karel[0] - origin[0]
    y_diff = karel[1] - origin[1]

    # go down first
    turn_right()
    for i in range(y_diff):
        move()

    # then go left
    turn_right()
    for j in range(x_diff):
        move()

    # back to default face right position
    for i in range(2):
        turn_right()

    update_location(karel, origin)


def pick(karel, destination):
    displacement = get_displacement(karel, destination)

    if displacement[0] == 0 and displacement[1] == 0:
        pick_beeper()

    else:
        displace(displacement)
        print("The displacement required is: ", displacement)
        pick_beeper()
        update_location(karel,destination)


def put(karel, destination):
    displacement = get_displacement(karel, destination)

    if displacement[0] == 0 and displacement[1] == 0:
        put_beeper()

    else:
        displace(displacement)
        print("The displacement required is: ", displacement)
        put_beeper()
        update_location(karel,destination)


def spatial_processor(spatial_ref, goal_state_location):

    # get the function
    function_from_known_spatial_dict = spatial_dict[spatial_ref]

    # call the function
    final_destination = function_from_known_spatial_dict(goal_state_location)

    return final_destination


def on(goal_state_location):
    return goal_state_location


def on(goal_state_location):
    goal = copy.deepcopy(goal_state_location)
    goal[1] += 1
    return goal


def below(goal_state_location):
    goal = copy.deepcopy(goal_state_location)
    goal[1] -= 1
    goal[0] -= 1
    return goal


def front(goal_state_location):
    goal = copy.deepcopy(goal_state_location)
    goal[0] -= 1
    return goal


def back(goal_state_location):
    goal = copy.deepcopy(goal_state_location)
    goal[0] += 1
    return goal


# End of Karel Functions
# Start of PTR

# Predicates
# place(,diamond,on(,,the blue box))
# place(,diamond,above(,,the blue box))
# place(,diamond,right(,,the blue box))

# pick(,diamond,on(,,the blue box))
# pick(,diamond,above(,,the blue box))
# pick(,diamond,on(,,right(,,the blue box)))


# Intermediate Predicate Processing Functions


def extract_action(predicate):
    s = predicate
    
    elems = s.split('(')
    
    return elems[0]


def extract_subject(s):
    elems = s.split('(')
    
    return elems[1]


def extract_components(predicate):
    s = predicate
    
    elems = s.split(',')

    # print(elems)
    
#     [:len(elems[2])-1] for getting rid of ')'
    spatial_ref = elems[2][:len(elems[2])-1]
    
    # get color
    goal_state_ref = elems[-1].split()[1]
    
    return spatial_ref, goal_state_ref

# End Predicate Processing Functions


# PTR
verb_dict = {"put":put, "pick":pick }
spatial_dict = {"on":on, "below":below, "front":front, "back":back }


def main():
    karel = [1, 1]
    red = [4, 1]
    green = [7, 2]
    blue = [10, 3]

    talking = True

# on, next to (left/right), flexibility (different sequence)
# on is equal, Left/Right/Above/Below

    while talking:
        print()
        instruction = input("What should Karel do?")
        print()

        if instruction.lower() != "done":
            print(f"Sending '{instruction}' to STP")
            print()
            predicate = stp.stp_converter(instruction)
            print(f"The predicate output is: '{predicate}'")
            print()
            print(f"Sending '{predicate}' to PTR")
            print()

            # get all components required for processing
            spatial_ref, goal_state_ref = extract_components(predicate)
            action = extract_action(predicate) 

            dest_base_location = []
            # Select goal from ptr (blue, red, green)
            if goal_state_ref == "red":
                dest_base_location = red
            elif goal_state_ref == "blue":
                dest_base_location = blue
            elif goal_state_ref == "green":
                dest_base_location = green
            
            print(f"The destination reference is at:", dest_base_location)

            # process goal state from ptr
            processed_destination = spatial_processor(spatial_ref, dest_base_location)
            print("The exact destination is at:", processed_destination)

            # visualise
            # get which movement
            function_from_known_actions_dict = verb_dict[action]

            # call the movement
            function_from_known_actions_dict(karel, processed_destination)

            # go home
            back_to_origin(karel)

        else:
            print("Thanks for using Karel!")
            talking = False
            exit()


if __name__ == "__main__":
    run_karel_program("final_demo.w")

