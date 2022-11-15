#const horizon=1.
horizon(horizon).

%- Nodes of the graph
#defined node/2.
%- Robots of the mapf problem
#defined robot/1.
%- Assign the final position to a robot
#defined final/2.

time(1..H):- horizon(H).
direction((X,Y)) :- X=-1..1, Y=-1..1, |X+Y|=1.
nextto((X,Y),(DX,DY),(X+DX,Y+DY)) :- node(X,Y), direction((DX,DY)), node(X+DX,Y+DY).

{ move(R,D,T) : direction(D) } =1 :- robot(R), time(T).

%- Recurcively generate position for each step
position(R,C,T) :- move(R,D,T), position(R,C',T-1),     nextto(C',D,C).

%- it is not possible to move to a NOT neighboring node 
:- move(R,D,T), position(R,C ,T-1), not nextto(C ,D,_).

%- Check if robot reach its goal
processed(R,S) :- final(R,C),robot(R), position(R,C,H), horizon(H).
processed(R)   :- processed(R,S).
%- it is not possible that a robot did not reached its goal
:- final(R,_), not processed(R).

#show position/3.
#show horizon/1.
#show processed/2.
