import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import numpy as np

# ==========================
# 1️⃣ Charger les données
# ==========================
df = pd.read_csv('fact_sales.csv')
# print(df.head())

# ==========================
# 2️⃣ Normalisation
# ==========================
X = df[['price', 'shipping_charges', 'sales_amount']].values
X_scaled = StandardScaler().fit_transform(X)
# print(X_scaled[:5])

# Création classes réelles (pédagogique)
df['real_class'] = df['sales_amount'].apply(lambda x: 1 if x >= 2000 else 0)

# ==========================
# 3️⃣ Graphe k-distance pour choisir eps
# ==========================
min_samples = 4
neighbors = NearestNeighbors(n_neighbors=min_samples)
neighbors_fit = neighbors.fit(X_scaled)
distances, _ = neighbors_fit.kneighbors(X_scaled)
distances = sorted(distances[:, min_samples-1])

plt.figure(figsize=(8,5))
plt.plot(distances)
plt.xlabel('Points triés')
plt.ylabel(f'Distance au {min_samples}-ème voisin')
plt.title('Graphe k-distance')
plt.show()

# ==========================
# 4️⃣ DBSCAN
# ==========================
eps = 0.35
db = DBSCAN(eps=eps, min_samples=min_samples)
df['cluster'] = db.fit_predict(X_scaled)

# ==========================
# 5️⃣ Visualisation 2D avec outliers jaunes
# ==========================
colors_for_plot = df['cluster'].astype(float).values
colors_for_plot[colors_for_plot == -1] = np.nan  # NaN pour clusters

plt.figure(figsize=(8,6))
plt.scatter(X_scaled[:,0], X_scaled[:,1], c=colors_for_plot, cmap='rainbow', s=50)
# Outliers en jaune
plt.scatter(X_scaled[df['cluster']==-1,0], X_scaled[df['cluster']==-1,1],
            color='yellow', label='Outliers', s=50, edgecolor='black')

plt.xlabel('Price (normalisé)')
plt.ylabel('Shipping Charges (normalisé)')
plt.title('Clusters DBSCAN 2D avec points isolés en jaune')
plt.legend()
plt.show()

# ==========================
# 6️⃣ Visualisation 3D avec outliers jaunes
# ==========================
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

normal_mask = df['cluster'] != -1
ax.scatter(X_scaled[normal_mask,0], X_scaled[normal_mask,1], X_scaled[normal_mask,2],
           c=df['cluster'][normal_mask], cmap='rainbow', s=50)

outlier_mask = df['cluster'] == -1
ax.scatter(X_scaled[outlier_mask,0], X_scaled[outlier_mask,1], X_scaled[outlier_mask,2],
           color='yellow', s=50, edgecolor='black', label='Outliers')

ax.set_xlabel('Price')
ax.set_ylabel('Shipping Charges')
ax.set_zlabel('Sales Amount')
plt.title('Clusters DBSCAN 3D avec points isolés en jaune')
ax.legend()
plt.show()

# ==========================
# 7️⃣ Résultat clusters et points bruit
# ==========================
n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
n_noise = list(db.labels_).count(-1)
print(df.head())
print(f"Clusters trouvés: {n_clusters}, Points bruit: {n_noise}")

# ==========================
# 8️⃣ Analyse des clusters
# ==========================
print(df.groupby('cluster')[['price','shipping_charges','sales_amount']].mean())
score = silhouette_score(X_scaled, db.labels_)
print("Silhouette Score :", score)
db_index = davies_bouldin_score(X_scaled, db.labels_)
print("Davies-Bouldin Index :", db_index)

# ========================== 
# 9️⃣ MATRICE DE CONFUSION & METRICS REALISTES
# ==========================

# Q3 comme seuil High Sales
threshold = df['sales_amount'].quantile(0.75)
df['real_class'] = df['sales_amount'].apply(lambda x: 1 if x >= threshold else 0)
print("Seuil High Sales (Q3) :", threshold)
print("Distribution des classes réelles :\n", df['real_class'].value_counts())

# DBSCAN pour matrice confusion (réutiliser eps)
df['cluster'] = db.fit_predict(X_scaled)

# Calcul moyenne de sales_amount par cluster
cluster_sales_mean = df.groupby('cluster')['sales_amount'].mean()
print("\nMoyenne de sales_amount par cluster :\n", cluster_sales_mean)

# Identifier clusters High Sales : toutes les moyennes >= seuil Q3
high_sales_clusters = cluster_sales_mean[cluster_sales_mean >= threshold].index.tolist()
print("\nClusters identifiés comme High Sales :", high_sales_clusters)

# Mapping cluster -> predicted_class
df['predicted_class'] = df['cluster'].apply(lambda x: 1 if x in high_sales_clusters else 0)

# Matrice de confusion et métriques
y_true = df['real_class']
y_pred = df['predicted_class']

cm = confusion_matrix(y_true, y_pred)
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)

print("\nMatrice de confusion :")
print(cm)
print("Accuracy :", accuracy)
print("Precision :", precision)

# Diagramme matrice de confusion
plt.figure(figsize=(6,5))
plt.imshow(cm, cmap='Blues')
plt.colorbar()
plt.xticks([0, 1], ['Low Sales', 'High Sales'])
plt.yticks([0, 1], ['Low Sales', 'High Sales'])

for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i, j], ha='center', va='center', color='black')

plt.xlabel('Classe prédite')
plt.ylabel('Classe réelle')
plt.title('Matrice de confusion (DBSCAN – dataset complet)')
plt.show()
