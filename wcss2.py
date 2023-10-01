import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Arquivo
csv_path = input("Arquivo: ")
data = pd.read_csv(csv_path)
numeric_columns = data.columns[:-2]

# Normalizar os dados
normalized_data = (data[numeric_columns] - data[numeric_columns].mean()) / data[numeric_columns].std()
normalized_data_array = normalized_data.values

# Calcular o WCSS
wcss_values = []
max_clusters = 10  # Defina o número máximo de clusters que você deseja testar

for n_clusters in range(1, max_clusters+1):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(normalized_data_array)
    wcss_values.append(kmeans.inertia_)

# Calcular as distâncias entre os pontos em relação à posição do ponto anterior no eixo y
distances = []
for i in range(1, len(wcss_values)):
    distance = abs(wcss_values[i] - wcss_values[i-1])
    distances.append(distance)

# Plotar o gráfico do WCSS 
import matplotlib.pyplot as plt

plt.plot(range(1, max_clusters+1), wcss_values, marker='o')
plt.xlabel('Número de clusters')
plt.ylabel('WCSS')
plt.title('WCSS versus número de clusters')

# Plotar as distâncias nas linhas do gráfico
for i, distance in enumerate(distances):
    plt.annotate(f'{distance:.2f}', xy=(i+1, wcss_values[i]), xytext=(i+1, wcss_values[i]+0.1), color='blue')

plt.show()
