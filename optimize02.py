# https://www.youtube.com/watch?v=0EY78yg_SLs&ab_channel=HashtagTreinamentos
from pulp import *
import pandas as pd

# INPUTS DO PROBLEMA
# fornecer a lista de variáveis em ordem alfabética
variaveis = ["arroz", "carne", "frango", "milho"]
preco_kg  = [2, 12, 20, 2.5]

# INSTANCIANDO UM PROBLEMA DE OTIMIZAÇÃO
prob = LpProblem("LP", LpMinimize)

# DEFININDO AS VARIÁVEIS PARA O PROBLEMA DE OTIMIZAÇÃO
pulp_variables = [LpVariable(f"{variavel}") for variavel in variaveis]

# DEFININDO A FUNÇÃO A SER OTIMIZADA
prob += lpSum([pulp_variables[i] * preco_kg[i] for i in range(len(pulp_variables))])

# DEFININDO AS RESTRIÇÕES
# arroz
prob += pulp_variables[0] >= 25
prob += pulp_variables[0] <= 50

# carne
prob += pulp_variables[1] >= 20
prob += pulp_variables[1] <= 35

# frango
prob += pulp_variables[2] >= 15
prob += pulp_variables[2] <= 30

# milho
prob += pulp_variables[3] >= 30
prob += pulp_variables[3] <= 55

# a soma das quantidades dos ingredientes compradas deve ser igual a 150kg
prob += lpSum([pulp_variables[i] for i in range(len(pulp_variables))]) == 150

# OTIMIZANDO A FUNÇÃO DADA AS RESTRIÇÕES
prob.solve()

# APRESENTANDO OS RESULTADOS
ingredientes = []
quantidades  = []
for v in prob.variables():
    print(f"{v.name} = {v.varValue:.0f}")
    ingredientes.append(v.name)
    quantidades.append(v.varValue)

results_df = (  
    pd.DataFrame(data={
        "ingrediente": ingredientes,
        "quantidade": quantidades
    })
    .assign(preco_kg = preco_kg)
    .assign(custo = lambda df: df['quantidade'] * df['preco_kg'])
)

print(f"Custo Total Otimizado = R$ {value(prob.objective):.2f}")



