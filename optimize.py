from pulp import *
import pandas as pd

investimento_total = 1e6
cpi_list = [1.75, 1.50, 0.75, 2.20, 3, 5]

# instanciando um problema de otimização
prob = LpProblem("LP", LpMaximize)
# prob = LpProblem("LP", LpMinimize)

# definindo a lista de variáveis
variable_list = [LpVariable(f"C{i+1}") for i in range(len(cpi_list))]

# definindo a função a ser otimizada
prob += lpSum([variable_list[i] * (1 / cpi_list[i]) for i in range(len(cpi_list))])

# definindo as restrições
for variable in variable_list:
    prob += variable >= 0.05 * investimento_total
    prob += variable <= 0.3 * investimento_total

prob += lpSum([variable_list[i] for i in range(len(cpi_list))]) <= investimento_total

# otimizando o problema
prob.solve()
print(f"Status do problema: {LpStatus[prob.status]}.")

# mostrando os resultados
channels = []
values = []
for variable in prob.variables():
    print(f"{variable.name} = R$ {variable.varValue:.2f}")
    channels.append(variable.name)
    values.append(variable.varValue)

print(f"Total de Clientes = {value(prob.objective):.0f}")
print(f"Custo por Impressão Efetivo = R$ {investimento_total / value(prob.objective):.2f}")

results_df = pd.DataFrame(data={
    "channels": channels,
    "values": values
})

