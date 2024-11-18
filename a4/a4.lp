% Test Project
#const n1 = 9. % X axis
#const n2 = 7. % Y axis
#const startX = 4.
#const socialDistance = 3.

p(0,4).
p(3,5).
p(6,3).


% #const n1 = 25. % X axis
% #const n2 = 25. % Y axis
% #const startX = 13.
% #const socialDistance = 6.

% p(13,7).
% p(21,4).
% p(4,19).

%*
Project Outline
*%

cell(0..n1,0..n2).

% Cells that should be avoided

wantedCell(X,Y) :- cell(X,Y), p(X1, Y1), (X-X1)**2 + (Y-Y1)**2 < socialDistance**2.

% Cells that be step on
allowedCell(X,Y) :- cell(X,Y), not wantedCell(X,Y).

% starting pathway
p_pathway(-7,-7,startX,0).

% Getting the Possible ways
{p_pathway(X,Y,X,Y+1) : p_pathway(_,_,X,Y), allowedCell(X,Y+1)} .
{p_pathway(X,Y,X+1,Y) : p_pathway(_,_,X,Y), allowedCell(X+1,Y)} .
{p_pathway(X,Y,X-1,Y) : p_pathway(_,_,X,Y), allowedCell(X-1,Y)} .

% removing the set that goes back and forth.
:- p_pathway(X1,Y1,X2,Y2), p_pathway(X2,Y2,X1,Y1).

% removing the set spreads out.
X2=X3:- p_pathway(X1,Y1,X2,Y2), p_pathway(X1,Y1,X3,Y3).

% removing the set that doesn't contain the goal.
:- not p_pathway(_,_,_,n2).

% reorganizing the answer
path(X1,Y1,X2,Y2) :- p_pathway(X1,Y1,X2,Y2), X1!=-7.

% #show allowedCell/2.
% #show path/4.
% #show wantedCell/2.

% Output
#show path/4.
