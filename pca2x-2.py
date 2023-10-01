import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import os
import argparse
import sys

# Parse
parser = argparse.ArgumentParser(description='2D plot/PCA/kmeans clustering')
parser.add_argument("-f", '--file', help="file_name.csv", action="store")
parser.add_argument("-o", '--output', help="file name", action="store")
parser.add_argument("-cl", '--n_clusters', help="file name", action="store")
args = parser.parse_args()

# Dataframe
df1 = pd.read_csv(args.file)
del df1["Unnamed: 0"]
name = df1['Name']
df1.drop(['Amidated_Mass','[M+H+]','Name', 'Peptides'], axis=1, inplace=True)
cols = df1.columns.tolist()
cols = cols[-1:] + cols[:-1]
df1 = df1[cols]
df1.set_index(name, inplace=True) 

#PCA
# Escalar os dados
scaling=StandardScaler()
 
# Usar fit e transformar
scaling.fit(df1)
Scaled_data=scaling.transform(df1)
 
# Setar n_components
principal=PCA(n_components=2)
principal.fit(Scaled_data)
df=principal.transform(Scaled_data)

# KMeans
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=int(args.n_clusters), random_state=0)
previsoes = kmeans.fit_predict(df)

# Adicionar as coordenadas das centroides
centroids = kmeans.cluster_centers_
df1['Clusters'] = previsoes
df1.to_csv(args.output + '.csv')

# Scatter plot dos dados
scatter = plt.scatter(df[:, 0], df[:, 1],
                      s=100,
                      c=df1['Clusters'],
                      cmap='rainbow',
                      linestyles='solid',
                      alpha=0.8,
                      linewidth=1,
                      edgecolor='black',
                      picker=True)

# Plot das centroides
plt.scatter(centroids[:, 0], centroids[:, 1], c='black', marker='o', s=100, label='Centroides')

# Adicionar uma legenda para as centroides
legend1 = plt.legend(*scatter.legend_elements(),
                    loc="lower left", title="Clusters")

# Calcular e exibir as variâncias das componentes principais
explained_variances = principal.explained_variance_
variance_labels = [f'{i + 1}: {variance:.2f}' for i, variance in enumerate(explained_variances)]

# Adicionar rótulos aos eixos x e y com variância
plt.xlabel(f"PCA 1 ({variance_labels[0]})", fontsize=12)
plt.ylabel(f"PCA 2 ({variance_labels[1]})", fontsize=12)

# Plotar
plt.show()

# Contribuição do PCA
labelstest = ['Volume','Resíduos Acídicos (%)','Resíduos Básicos (%)', 'Resíduos Carregados (%)', 'Momento Hidrofóbico', 'Hidrofobicidade', 'Ponto Isoelétrico', 'Massa Monoisotópica', 'Resíduos Não-Polares (%)', 'Resíduos Polares (%)', 'Resíduos Aromáticos (%)', 'Coeficiente de α-Hélice', 'Coeficiente de Folhas-β', 'Coeficiente de Voltas', 'Carga', 'Resíduos Enterrados (%)', 'Acessibilidade do Solvente à Cadeia Principal', 'Acessibilidade do Solvente a Resíduos Não-Polares', 'Acessibilidade do Solvente a Resíduos Polares']

loadings = principal.components_
num_pc = principal.n_features_
pc_list = ["PC"+str(i) for i in list(range(1, num_pc+1))]
loadings_df = pd.DataFrame.from_dict(dict(zip(pc_list, loadings)))
df1.drop(['Clusters'],axis=1,inplace=True)
loadings_df['Atributos físico-químicos'] = labelstest
loadings_df = loadings_df.set_index('Atributos físico-químicos')


# Matriz de correlação
ax = sns.heatmap(loadings_df, annot=True, cmap='Spectral')
plt.show()