param num;			#number of Dept.

set D:=0..num;			#set of Dept.

param l{i in D};												#length dimension of i
param h{i in D};												#height dimension of i
param b{i in D}:= 2*(l[i]+h[i]);										#perimeter of i
param f{i in D,j in D:i<j} default 0;										#flow between Dept i & j
param lb{i in D, j in D:i<j} default 0;										#lower bound edge contact between i & j
param ub{i in D, j in D:i<j}:= if(i==0) then(b[j] - min(l[j],h[j])) else min(max(l[i],h[i]),max(l[j],h[j]));	#upper bound edge contact between i & j												#height dimension of i
param w{i in D,j in D:i<j}:= if ub[i,j]>0 then f[i,j]/ub[i,j] else 0;						#weighted adjacency between i & j

var x{i in D, j in D:i<j} >=lb[i,j], <=ub[i,j], integer;		#edge contact between i & j

maximize Adjacency: sum{i in D, j in D:i<j}(w[i,j]*x[i,j]);
s.t. Edge{i in D}: sum{j in D:i<j}(x[i,j]) + sum{j in D:i>j}(x[j,i]) = b[i];