import json
from enum import Enum

class State(Enum):
    VIEWING = 1
    ADDING = 2
    EDITING = 3
    DELETING = 4
    DECIDING = 5

#Objectives: date and reminders. Application check. Major perhaps? CommonApp? Dream, reach, etc

#Template entry
# {
#     "UT Austin": {
#         "appType": "reach",
#         "deadline": "_",
#         "site": "CommonApp",
#         "major": "electrical",
#         "progress": "started"
#     }
# }

#Things to make sure to do:
#   Be able to quit everywhere: DONE hopefully
#   Add reminder or something: using dateutils


KEYS = ("appType", "deadline", "site", "major", "progress")
KEY_STRINGS = ("Safety, reach, or dream", "Deadline", "Application site", "Major", "Progress")
NOTFOUND = "N/A" #can probably be defeated

CORRUPTION_MESSAGE = "Error in JSON. Check that all colleges follow the template entry"


data = {}
started = False
state = State.DECIDING

college_selected = None

def corruption_check():
    for college in data:
        if len(data[college]) != len(KEYS):
            raise Exception(CORRUPTION_MESSAGE)
        
        for key in KEYS:
            if key not in data[college]:
                raise Exception(CORRUPTION_MESSAGE)

def print_data():
    index = 0
    
    for college in data:
        print_college(college)

        if index < len(data) - 1:
            print()
            
        index += 1

def print_college(college):
    print(college)
        
    for i in range(0, len(KEYS)):
        print(KEY_STRINGS[i] + ": " + data[college][KEYS[i]]) #Don't think the notfound should be necessary

def check_for_return(string):
    global state
    
    if string == "y" or string == "Y":
        state = State.DECIDING
        return True
    
    return False

def select_option(options, is_second_part, select_string):
    global state
    
    decision = None
    
    choices = {}
        
    index = 1
    for item in options:
        #Int or string, that is the question
        choices[index] = item
        
        print(" [" + str(index) + "] " + (item if not is_second_part else (KEY_STRINGS[index - 1] + ": " + options[item])))
        
        index += 1

    if not is_second_part:
        print("\nEnter Y on any of the prompts to return/restart")

    while True:
        selected = input(select_string + ": ")
        
        if check_for_return(selected):
            state = State.DECIDING
            break
        
        if selected.isdigit():
            #probably a bad idea
            selected = int(selected)
            
            if selected in choices:
                decision = choices[selected]
                break

    return decision

def input_app_type():
    global state

    #Reach, etc
    appType = None
    while appType != "safety" and appType != "reach" and appType != "dream":
        appType = input(KEY_STRINGS[0] + " (choose 1): ").lower()

        if check_for_return(appType):
            state = State.DECIDING
            break

    return appType

def input_deadline():
    global state
    
    deadline = input(KEY_STRINGS[1] + " (m/d/y): ")
    
    if check_for_return(deadline):
        state = State.DECIDING
    
    return deadline

def input_website():
    global state
    
    site = input(KEY_STRINGS[2] + ": ")
        
    if check_for_return(site):
        state = State.DECIDING
    
    return site

def input_major():
    global state
    
    major = input(KEY_STRINGS[3] + ": ")
        
    if check_for_return(major):
        state = State.DECIDING
        
    return major

def input_progress():
    global state
    
    progress = None
    while progress != "not started" and progress != "in progress" and progress != "finished":
        progress = input(KEY_STRINGS[4] + " (not started, in progress, finished): ").lower()
        
        if check_for_return(progress):
            state = State.DECIDING
            break
    
    return progress
    

while True:
    if not started:
        print("Welcome to the college selection thingy")
        started = True
        
    else:
        print()
        
    with open("data.json", "r", encoding= "utf-8") as f:
        if f.read(1):
            f.seek(0)
            data = json.load(f)
        
            corruption_check()
        
        if len(data) == 0:
            state = State.ADDING
    
    if state == State.DECIDING:
        print("What do you want to do?\n [1] View\n [2] Add\n [3] Edit\n [4] Delete")
        
        while True:
            decision = input()
            
            if decision == "1":
                state = State.VIEWING
                break
                
            elif decision == "2":
                state = State.ADDING
                break
            
            elif decision == "3":
                state = State.EDITING
                break
            
            elif decision == "4":
                state = State.DELETING
                break
            
            else:
                print("Invalid option. Perhaps try again?")


    elif state == State.VIEWING:
        print_data()
        
        # while True:
        #     decision = input("Enter Y to return: ")
            
        #     if check_for_return(decision):
        #         break
        
        state = State.DECIDING
        
        
    elif state == State.ADDING:
        if len(data) == 0:
            print("No colleges yet")
            
        else:
            print("Inputted colleges for reference")
            
            index = 1
            for college in data:
                print(" " + college)
                index += 1
        
        print("\nEnter Y on any of the prompts to return/restart")

        #College name
        decision = input("Add a college: ")
        
        if check_for_return(decision):
                continue
        
        while decision in data:
            decision = input("Already entered. Add a new college: ")
            
            if check_for_return(decision):
                continue
        
        temp_dict = {}

        #Not sure what to call this. Safety reach dream
        appType = input_app_type()
            
        if state == State.DECIDING:
            continue
            
        temp_dict[KEYS[0]] = appType
        
        #Deadline
        deadline = input_deadline()
        
        if state == State.DECIDING:
            continue
        
        temp_dict[KEYS[1]] = deadline
        
        #Website
        site = input_website()
        
        if state == State.DECIDING:
            continue
        
        temp_dict[KEYS[2]] = site
        
        #Major
        major = input_major()
        
        if state == State.DECIDING:
            continue
        
        temp_dict[KEYS[3]] = major
        
        #Progress
        progress = input_progress()
            
        if state == State.DECIDING:
            continue
            
        temp_dict[KEYS[4]] = progress
        
        data[decision] = temp_dict
        
        with open("data.json", "w", encoding= "utf-8") as f:
            f.write(json.dumps(data, ensure_ascii= False, indent= 4))

        state = State.DECIDING
        
        
    else:
        college = select_option(data, False, "Select a college to " + ("edit" if state == State.EDITING else "delete"))
        
        if state == State.DECIDING:
            continue
        
        if state == State.EDITING:
            while True:
                print()
                
                decision2 = select_option(data[college], True, "Select something to edit")
            
                if state == State.DECIDING:
                    break
            
                print()
            
                to_input = None
                #This chain might be avoided if I used the thing in the function. Probably not
                if decision2 == KEYS[0]:
                    to_input = input_app_type()
                elif decision2 == KEYS[1]:
                    to_input = input_deadline()
                elif decision2 == KEYS[2]:
                    to_input = input_website()
                elif decision2 == KEYS[3]:
                    to_input = input_major()
                elif decision2 == KEYS[4]:
                    to_input = input_progress()
                
                if state == State.DECIDING:
                    break
                
                data[college][decision2] = to_input 
            
                with open("data.json", "w", encoding= "utf-8") as f:
                    f.write(json.dumps(data, ensure_ascii= False, indent= 4))
                        
        else:
            data.pop(college)
            
            print("\n" + college + " deleted")
            
            with open("data.json", "w", encoding= "utf-8") as f:
                f.write(json.dumps(data, ensure_ascii= False, indent= 4))
            
            #Delete this for infinite deleting
            state = State.DECIDING