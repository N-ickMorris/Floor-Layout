# facilities planning: layout IP
# this model is intended to minimize the distance between departments with high rates of flow (ie. ppl, material, information)

# ---- setup the model ----

from pyomo.environ import *    # imports the pyomo envoirnment
model = AbstractModel()    # creates an abstract model
model.name = "Layout IP Model"    # gives the model a name

# ---- define set(s) ----

model.D = Set()    # a set of departments

# ---- define parameter(s) ----

model.f = Param(model.D,model.D)    # the flow between two departments
model.Bl = Param()    # length of the building
model.Bw = Param()    # width of the building
model.l = Param(model.D)    # length of a department
model.w = Param(model.D)    # width of a department

# if department sizes are unknown or stochastic, use these parameters in place of parameters 'model.l' and 'model.w'

#model.Lu = Param(model.D)    # upper length limit for a department
#model.Ll = Param(model.D)    # lower length limit for a department
#model.Wu = Param(model.D)    # upper width limit for a department
#model.Wl = Param(model.D)    # lower width limit for a department
#model.Pu = Param(model.D)    # upper perimeter limit for a department
#model.Pl = Param(model.D)    # lower perimeter limit for a department

# ---- define variable(s) ----

model.x = Var(model.D, domain = NonNegativeReals)    # x-coordinate of bottom left corner of a department
model.y = Var(model.D, domain = NonNegativeReals)    # y-coordinate of bottom left corner of a department
model.Zx = Var(model.D, model.D, domain = Binary)    # a department is/isn't to the left of another department
model.Zy = Var(model.D, model.D, domain = Binary)    # a department is/isn't below another department
model.h = Var(model.D, model.D, domain = NonNegativeReals)    # horizontal distance between the centriods of two departments
model.v = Var(model.D, model.D, domain = NonNegativeReals)    # vertical distance between the centriods of two departments

# if department sizes are unknown or stochastic, use these variables in place of parameters 'model.l' and 'model.w'

#def xbounds_rule(model,i):
#    return(model.Ll[i], model.Lu[i])    # length limit oF a department
#
#def xbounds_rule(model,i):
#    return(model.Wl[i], model.Wu[i])    # width limit oF a department
#
#model.l = Var(model.D, bounds = xbounds_rule, domain = Integers)
#model.w = Var(model.D, bounds = xbounds_rule, domain = Integers)

# ---- define objective function(s) ----

def obj(model):
    return sum(sum(model.f[i,j]*(model.h[i,j] + model.v[i,j]) for i in model.D) for j in model.D)    # the weighted distance function between departments

model.obj = Objective(rule = obj, sense = minimize)    # a minimization problem of the function defined above

# ---- define constraint(s) ----

def AdjX(model, i, j):
    if i != j:
        return model.x[i] + model.l[i] - model.x[j] - (model.Bl*(1 - model.Zx[i,j])) <= 0    # maintains adjacency between departments such that departments don't overlap along the x-axis
    else:
        return Constraint.Skip

def AdjY(model, i, j):
    if i != j:
        return model.y[i] + model.w[i] - model.y[j] - (model.Bw*(1 - model.Zy[i,j])) <= 0    # maintains adjacency between departments such that departments don't overlap along the y-axis
    else:
        return Constraint.Skip

def Orient(model, i, j):
    if i != j:
        return model.Zx[i,j] + model.Zx[j,i] + model.Zy[i,j] + model.Zy[j,i] >= 1    # define the adjacent orientation of a department relative to another
    else:
        return Constraint.Skip

def CoorX(model, i):
    return model.x[i] + model.l[i] <= model.Bl    # a department cannot be positioned outside the x-axis building limits

def CoorY(model, i):
    return model.y[i] + model.w[i] <= model.Bw    # a department cannot be positioned outside the y-axis building limits

def CenX1(model, i, j):
    if i != j:
        return model.h[i,j] - (model.x[i] + (0.5*model.l[i]) - model.x[j] - (0.5*model.l[j])) >= 0    # the x-axis distance between a department and another (set 1 of 4 absolute value constraints)
    else:
        return Constraint.Skip

def CenX2(model, i, j):
    if i != j:
        return model.h[i,j] + (model.x[i] + (0.5*model.l[i]) - model.x[j] - (0.5*model.l[j])) >= 0    # the x-axis distance between a department and another (set 2 of 4 absolute value constraints)
    else:
        return Constraint.Skip

def CenY1(model, i, j):
    if i != j:
        return model.v[i,j] - (model.y[i] + (0.5*model.w[i]) - model.y[j] - (0.5*model.w[j])) >= 0    # the y-axis distance between a department and another (set 3 of 4 absolute value constraints)
    else:
        return Constraint.Skip

def CenY2(model, i, j):
    if i != j:
        return model.v[i,j] + (model.y[i] + (0.5*model.w[i]) - model.y[j] - (0.5*model.w[j])) >= 0    # the y-axis distance between a department and another (set 4 of 4 absolute value constraints)
    else:
        return Constraint.Skip

model.AdjacencyX = Constraint(model.D, model.D, rule = AdjX)    # x-axis adjacency constraint for every pair of departments compared
model.AdjacencyY = Constraint(model.D, model.D, rule = AdjY)    # y-axis adjency constraint for evey pair of departments compared
model.Orientation = Constraint(model.D, model.D, rule = Orient)    # orientation constraint for every pair of departments compared
model.CooridnateX = Constraint(model.D, rule = CoorX)    # the x-cooridnate limitation constraint for every department
model.CoordinateY = Constraint(model.D, rule = CoorY)    # the y-cooridnate limitation constraint for every department
model.CenterX1 = Constraint(model.D, model.D, rule = CenX1)    # absolute value distance constraint 1 for every pair of departments compared
model.CenterX2 = Constraint(model.D, model.D, rule = CenX2)    # absolute value distance constraint 2 for every pair of departments compared
model.CenterY1 = Constraint(model.D, model.D, rule = CenY1)    # absolute value distance constraint 3 for every pair of departments compared
model.CenterY2 = Constraint(model.D, model.D, rule = CenY2)    # absolute value distance constraint 4 for every pair of departments compared

# if department sizes are unknown or stochastic, include this additional perimeter constraint

#def Perim(model,i):
#    return model.Pl[i] <= 2*(model.l[i] + model.w[i]) <= model.Pu[i]    # perimeter limit oF a department
#
#model.Perimeter = Constraint(model.D, rule = Perim)    # the perimeter limitation constraint for every department

# ---- execute solver ----

from pyomo.opt import SolverFactory
opt = SolverFactory("glpk")
# opt = SolverFactory('ipopt',solver_io='nl')
instance = model.create_instance("layout2.dat")
results = opt.solve(instance)
instance.display()
