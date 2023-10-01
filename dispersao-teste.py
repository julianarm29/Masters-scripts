import pandas as pd
import matplotlib.pyplot as plt

# Ler os dados do arquivo Excel (substitua 'seuarquivo.xlsx' pelo caminho do seu arquivo)
inp = input('Aba: ')
afq = input('Atributo físico-químico: ')
df = pd.read_excel('dispersao.xlsx', sheet_name = inp)

# Crie um gráfico de dispersão para cada coluna (grupo)
for column in df.columns:
    plt.scatter(range(len(df)), df[column], label=column)

# Adicione rótulos aos eixos e uma legenda
plt.xlabel('Índice dos peptídeos', fontsize = 14)
plt.ylabel('Valores', fontsize = 14)
plt.title(f'{afq}', fontsize=16)
plt.legend()

# Exiba o gráfico de dispersão
plt.show()
