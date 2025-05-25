from gurobipy import *


model = Model()

#create parameters for w[i]
weight=[34,6,8,17,16,5,13,21,25,31,14,13,33,9,25,25];


m=len(weight) #number of boxes
n=3
x={}


# create variables for x[i][j]
for i in range(m):
    for j in range(n):
        x[i,j] = model.addVar(vtype=GRB.BINARY, name="x_{}{}".format(i,j))

t = model.addVar(vtype=GRB.CONTINUOUS, ub=100, name="t")

# integrate new variables
model.update()

# add constraint for each wagon capacity
for j in range(n):
    model.addConstr(quicksum(weight[i] * x[i,j] for i in range(m)) <= 100)

#add constraint to guarantee each box is assigned
for i in range(m):
    model.addConstr(quicksum(x[i,j] for j in range(n)) == 1 )

for j in range(n):
    model.addConstr(quicksum(weight[i]*x[i,j] for i in range(m)) <= t)

#objective function
model.setObjective(t, GRB.MINIMIZE)

model.optimize()

print('Obj: %g' % model.objVal)
