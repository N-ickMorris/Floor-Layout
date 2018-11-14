param numD;		#number of dept

set D:=1..numD;		#set of dept

param f{i in D,j in D} default 0;			#flow between dept i & j
param Bx;						#length of building
param By;						#width of building
param Lu{i in D};					#upper length limit for dept i
param Ll{i in D};					#lower length limit for dept i
param Wu{i in D};					#upper width limit for dept i
param Wl{i in D};					#lower width limit for dept i
#param Pu{i in D};					#upper perimeter limit for dept i
#param Pl{i in D};					#lower perimeter limit for dept i

var l{i in D} integer, >=Ll[i], <=Lu[i];		#length of dept i
var w{i in D} integer, >=Wl[i], <=Wu[i];		#width of dept i
var x{i in D} integer, >=0;				#x-coordinate of bottom left corner of dept i
var y{i in D} integer, >=0;				#y-coordinate of bottom left corner of dept i
var Zx{i in D, j in D} binary;				#dept i is/isn't to the left of dept j
var Zy{i in D, j in D} binary;				#dept i is/isn't below dept j
var a{i in D, j in D};					#horizontal distance between the centroids of dept i & j
var b{i in D, j in D}; 					#vertical distance between the centroids of dept i & j

minimize Disorder:sum{i in D, j in D}((if f[i,j] > 0 then f[i,j])*(a[i,j]+b[i,j]));
s.t. AdjacencyX{i in D, j in D: i!=j}: x[i] + l[i] <= x[j]+(Bx*(1-Zx[i,j]));
s.t. AdjacencyY{i in D, j in D: i!=j}: y[i] + w[i] <= y[j]+(By*(1-Zy[i,j]));
s.t. Orientation{i in D, j in D: i<j}: Zx[i,j] + Zx[j,i] + Zy[i,j] + Zy[j,i] >= 1;
s.t. CoordinateX{i in D}: x[i] + l[i] <= Bx;
s.t. CoordinateY{i in D}: y[i] + w[i] <= By;
s.t. CenterX1{i in D, j in D: i<j}: a[i,j] >= (x[i]+(.5*l[i])-x[j]-(.5*l[j]));
s.t. CenterX2{i in D, j in D: i<j}: a[i,j] >= -(x[i]+(.5*l[i])-x[j]-(.5*l[j]));
s.t. CenterY1{i in D, j in D: i<j}: b[i,j] >= (y[i]+(.5*w[i])-y[j]-(.5*w[j]));
s.t. CenterY2{i in D, j in D: i<j}: b[i,j] >= -(y[i]+(.5*w[i])-y[j]-(.5*w[j]));
#s.t. Perimeter{i in D}: Pl[i] <= 2*(l[i] + w[i]) <= Pu[i];