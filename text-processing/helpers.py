import numpy as np
import matplotlib.pyplot as plt


def calculate_average_radius(points, labels, centroids):
    """
    Calculate the average radius of each cluster.
    See. Week 6 slide 34
    """
    n_clusters = len(centroids)
    average_radius = np.zeros(n_clusters)
    
    for i in range(n_clusters):
        
        # Get the distances from the points to their centroid
        cluster_points = points[labels == i]
        distances = np.sqrt(((cluster_points - centroids[i])**2).sum(axis=1).mean())
        
        average_radius[i] = distances
    
    return average_radius


def davies_bouldin_score(points, labels, centroids):
    """ Computes the Davies-Bouldin score of a cluster, see Week 6 slide 26 """
    k = len(centroids)
    score = 0

    r = calculate_average_radius(points, labels, centroids)

    for i in range(k):
        max_ratio = 0

        for j in range(k):
            if i == j:
                continue
            
            # Calculate the distance between centroids
            dist = np.linalg.norm(centroids[i] - centroids[j])

            # Get the max of the ratios
            max_ratio = max((r[i] + r[j]) / dist, max_ratio)
            
        score += max_ratio

    return score / k


## ------------ Plotting ------------

def scatter(points, centroids = None, colors = "red", title = "", figsize = (5,5)):
    plt.figure(figsize = figsize)
    plt.scatter(points[:,0], points[:,1], c=colors, cmap="Set1")
    if not centroids is None:
        plt.scatter(centroids[:,0], centroids[:,1], c='black', marker='x')
    
    plt.title(title)
    plt.show()