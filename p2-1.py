from gurobipy import *

#create parameters for X[ij]
a=[[1,1,0,0],
   [1,0,1,0],
   [0,0,1,0],
   [1,1,0,0],
   [0,1,0,1],
   [0,1,1,0],
   [0,0,1,0],
   [0,0,1,1]]

b=[[1,0,0,0,0],
   [1,1,1,0,0],
   [1,0,0,1,0],
   [0,1,1,0,0],
   [0,1,1,0,1],
   [0,1,1,1,1],
   [0,0,0,1,0],
   [0,0,0,0,1]]

m=8
n=4
q=5

model = Model()

x = model.addVars(m,m,vtype=GRB.BINARY,name="pair")

#x = model.addVars(8,8,vtype=GRB.BINARY,name="")

model.update()

model.setObjective(quicksum(a[i][j]*b[i][k]*a[t][j]*b[t][k]*x[i,t] for i in range(m) for t in range(i+1,m) for j in range(n) for k in range(q)), GRB.MAXIMIZE)
#model.setObjective(quicksum(x[i,t] for i in range(m) for t in range(i+1,8)),GRB.MAXIMIZE)

#for i in range(m):
#    model.addConstr(quicksum(x[i,t] for t in range(i+1,8)) <= 1)

#for i in range(m):
#    for j in range(n):
#            for k in range(q):
#                for t in range(i+1,8):
#                    model.addConstr(x[i,t] <= a[i][j]*b[i][k]*a[t][j]*b[t][k])

#for i in range(m):
#    for t in range(i+1,m):
#        for s in range(t+1,m):
#            model.addConstr(x[i,t]*x[t,s] == 0)

for i in range(m):
    for t in range(i+1,m):
        for s in range(t+1,m):
            model.addConstr(x[i,t]*x[t,s] == 0)

for i in range(m):
    for t in range(i+1,m):
        for q in range(i+1,t-1):
            #if i+2 < t:
                model.addConstr(x[i,t]*x[q,t] == 0)

for i in range(m):
    for t in range(i+1,m):
        for c in range(t+1,8):
            model.addConstr(x[i,t]*x[i,c] == 0)

model.addConstr(x[3,5]*x[4,5] == 0)

model.optimize()

#print('Obj: %g' % model.objVal)

for v in model.getVars():
    print('%s %g' % (v.varName, v.x))
