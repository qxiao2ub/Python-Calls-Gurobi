from gurobipy import *

model=Model()

#Tank capacity
a=[500,400,600,600,900,800,800,400,800]

#demand for each type
d=[1200,700,1000,450,1200]

m=len(a)
n=len(d)
x={}
y={}

for i in range(m-2):
    for j in range(n):
        x[i,j] = model.addVar(vtype=GRB.BINARY, name="x_{}{}".format(i,j))

x[7,0] = model.addVar(vtype=GRB.BINARY, name="x_70")

x[7,1]=0
x[7,2]=0
x[7,3]=0
x[7,4]=0


x[8,4] = model.addVar(vtype=GRB.BINARY, name="x_84")

x[8,0]=0
x[8,1]=0
x[8,2]=0
x[8,3]=0

#for i in range(m):
#    y[i] = model.addVar(vtype=GRB.BINARY,name="y_{}".format(i))


model.update()

#constraint 1
for i in range(m-2):
    model.addConstr(quicksum(x[i,j] for j in range(n)) <= 1)

#constraint 2
for j in range(n):
    model.addConstr(quicksum(a[i]*x[i,j] for i in range(m)) >= d[j] )

model.setObjective(quicksum(x[i,j] for i in range(m) for j in range(n)), GRB.MINIMIZE)

model.optimize()

print('obj: %g' % model.objVal)

for v in model.getVars():
    print('%s %g' % (v.varName, v.x))
