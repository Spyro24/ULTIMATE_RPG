"""
    The map editor for pyr_pg(this is included in the pyr_pg execute folder)
    Copyright (C) 2024 Spyro24

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import pygame as p
from text import text_field as inp
import pywin as pw
import time
import map_ as prm

dis_w, dis_h = 500, 500  # the size of the window
toolw = p.display.set_mode((dis_w, dis_h))

cur_tile = 1 #Curent tile for the tool (tile and tiles numbers are in the tiles.list file)
#map
show = []
hit  = []
overlay = []
act  = []
acthit = []
overdraw = []

#internal vars
mx = 0
my = 0
size = 20 #size of font, etc...
img_size = 16 #the image size and must be a multiple of the tile size
img_scale = 1.5 #the scale of the image (img_size * img_scale)
update = 0
run = 1
x_s = 0 #size in X tiles
y_s = 0 #size in Y tiles
map_loaded = False #Check if a map is loaded
new_map = False
redraw = True
edit_mode = 1 #This is for the edit mode selction (0 = no edit mode selectet, 1 = ground, 2 = overlay, 3 = hitbox)
exit_ = False
export_ = False
load_map = True
last_mx = mx
last_my = my

#button values
new_p = False #The "NEW" button
if_b = True # test for the arrow buttons

while run:
    
    #redraw script toredraw the entire display
    if redraw:
        toolw.fill((0,0,0))
        
        #Draw buttons
        pw.draw_rect(toolw, (dis_h / 10) * 8, 0, dis_h / 10 * 2, dis_w / 10 , (125,125,125))
        pw.draw_rect(toolw, (dis_h / 10) * 8, dis_w / 10 * 1, dis_h, dis_w / 10, (100,100,100))
        pw.draw_rect(toolw, (dis_h / 10) * 8, dis_w / 10 * 2, dis_h, dis_w / 10, (125,125,125))
        #pw.draw_rect(toolw, (dis_h / 10) * 8, dis_w / 10 * 4, dis_h, dis_w / 10, (125,125,125))
        pw.draw_font(toolw, size, (dis_h / 10) * 8 + (dis_h / 40), dis_w / 40, "EXIT", (0,0,0))
        pw.draw_font(toolw, size, (dis_h / 10) * 8 + (dis_h / 40), dis_w / 40 * 5, "Clear", (0,0,0))
        pw.draw_font(toolw, size, (dis_h / 10) * 8 + (dis_h / 40), dis_w / 40 * 9, "Tile", (0,0,0))
        #pw.draw_font(toolw, size, (dis_h / 10) * 8 + (dis_h / 40), dis_w / 40 * 17, "Tile", (0,0,0))
        
        #Draw Edit mode Buttons
        pw.draw_rect(toolw, 0, dis_w / 10 * 8, dis_h / 10 * 2, dis_w / 10 , (125,125,125))
        pw.draw_rect(toolw, 0, dis_w / 10 * 9, dis_h / 10 * 2, dis_w / 10 , (100,100,100))
        pw.draw_rect(toolw, dis_h / 10 * 2, dis_w / 10 * 8, dis_h / 10 * 2, dis_w / 10 , (100,100,100))
        pw.draw_rect(toolw, dis_h / 10 * 2, dis_w / 10 * 9, dis_h / 10 * 2, dis_w / 10 , (125,125,125))
        pw.draw_font(toolw, size, (dis_h / 40), dis_w / 40 * 33, "Layer 0", (0,0,0))
        pw.draw_font(toolw, size, (dis_h / 40), dis_w / 40 * 37, "Layer 1", (0,0,0))
        pw.draw_font(toolw, size, (dis_h / 40 * 9), dis_w / 40 * 33, "Hitbox", (0,0,0))
        pw.draw_font(toolw, size, (dis_h / 40 * 9), dis_w / 40 * 37, "Action", (0,0,0))
        
        #draw the map changer arow buttons
        pw.draw_rect(toolw, dis_h / 10 * 9, dis_w / 10 * 8, dis_h / 10 , dis_w / 10 , (125,125,125))
        pw.draw_rect(toolw, dis_h / 10 * 7, dis_w / 10 * 8, dis_h / 10 , dis_w / 10 , (125,125,125))
        pw.draw_rect(toolw, dis_h / 10 * 8, dis_w / 10 * 7, dis_h / 10 , dis_w / 10 , (125,125,125))
        pw.draw_rect(toolw, dis_h / 10 * 8, dis_w / 10 * 9, dis_h / 10 , dis_w / 10 , (125,125,125))
        pw.draw_font(toolw, size * 2, dis_h / 40 * 37, dis_w / 40 * 31.75, ">", (0,0,0))
        pw.draw_font(toolw, size * 2, dis_h / 40 * 29, dis_w / 40 * 31.75, "<", (0,0,0))
        pw.draw_font(toolw, size * 2, dis_h / 40 * 33, dis_w / 40 * 28, "/\\", (0,0,0))
        pw.draw_font(toolw, size * 2, dis_h / 40 * 33, dis_w / 40 * 36, "\/", (0,0,0))

        print(show,hit,overlay,act,acthit,overdraw)
        #Draw the entire map new (use the edit mode to tell wich layers are to draw)
        if edit_mode == 1:
            pw.draw_map(toolw, (0,0), img_size * img_scale, show, (x_s, y_s))
        
        elif edit_mode == 2:
            pw.draw_map(toolw, (0,0), img_size * img_scale, show, (x_s, y_s))
            pw.draw_map(toolw, (0,0), img_size * img_scale, overlay, (x_s, y_s), "ov")
        
        elif edit_mode == 3:
            pw.draw_map(toolw, (0,0), img_size * img_scale, show, (x_s, y_s))
            pw.draw_map(toolw, (0,0), img_size * img_scale, overlay, (x_s, y_s), "ov")
            pw.draw_map(toolw, (0,0), img_size * img_scale, hit, (x_s, y_s), "X")
        
        elif edit_mode == 4:
            pw.draw_map(toolw, (0,0), img_size * img_scale, show, (x_s, y_s))
            pw.draw_map(toolw, (0,0), img_size * img_scale, overlay, (x_s, y_s), "ov")
            pw.draw_map(toolw, (0,0), img_size * img_scale, act, (x_s, y_s), "X")
        
        redraw = False
        update = True
        
    #Display update script
    if update:
        p.display.flip()
        update = False
    
    last_mx = mx
    last_my = my
    #Buttons to interact with the editor vars
    if pw.p_push_button((dis_h / 10) * 8, 0, dis_h, dis_w / 10 ):
        exit_ = True
    if pw.p_push_button2((dis_h / 10) * 8, dis_w / 10 * 1, dis_h, dis_w / 10):
        export_ = True
    if pw.p_push_button((dis_h / 10) * 8, dis_w / 10 * 2, dis_h, dis_w / 10 * 3 ):
        new_p = True
    if pw.p_push_button((dis_h / 10) * 8, dis_w / 10 * 4, dis_h, dis_w / 10 * 5 ):
        tmp_ = inp(toolw,size,30,50,dis_w - 60,size,[(50,50,100),(100,100,100),(255,255,255),(0,0,0)],"Chose a Tile  [0 = BG/NONE/AIR]")
        try:
            tmp_ = int(tmp_)
        except: pass
        if (str(type(tmp_)) == "<class 'int'>") and (tmp_ >= 0):
            cur_tile = int(tmp_)
        redraw = True
    if pw.p_push_button2(0, dis_w / 10 * 8, dis_h / 10 * 6, dis_w / 10 * 2):
        if pw.p_push_button2(0, dis_w / 10 * 8, dis_h / 10 * 2, dis_w / 10):
            edit_mode = 1
            redraw = True
        if pw.p_push_button2(0, dis_w / 10 * 9, dis_h / 10 * 2, dis_w / 10 ):
            edit_mode = 2
            redraw = True
        if pw.p_push_button2(dis_h / 10 * 2, dis_w / 10 * 8, dis_h / 10 * 2, dis_w / 10):
            edit_mode = 3
            redraw = True
        if pw.p_push_button2(dis_h / 10 * 2, dis_w / 10 * 9, dis_h / 10 * 2, dis_w / 10):
            edit_mode = 4
            redraw = True
            
    #Arrow buttons to change the map
    if pw.p_push_button2(dis_h / 10 * 7, dis_w / 10 * 7, dis_h, dis_w):
        if pw.p_push_button2(dis_h / 10 * 9, dis_w / 10 * 8, dis_h / 10 , dis_w / 10):
            load_map = True
            if_b = True
            mx += 1
        elif pw.p_push_button2(dis_h / 10 * 7, dis_w / 10 * 8, dis_h / 10 , dis_w / 10):
            load_map = True
            if_b = True
            mx -= 1
        elif pw.p_push_button2(dis_h / 10 * 8, dis_w / 10 * 7, dis_h / 10 , dis_w / 10):
            load_map = True
            if_b = True
            my -= 1
        elif pw.p_push_button2(dis_h / 10 * 8, dis_w / 10 * 9, dis_h / 10 , dis_w / 10):
            load_map= True
            if_b = True
            my += 1
        time.sleep(0.1)
        
    #check ifa map if loaded or created to avoid data lose
    if new_p:
        if map_loaded :
            check_del = inp(toolw,size,30,50,dis_w - 60,size,[(50,50,100),(100,100,100),(255,255,255),(0,0,0)],"Are you sure? Type 'DELETE'")
            if check_del == "DELETE":
                new_map = True
            else:
                inp(toolw,size,50,50,dis_w - 60,size,[(50,50,100),(100,100,100),(255,255,255),(0,0,0)],"Canceled. Press 'ENTER' to continue")
        else:
            new_map = True
        new_p = False
        redraw = True
        
    #create the map
    if new_map:
        show,hit,overlay,act,acthit,overdraw = [],[],[],[],[],[]
        new_map = False
        map_loaded = True
        for h_ in range(0,int(x_s)):
            for w_ in range(0,int(y_s)):
                show.append(1)
                hit.append(0)
                overlay.append(0)
                act.append(0)
                acthit.append(0)
                overdraw.append(0)
    
    #code that runs if a map is existing
    if map_loaded:
        
        #Editor Window
        void, pressed = pw.button_grid(0,0,img_size * img_scale,x_s,y_s)
        if pressed != None:
            if edit_mode == 1:
                print(pressed)
                show.pop(pressed)
                show.insert(pressed, cur_tile)
                pw.draw_tile(toolw, (0,0), False, img_size * img_scale, void, cur_tile)
                
            if edit_mode == 2:
                overlay.pop(pressed)
                overlay.insert(pressed, cur_tile)
                pw.draw_tile(toolw, (0,0), False, img_size * img_scale, void, show[pressed])
                pw.draw_tile(toolw, (0,0), True, img_size * img_scale, void, cur_tile)
            
            #hitbox editor
            elif edit_mode == 3:
                tester_ = hit.pop(pressed)
                if tester_ == 1:
                    hit.insert(pressed, 0)
                    pw.draw_tile(toolw, (0,0), False, img_size * img_scale, void, show[pressed])
                    pw.draw_tile(toolw, (0,0), True, img_size * img_scale, void, overlay[pressed])
                    time.sleep(0.1)
                else:
                    hit.insert(pressed, 1)
                    pw.draw_tile(toolw, (0,0), False, img_size * img_scale, void, show[pressed])
                    pw.draw_tile(toolw, (0,0), True, img_size * img_scale, void, overlay[pressed])
                    pw.draw_x(toolw, (0,0), img_size * img_scale, void)
                    time.sleep(0.1)
                    
            elif edit_mode == 4:
                act.pop(pressed)
                act.insert(pressed, cur_tile)
                pw.draw_tile(toolw, (0,0), False, img_size * img_scale, void, show[pressed])
                pw.draw_tile(toolw, (0,0), True, img_size * img_scale, void, overlay[pressed])
                if cur_tile !=0:
                    pw.draw_x(toolw, (0,0), img_size * img_scale, void)
                
            update = True
    
    #open the map file and export the map
    if export_:
        if map_loaded:
            inp_ = inp(toolw,size,30,50,dis_w - 60,size,[(50,50,100),(100,100,100),(255,255,255),(0,0,0)],"Export to map [X_Y]")
            mapf = open("../map/" + str(inp_), "bw")
            map_ar = [show,hit,overlay,act,acthit,overdraw]
            for m in range(0, len(map_ar)):
                for n in range(0, int(x_s) * int(y_s)):
                    mapf.write(int.to_bytes(int(map_ar[m][n]), length=2, byteorder="big"))
            mapf.close()
            redraw = True
        export_ = False
    
    #script for maploading
    if load_map:
        if if_b:                
            #save the curent map
            if map_loaded:
                print("wrong")
                mapf = open("../map/" + str(last_mx) + "_" + str(last_my), "bw")
                map_ar = [show,hit,overlay,act,acthit,overdraw]
                print(show,hit,overlay,act,acthit,overdraw)
                for m in range(0, len(map_ar)):
                    for n in range(0, int(x_s) * int(y_s)):
                        mapf.write(int.to_bytes(int(map_ar[m][n]), length=2, byteorder="big"))
                mapf.close()
            else:
                mx = 0
                my = 0
                x_s = 16
                y_s = 16
                
            
            try:
                show,hit,overlay,act,acthit,overdraw = prm.map_load(mx,my,16,16,2)
            except:
                x_s = 16
                y_s = 16
                show,hit,overlay,act,acthit,overdraw = [],[],[],[],[],[] #Clear all map vars
                for h_ in range(0,int(x_s)):
                    for w_ in range(0,int(y_s)):
                        show.append(1)
                        hit.append(0)
                        overlay.append(0)
                        act.append(0)
                        acthit.append(0)
                        overdraw.append(0)
            
            map_loaded = True
            redraw = True
            load_map = False
            if_b = False
            
    
    """#get the state of the X button
    for event in p.event.get():
        if event.type == p.QUIT:
            exit_ = True"""
    
    #Run if a exit action is trigered
    if exit_:
        if map_loaded :
            #check_del = inp(toolw,size,30,50,dis_w - 60,size,[(50,50,100),(100,100,100),(255,255,255),(0,0,0)],"Are you sure? Type 'QUIT'")
            if True:
                 mapf = open("../map/" + str(last_mx) + "_" + str(last_my), "bw")
                 map_ar = [show,hit,overlay,act,acthit,overdraw]
                 for m in range(0, len(map_ar)):
                     for n in range(0, int(x_s) * int(y_s)):
                         mapf.write(int.to_bytes(int(map_ar[m][n]), length=2, byteorder="big"))
                 mapf.close()
                 run = False
            else:
                exit_ = False
                redraw = True
        else:
            run = False
            
p.quit()