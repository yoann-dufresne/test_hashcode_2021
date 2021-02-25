inputs="""100 65 60 60
5 mushrooms onions neapolitan-crust emmental-cheese cheddar
8 mushrooms tomatoes onions pineapple neapolitan-crust emmental-cheese mozzarella cheddar
1 basil
3 tomatoes emmental-cheese mozzarella
1 pineapple
4 onions neapolitan-crust emmental-cheese mozzarella
3 mushrooms basil mozzarella
7 mushrooms onions pineapple ham neapolitan-crust mozzarella cheddar
3 pineapple ham neapolitan-crust
1 ham
3 tomatoes basil mozzarella
6 mushrooms tomatoes ham neapolitan-crust mozzarella cheddar
9 mushrooms tomatoes onions ham basil neapolitan-crust emmental-cheese mozzarella cheddar
3 mushrooms tomatoes mozzarella
8 mushrooms onions pineapple neapolitan-crust ham basil emmental-cheese cheddar
4 mushrooms emmental-cheese mozzarella cheddar
2 basil cheddar
7 tomatoes pineapple neapolitan-crust basil emmental-cheese mozzarella cheddar
3 ham neapolitan-crust mozzarella
4 onions ham basil cheddar
4 pineapple ham emmental-cheese mozzarella
8 mushrooms tomatoes onions pineapple basil neapolitan-crust mozzarella cheddar
2 ham neapolitan-crust
3 neapolitan-crust emmental-cheese cheddar
3 mushrooms basil neapolitan-crust
2 pineapple mozzarella
2 mushrooms tomatoes
2 emmental-cheese mozzarella
10 mushrooms tomatoes onions pineapple basil ham neapolitan-crust emmental-cheese mozzarella cheddar
2 mushrooms ham
1 mozzarella
3 onions basil cheddar
2 onions cheddar
9 mushrooms tomatoes onions pineapple neapolitan-crust basil emmental-cheese mozzarella cheddar
4 mushrooms tomatoes basil emmental-cheese
10 mushrooms tomatoes onions pineapple ham basil neapolitan-crust emmental-cheese mozzarella cheddar
2 onions neapolitan-crust
1 emmental-cheese
5 mushrooms tomatoes onions basil cheddar
1 onions
2 mushrooms emmental-cheese
2 onions mozzarella
1 ham
1 ham
2 mushrooms onions
2 tomatoes cheddar
2 pineapple neapolitan-crust
9 mushrooms tomatoes onions neapolitan-crust basil ham emmental-cheese mozzarella cheddar
5 mushrooms pineapple ham basil emmental-cheese
1 mozzarella
2 tomatoes cheddar
1 basil
5 mushrooms onions ham neapolitan-crust mozzarella
1 ham
2 onions neapolitan-crust
3 mushrooms basil emmental-cheese
2 mozzarella cheddar
1 emmental-cheese
1 ham
2 emmental-cheese mozzarella
4 mushrooms tomatoes basil emmental-cheese
4 mushrooms basil emmental-cheese cheddar
1 cheddar
1 basil
6 tomatoes onions pineapple basil mozzarella cheddar
3 neapolitan-crust emmental-cheese cheddar
2 neapolitan-crust emmental-cheese
1 cheddar
1 basil
2 mozzarella cheddar
2 tomatoes ham
3 onions neapolitan-crust mozzarella
6 mushrooms tomatoes basil ham emmental-cheese cheddar
6 tomatoes ham neapolitan-crust emmental-cheese mozzarella cheddar
1 mushrooms
1 ham
2 mushrooms emmental-cheese
1 pineapple
2 mushrooms onions
2 onions mozzarella
2 pineapple cheddar
2 emmental-cheese cheddar
1 ham
1 basil
1 basil
1 onions
7 mushrooms tomatoes onions pineapple neapolitan-crust basil ham
1 emmental-cheese
1 cheddar
3 mushrooms neapolitan-crust ham
3 basil mozzarella cheddar
3 mushrooms tomatoes emmental-cheese
2 mushrooms neapolitan-crust
10 mushrooms tomatoes onions pineapple neapolitan-crust basil ham emmental-cheese mozzarella cheddar
1 tomatoes
2 tomatoes onions
1 basil
10 mushrooms tomatoes onions pineapple neapolitan-crust ham basil emmental-cheese mozzarella cheddar
1 cheddar
3 onions neapolitan-crust basil""".split('\n')

import sys
if len(sys.argv) > 1:
    inputs=open(sys.argv[1]).read().split('\n')

nb_pizzas, nb_team2, nb_team3, nb_team4 = map(int,inputs[0].strip().split())
pizzas = []
for i in range(1,nb_pizzas+1):
    pizzas += [set(inputs[i].split()[1:])]
print(nb_pizzas,nb_team2,nb_team3,nb_team4)
print(pizzas)

P = range(nb_pizzas)

## -- mip part

from mip import Model, xsum, maximize, BINARY

m = Model('even_more_pizza')

T2 = range(nb_team2)
T3 = range(nb_team3)
T4 = range(nb_team4)

# whether a pizza is in one of the teams of 2, or 3, or 4
inTeam2 = dict([((p,t2),m.add_var(var_type=BINARY)) for p in P for t2 in T2])
inTeam3 = dict([((p,t3),m.add_var(var_type=BINARY)) for p in P for t3 in T3])
inTeam4 = dict([((p,t4),m.add_var(var_type=BINARY)) for p in P for t4 in T4])

# each pizza can only be in one of the teams
for p in P:
    m += xsum(inTeam2[(p,t2)] for t2 in T2) + xsum(inTeam3[(p,t3)] for t3 in T3)  + xsum(inTeam4[(p,t4)] for t4 in T4) <= 1

# determine if a team has been served at least one pizza
servedTeam2 = dict([(t2,m.add_var(var_type=BINARY)) for t2 in T2])
servedTeam3 = dict([(t3,m.add_var(var_type=BINARY)) for t3 in T3])
servedTeam4 = dict([(t4,m.add_var(var_type=BINARY)) for t4 in T4])

# precisely limit of how many pizzas there can be per teams (either all the people in the team has one, or none has)
for t2 in T2:
    for p in P:
        m += servedTeam2[t2] >= inTeam2[(p,t2)]
    m += xsum(inTeam2[(p,t2)] for p in P) == 2*servedTeam2[t2]
for t3 in T3:
    for p in P:
        m += servedTeam3[t3] >= inTeam3[(p,t3)]
    m += xsum(inTeam3[(p,t3)] for p in P) == 3*servedTeam3[t3]
for t4 in T4:
    for p in P:
        m += servedTeam4[t4] >= inTeam4[(p,t4)]
    m += xsum(inTeam4[(p,t4)] for p in P) == 4*servedTeam4[t4]

# computer set of all ingredients
I = set([i for p in P for i in pizzas[p]])

# for each team, determine which ingredients it has
Iteam2 = dict([((t2,i),m.add_var(var_type=BINARY)) for t2 in T2 for i in I])
Iteam3 = dict([((t3,i),m.add_var(var_type=BINARY)) for t3 in T3 for i in I])
Iteam4 = dict([((t4,i),m.add_var(var_type=BINARY)) for t4 in T4 for i in I])
for i in I:
    for t2 in T2:
        for p in P:
            if i in pizzas[p]:
                m += Iteam2[(t2,i)] >= inTeam2[(p,t2)]
        m += Iteam2[(t2,i)] <= xsum(inTeam2[(p,t2)] for p in P if i in pizzas[p])
    for t3 in T3:
        for p in P:
            if i in pizzas[p]:
                m += Iteam3[(t3,i)] >= inTeam3[(p,t3)]
        m += Iteam3[(t3,i)] <= xsum(inTeam3[(p,t3)] for p in P if i in pizzas[p])
    for t4 in T4:
        for p in P:
            if i in pizzas[p]:
                m += Iteam4[(t4,i)] >= inTeam4[(p,t4)]
        m += Iteam4[(t4,i)] <= xsum(inTeam4[(p,t4)] for p in P if i in pizzas[p])


# a linearization trick to permit quadratic scoring
# (otherwise would only be able to maximize a linear sum of variables)
K=range(1,100)
Steam2 = dict([((t2,k),m.add_var(var_type=BINARY)) for t2 in T2 for k in K])
Steam3 = dict([((t3,k),m.add_var(var_type=BINARY)) for t3 in T3 for k in K])
Steam4 = dict([((t4,k),m.add_var(var_type=BINARY)) for t4 in T4 for k in K])
for t2 in T2:
    m += xsum(  Steam2[(t2,k)] for k in K) <= 1
    m += xsum(k*Steam2[(t2,k)] for k in K) == xsum(Iteam2[(t2,i)] for i in I)
for t3 in T3:
    m += xsum(  Steam3[(t3,k)] for k in K) <= 1
    m += xsum(k*Steam3[(t3,k)] for k in K) == xsum(Iteam3[(t3,i)] for i in I)
for t4 in T4:
    m += xsum(  Steam4[(t4,k)] for k in K) <= 1
    m += xsum(k*Steam4[(t4,k)] for k in K) == xsum(Iteam4[(t4,i)] for i in I)

m.objective = maximize(xsum(k*k*Steam2[(t2,k)] for t2 in T2 for k in K) +\
                       xsum(k*k*Steam3[(t3,k)] for t3 in T3 for k in K) +\
                       xsum(k*k*Steam4[(t4,k)] for t4 in T4 for k in K))

m.optimize()

selected = sorted([(p,t2) for t2 in T2 for p in P if inTeam2[(p,t2)].x >= 0.99] + \
                  [(p,t3) for t3 in T3 for p in P if inTeam3[(p,t3)].x >= 0.99] + \
                  [(p,t4) for t4 in T4 for p in P if inTeam4[(p,t4)].x >= 0.99])

import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    
eprint("solution found at value:",m.objective_value)
eprint('selected types: {}'.format(selected))

if len(sys.argv) > 1:
    sol = open(sys.argv[1]+".sol","w")
else:
    sol = open("solution.txt","w")
def printsol(s):
    sol.write(str(s)+"\n")

printsol(len(selected))
printsol(' '.join(map(str,selected)))

sol.close()

from collections import defaultdict
def display(n,l):
    print("teams of",n,"will get",l)
    teams=defaultdict(set)
    for p,t in l:
        teams[t] |= pizzas[p]
    print(teams)

display(2,[(p,t2) for t2 in T2 for p in P if inTeam2[(p,t2)].x >= 0.99])
display(3,[(p,t3) for t3 in T3 for p in P if inTeam3[(p,t3)].x >= 0.99])
display(4,[(p,t4) for t4 in T4 for p in P if inTeam4[(p,t4)].x >= 0.99])
