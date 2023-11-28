from math import sqrt

# Flags for special cases of node types
UNDEFINED = 0
NOISE = -1

def dbscan(points: list, eps: float, min_neighbours: int, dist_function: str = "euclidean") -> list:
    """
    Function for doing the DBSCAN clustering algorithm on a list of points
    
    Parameters
    ----------
    points : list[float, float]
        List of Nd points to cluster
    eps : float
        The distance in which points will be considered neighbours
    min_neighbours : int
        How many points should be within eps to create a cluster
    dist_function : str, optional = 'euclidean'
        The distance function to use, defaults (and only option) is euclidean

    Returns
    -------
    labels : list[int]
        Labels of the points, -1 indicates outlier points that dont belong to a cluster
    
    Examples
    --------
    >>> points = random.uniform(-10, 10, (N, 2))
    >>> labels = dbscan(points.tolist(), eps = 1.5, min_neighbours = 3, dist_function = "eucliean")

    Notes
    -----
    Implemented from the pseudocode in: "https://en.wikipedia.org/wiki/DBSCAN"
    """
    C = 0           # Number of clusters
    N = len(points)

    labels = [UNDEFINED] * N

    for p in range(N):
        # Point has already been clustered
        if labels[p] != UNDEFINED:
            continue

        # Find neighbours, if the density is too low mark as outlier
        neighbour_idx = find_neighbours(points, p, eps, dist_function = dist_function)
        if len(neighbour_idx) < min_neighbours:
            labels[p] = NOISE
            continue

        # Start new cluster and consider the starting points neighbours
        C += 1
        labels[p] = C
        while neighbour_idx:
            q = neighbour_idx.pop()
            if q == p:
                continue
            
            # Add noise points to the cluster and skip points that belong to another cluster
            if labels[q] == NOISE:
                labels[q] = C
            if labels[q] != UNDEFINED:
                continue

            # Add previously new points to the search area
            labels[q] = C
            neighbours_q = find_neighbours(points, q, eps, dist_function = dist_function)

            # Add new neighbors if the density is high enough
            if min_neighbours <= len(neighbours_q):
                neighbour_idx = neighbour_idx.union(neighbours_q)
    
    return labels


def euclidean_distance(p, q) -> float:
    return sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)


def find_neighbours(points: list, p: int, eps: float, dist_function: str = "eucliean"):
    """ Function for finding all points with eps distance of point. Only 'euclidean' distance implemented. """
    if dist_function == "eucliean":
        return set([q for q in range(len(points)) if euclidean_distance(points[p], points[q]) < eps])
    else:
        raise NotImplementedError(f"The distance function {dist_function} isnt implemented")


# Example usage
if __name__ == "__main__":
    N = 100

    from numpy import random

    points = random.uniform(-10, 10, (N, 2))
    labels = dbscan(points.tolist(), eps = 1.5, min_neighbours = 3, dist_function = "eucliean")

    print(labels)