import pygame as p
import pyr_pg.map_ as map_to 

def dialog_wrapper(win,map_,script, *debug):
    #init all vars
    reba = []
    iter_ = 0
    cpos = 0 #The curent execute position for a script
    run_ = True #if this false the code stops
    script = open("./dialog/" + str(map_[0]) + "_" + str(map_[1]) + "/" + str(script) + ".dialog")
    code = script.readlines()
    empty3829 = len(code) #this is for thw ma lenght of a script
    
    #run the dialog script file
    while cpos < int(empty3829) and run_:
        #get curent code
        cur = code[cpos]
        print(cur)
        
        #split the string at ;
        csp = cur.split(";")
        
        #check forthe end of execution
        if csp[0] == "#end":
            run_ = False
            
        #set the player position
        elif csp[0] == "#setpos":
            x = int(csp[1])
            y = int(csp[2])
            reba.append("player_p_set")
            reba.append(x)
            reba.append(y)
            
        #jump to the chosen line
        elif csp[0] == "#jmp":
            cpos = int(csp[1]) - 2
        
        cpos += 1
    
    return reba