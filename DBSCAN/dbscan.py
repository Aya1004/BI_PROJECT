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
df = pd.read_csv('C:\\Users\\hp\\Desktop\\BI_PROJECT\\DBSCAN\\fact_sales.csv')
print(df.head())

#  Normalisation
X = df[['price', 'shipping_charges', 'sales_amount']].values
X_scaled = StandardScaler().fit_transform(X)
print(X_scaled[:5])


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
eps = 0.47
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
#print(df.groupby('cluster')[['price','shipping_charges','sales_amount']].mean())
score = silhouette_score(X_scaled, db.labels_)
print("Silhouette Score :", score)
db_index = davies_bouldin_score(X_scaled, db.labels_)
print("Davies-Bouldin Index :", db_index)
