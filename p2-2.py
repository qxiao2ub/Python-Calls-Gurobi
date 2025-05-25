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

T=[[18,0,0,0,0],
  [12,17,17,0,0],
  [15,0,0,14,0],
  [0,11,11,0,0],
  [0,13,13,0,12],
  [0,10,10,12,18],
  [8,0,0,16,0],
  [0,0,0,0,18]]

m=8
n=4
q=5

model = Model()

x = model.addVars(m,m,vtype=GRB.BINARY,name="pair")

#x = model.addVars(8,8,vtype=GRB.BINARY,name="")

model.update()

for i in range(m):
    for t in range(i+1,8):
        for k in range(q):
            model.setObjectiveN((T[i][k]+T[t][k])*x[i,t], 2, 1)

model.setObjectiveN(quicksum(a[i][j]*b[i][k]*a[t][j]*b[t][k]*x[i,t] for i in range(m) for t in range(i+1,m) for j in range(n) for k in range(q)),1,2)

model.modelSense=GRB.MAXIMIZE

#model.modelSense=GRB.MAXIMIZE

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

model.addConstr(x[5,7]*x[6,7] == 0)

model.addConstr(x[2,5]*x[4,5] == 0)



model.optimize()

#print('Obj: %g' % model.objVal)

for v in model.getVars():
    print('%s %g' % (v.varName, v.x))

u=x[1,3]*(T[1][1]+T[1][3])
o=x[2,6]*(T[2][3]+T[6][3])
h=x[4,5]*(T[4][4]+T[5][4])

print(u)
print(o)
print(h)

#print(Max([1*x[1,3],2*x[2,6],3*x[4,5]]))

#T[1][1]+T[1][3])
#(T[2][3]+T[6][3])*
#(T[4][5]+T[5][5])*

#for i in range(m):
#    for t in range(i+1,8):
#        for k in range(q):
#            model.setObjectiveN((T[i][k]+T[t][k])*x[i,t], 2,
