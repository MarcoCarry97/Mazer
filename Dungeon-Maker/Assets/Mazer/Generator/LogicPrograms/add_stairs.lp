
%problem instance

#const max=num_rooms*2.

#const min_size=corr_dim+2.



#const init_pos_x=0.

#const init_pos_y=0.



%PART NINE: STAIRS



{stairs_pos(-1,R,X,Y,@rand_dec(X,XS,XR),@rand_dec(Y,YS,YR))} :- end_room(R), room_size(R,XS,YS,XR,YR), room_pos(R,X,Y).

:-end_room(R), {stairs_pos(D,R,X,Y,TX,TY)}!=1.

decoration(D,R,X,Y,TX,TY) :- stairs_pos(D,R,X,Y,TX,TY).





{start_point_pos(-1,R,X,Y,@rand_dec(X,XS,XR),@rand_dec(Y,YS,YR))} :- initial_room(R), room_size(R,XS,YS,XR,YR), room_pos(R,X,Y).

:-initial_room(R), {start_point_pos(D,R,X,Y,TX,TY)}!=1.

decoration(D,R,X,Y,TX,TY) :- start_point_pos(D,R,X,Y,TX,TY).

:-decoration(D1,R,X,Y,_,_), decoration(D2,R,X,Y,_,_), D1!=D2.

%:-stairs(R,X,Y), decoration(D,R,X+1,Y).

%:-stairs(R,X,Y), decoration(D,R,X-1,Y).

%:-stairs(R,X,Y), decoration(D,R,X,Y+1).

%:-stairs(R,X,Y), decoration(D,R,X,Y-1).
%:-stairs(R,X,Y), trap_pos(T,R,X,Y).

%-stairs(R,X,Y), treasure_pos(T,R,X,Y).

%:-stairs(R,X,Y), item_pos(T,R,X,Y).

%:-stairs(R,X,Y), key_pos(T,R,X,Y).









