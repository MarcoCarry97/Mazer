import sys

import clingo

import scripts as s

from clingo.script import register_script

from mazer_context import mazer_context

import random

import clingo

def create_room_dict(room,size_list,expand_list):
    room_dict=dict()
    room=room.replace("place_center(","").replace(")","")
    parts=room.split(",")
    center=dict()
    center["x"]=int(parts[1])
    center["y"]=int(parts[2])
    true_center = dict()
    true_center["x"] = int(parts[3])
    true_center["y"] = int(parts[4])
    room_dict["id"]=int(parts[0])
    room_dict["center"]=center
    room_dict["truecenter"] = true_center
    room_dict["expansions"] = []
    for size in size_list:
        if(size["room"]==room_dict["id"]):
            size_dict=dict()
            size_dict["x"]=size["x"]
            size_dict["y"]=size["y"]
            room_dict["size"]=size_dict
    for expand in expand_list:
        if(expand["room"]==room_dict["id"]):
            exp_dict=dict()
            exp_dict["center"]=expand["center"]
            exp_dict["truecenter"]=expand["truecenter"]
            exp_dict["size"]=expand["size"]
            room_dict["expansions"]+=[exp_dict]
    return room_dict

def create_expand_dict(rooms,sizes,expands):
    lis=[]
    for expand in expands:
        exp_dict = dict()
        expand = expand.replace("expansion(", "").replace(")", "")
        parts = expand.split(",")
        room_list=[]
        for room in rooms:
            room_dict=create_room_dict(room,sizes,[])
            id = int(parts[0])
            exp_id = int(parts[1])
            room_id = int(parts[2])
            if (room_dict["id"] == id):
                exp_dict["id"] = id
                exp_dict["room"] = room_id
                exp_dict["center"] = room_dict["center"]
                exp_dict["truecenter"] = room_dict["truecenter"]
                exp_dict["size"] = room_dict["size"]
                lis += [exp_dict]

    return lis


def create_size_dict(size_list):
    s_list=[]
    for size in size_list:
        size_dict = dict()
        size = size.replace("place_size(", "")
        size = size.replace(")", "")
        parts = size.split(",")
        size_dict["room"]=int(parts[0])
        size_dict["x"] = int(parts[3])
        size_dict["y"] = int(parts[4])
        s_list+=[size_dict]
    return s_list

def create_door_dict(door):
    door_dict=dict()
    door=door.replace("door(","")
    door=door.replace(")","")
    parts=door.split(",")
    door_dict["start"]=int(parts[0])
    door_dict["end"]=int(parts[1])
    door_dict["orientation"]=parts[2]
    return door_dict

def create_decoration_dict(dec_list, type):
    res=[]
    for dec in dec_list:
        dec=dec.replace(type+"_pos(","")
        dec=dec.replace(")","")
        parts=dec.split(",")
        dec_dict=dict()
        dec_dict["type"]=type
        dec_dict["index"]=int(parts[0])
        dec_dict["room"]=int(parts[1])
        pos_dict=dict()
        pos_dict["x"]=int(parts[2])
        pos_dict["y"]=int(parts[3])
        dec_dict["position"]=pos_dict
        res+=[dec_dict]
    return res

def create_stairs_dict(stairs):
    stairs_dict=dict()
    stairs=stairs.replace("stairs(","")
    stairs=stairs.replace(")","")
    parts=stairs.split(",")
    pos_dict = dict()
    pos_dict["x"] = int(parts[3])
    pos_dict["y"] = int(parts[4])
    stairs_dict["room"]=int(parts[0])
    stairs_dict["position"]=pos_dict
    return stairs_dict

def create_start_dict(start):
    start_dict=dict()
    start=start.replace("start_point(","")
    start=start.replace(")","")
    parts=start.split(",")
    pos_dict = dict()
    pos_dict["x"] = int(parts[3])
    pos_dict["y"] = int(parts[4])
    start_dict["room"]=int(parts[0])
    start_dict["position"]=pos_dict
    return start_dict

def extract_init_room_id(init_room):
    init_room=init_room.replace("initial_room(","")
    init_room=init_room.replace(")","")
    return int(init_room)

def create_model_dict(model):
    model_list=to_asp_list(model)
    size,init_room,rooms, doors, traps, treasures,keys, items,enemies, stairs,start,expands=divide_list(model_list)
    model_dict=dict()
    model_dict["rooms"]=[]
    model_dict["doors"]=[]
    size_list=create_size_dict(size)
    expands_list=create_expand_dict(rooms,size_list,expands)
    #print(expands)
    init=None
    if(init_room!=None):
        init=extract_init_room_id(init_room)
    model_dict["init_room"]=init
    model_dict["decorations"]=create_decoration_dict(traps,"trap")
    model_dict["decorations"]+=create_decoration_dict(treasures,"treasure")
    model_dict["decorations"]+=create_decoration_dict(keys,"key")
    model_dict["decorations"]+=create_decoration_dict(items,"item")
    model_dict["decorations"]+=create_decoration_dict(enemies,"enemy")
    if(stairs!=None):
        model_dict["stairs"]=create_decoration_dict([stairs],"stairs")[0]
    if (stairs != None):
        model_dict["startpoint"] = create_decoration_dict([start],"start_point")[0]
    for room in rooms:
        room_dict=create_room_dict(room,size_list,expands_list)
        model_dict["rooms"]+=[room_dict]
    for door in doors:
        door_dict=create_door_dict(door)
        model_dict["doors"]+=[door_dict]
    return model_dict

def divide_list(lis):
    size=[]
    init_room=None
    rooms=[]
    doors=[]
    deltas=[]
    traps=[]
    treasures=[]
    items=[]
    stairs=None
    start=None
    keys=[]
    enemies=[]
    expands=[]
    for literal in lis:
        parts=literal.split("(")
        if(parts[0]=="place_size"):
            size+=[literal]
        elif(parts[0]=="place_center"):
            rooms+=[literal]
        elif(parts[0]=="door"):
            doors+=[literal]
        elif (parts[0] == "delta"):
            deltas += [literal]
        elif(parts[0]=="initial_room"):
            init_room=literal
        elif (parts[0] == "trap_pos"):
            traps+= [literal]
        elif (parts[0] == "treasure_pos"):
            treasures+= [literal]
        elif (parts[0] == "key_pos"):
            keys+= [literal]
        elif (parts[0] == "item_pos"):
            items = [literal]
        elif (parts[0] == "stairs_pos"):
            stairs = literal
        elif (parts[0] == "start_point_pos"):
            start = literal
        elif (parts[0] == "enemy_pos"):
            enemies+=[literal]
        elif (parts[0] == "expansion"):
            expands+=[literal]
    return size, init_room, rooms, doors,traps,treasures, keys,items,enemies,stairs,start, expands


def get_models(input,filename,num_levels,num_rooms, size, distance,path,space,num_trap, num_treasure, num_item,rand_init,corr_size,num_enemy):
    models=[]
    for i in range(0,num_levels):
        levels, status, _ = single_model_solving(input, filename,num_levels, num_rooms, size, distance, path, space,
                                                 num_trap, num_treasure, num_item, rand_init, corr_size, num_enemy,
                                                 previous=models)
        models += [get_rand_models(levels, 1)[0]]
        #print(filename+" "+str(len(levels))+" "+str(len(models)))

    return models

def get_models_from_more_files(inputs,files,num_levels,num_rooms, size, distance,path,space,num_trap, num_treasure, num_item,rand_init,corr_size,num_enemy):
    models=[]
    for input in inputs:
        for file in files:
            #print(file)
            #print(input)
            res = get_models(input, file, 1, num_rooms, size, distance, path, space, num_trap, num_treasure,
                             num_item, rand_init, corr_size, num_enemy)
            input=get_rand_models(res,1)[0]
        models+=[input]
    return models

def single_model_solving(input,filename,num_levels,num_rooms, size, distance,path,space,num_trap, num_treasure, num_item,rand_init,corr_size,num_enemy, previous=None):
    input=to_asp_format(input)

    file = open("LogicPrograms/"+filename)
    program = input+file.read()
    x_start=0
    y_start=0
    if(rand_init):
        max = num_rooms * 2
        random.seed=random.randrange(-max+1,max-1)
        xrand=random.randrange(-max+1,max-1)
        yrand=random.randrange(-max+1,max-1)
        x_start=xrand*distance
        y_start=yrand*distance
        #print(str(x_start)+" "+str(y_start))
    args=["--model="+str(num_levels*space),
          "--rand-freq=0.1",
          "--no-backprop",
          "--restart-on-model",
          #"--seed=1",
          "-c num_rooms="+str(num_rooms),
          "-c max_size="+str(size),
          "-c max_path="+str(path),
          "-c distance="+str(distance),
          "-c num_trap="+str(num_trap),
          "-c num_treasure="+str(num_treasure),
          "-c num_item="+str(num_item),
          "-c corr_dim="+str(corr_size),
          "-c num_enemy="+str(num_enemy),
          "-c x_start="+str(x_start),
          "-c y_start="+str(y_start)]
    control = clingo.Control(arguments=args)
    control.add("base", [], program)
    context=mazer_context()
    sys.stderr.write("Grounding for "+filename+" ...\n")
    control.ground([("base", [])], context=context)
    sys.stderr.write("Solving for "+filename+" ...\n")
    handle=control.solve(yield_=True)
    models=to_model_list(handle)

    if (len(models)==0):
        raise Exception("This logic program cannot generate stable models")
    res= get_distant_models(models,previous,num_levels,filename)

    return res, handle.get(), previous


def to_asp_format(s):
    s=str(s)
    s=s.replace(" ",".")
    if(s!=""):
        s+="."
    return s

def to_asp_list(sample):
    return to_list(to_asp_format(sample), ".")

def not_in_previous(literal, previous):
    for prev in previous:
        prev_list=to_asp_list(prev)
        if(literal in prev_list):
            return 0
    return 1

def to_model_list(handle):
    models=[]
    for model in handle:
        models+=[str(model)]
    return models

def random_formula(num,length):
    multiplier1 = random.randrange(0, length)
    addend1 = random.randrange(0, length)
    multiplier2 = random.randrange(0, length)
    addend2 = random.randrange(0, length)
    num = (num + (1 + addend1) * multiplier1 + (1 + addend2) * multiplier2 + 1) % length
    rand_exp=random.randrange(0, length)
    num= (num+num**rand_exp)%length
    return num

def convert_to_string(model):
    s=""
    for i in range(0,len(model)):
        s+=str(model[i])
        if(i<len(model)-1):
            s+=" "
    return s

def to_list(s,regex):
    lis=[]
    for piece in str(s).split(regex):
        lis=lis+[piece]
    return lis

def count_distance(current_level, previous):
    current_list=to_asp_list(current_level)
    previous_list=to_asp_list(previous)
    distance=0
    for cur_lit in current_list:
        if cur_lit not in previous_list:
            distance+=1
    return distance

def center_distance(current_level, previous):
    current_dict=create_model_dict(current_level)
    previous_dict=create_model_dict(previous)
    distance=0
    for cur_room in current_dict["rooms"]:
        for prev_room in previous_dict["rooms"]:
            if cur_room["id"]==prev_room["id"]:
                distx=abs(cur_room["center"]["x"]-prev_room["center"]["x"])
                disty=abs(cur_room["center"]["y"]-prev_room["center"]["y"])
                distance+=distx+disty
    return distance

def size_distance(current_level, previous):
    current_dict=create_model_dict(current_level)
    previous_dict=create_model_dict(previous)
    distance=0
    for cur_room in current_dict["rooms"]:
        for prev_room in previous_dict["rooms"]:
            if cur_room["id"]==prev_room["id"]:
                distx=abs(cur_room["size"]["x"]-prev_room["size"]["x"])
                disty=abs(cur_room["size"]["y"]-prev_room["size"]["y"])
                distance+=distx+disty
    return distance

def door_distance(current_level,previous):
    current_dict=create_model_dict(current_level)
    previous_dict=create_model_dict(previous)
    current_distance=len(current_dict["doors"])
    previous_distance=len(previous_dict["doors"])
    return abs(current_distance-previous_distance)


def get_measure_functions(file):
    lis = [count_distance]
    if file=="rooms_doors.lp":
        lis+=[center_distance,door_distance]
    if file=="assign_size.lp":
        lis+=[size_distance]
    return lis


def get_rand_models(models,size):
    res=[]
    num=0
    for i in range(0,size):
        num=random_formula(num,len(models))
        res+=[models[num]]
    return res


def get_distant_models(models, previouses,size, file):
    res=[]

    measurements=get_measure_functions(file)
    for i in range(0,size):
        if (len(previouses) == 0):
            res += [get_rand_models(models, 1)[0]]
        else:
            for model in models:
                distance=0
                best=get_rand_models(models,1)
                for prev in previouses:
                    dist=0
                    for measurement in measurements:
                        dist+=measurement(model,prev)
                    if(distance<=dist):
                        best=model
                        distance=dist
                if(best!=None):
                    res += [best]
                    models.remove(best)
    return res

