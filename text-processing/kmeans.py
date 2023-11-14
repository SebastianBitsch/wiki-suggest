import numpy as np

class KMeans:
    def __init__(self, n_clusters:int = 3, n_iterations:int = 10, init_method: str = 'forgy'):
        """
        A class for clustering a set of points into K different clusters based on their proximity

        Parameters
        ----------
        n_clusters, int (optional)
            The number of clusterings to make
        
        n_iterations, int (optional)
            The number of times to run the algorithm with different initializations before voting

        init_method, str
            The initialization method to init the cluster centers;
            choose between 'random' and 'forgy'
        """
        self.n_clusters = n_clusters
        self.n_iterations = n_iterations
        self.init_method = init_method


    def ensamble_cluster(self, points, n_runs: int, max_attempts: int = 100):
        """ 
        Do K-means clustering by ensamble voting. i.e. we run the Kmeans algorithm N times, each with
        random initialization. Each run of the clustering is a "vote" for every point having that 
        label. In the end we tally the votes and assign points based on what label got the most votes
        """
        labels_all_runs = []

        # Run the algorithm N times
        for _ in range(n_runs):
            labels = self._cluster_single_run(points, max_attempts)
            labels_all_runs.append(labels)
        
        # Vote on what the best label is for every point
        return self._ensamble_vote(labels_all_runs)


    def cluster(self, points, max_attempts: int = 100):
        """ Apply the KMeans clustering algorithm """
        best_labels = None
        best_centroids = None
        best_inertia = np.inf

        for _ in range(self.n_iterations):
            centroids = self._initialize_centroids(points)

            # Update
            for _ in range(max_attempts):
                # Assignment step
                labels = self._assign_clusters(points, centroids)

                # Update step
                new_centroids = self._update_centroids(points, labels)

                # Check termination rule
                if np.array_equal(centroids, new_centroids):
                    break
                else:
                    centroids = new_centroids

            # Update the best clustering if we have found a better one
            inertia = self.calculate_inertia(points, centroids, labels)
            if inertia < best_inertia:
                best_labels = labels
                best_centroids = centroids
                best_inertia = inertia

        return best_labels, best_centroids

    def calculate_inertia(self, data, centroids, labels):
        inertia = 0
        for k in range(self.n_clusters):
            cluster_data = data[labels == k]
            inertia += ((cluster_data - centroids[k]) ** 2).sum()
        return inertia
    
    def _ensamble_vote(self, labels_all_runs):
        """
        Given a list of N labels from k runs, return a list of the N labels that were most common
        for each element across k runs.
        Cheeky function shamelessly stolen from: https://stackoverflow.com/a/56050427
        """
        return np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=labels_all_runs)
    

    def _initialize_centroids(self, points):
        """
        Initialize the cluster centroids, there are multiple ways of doing this - we are just 
        using the simplest method; picking random points as the centroids
        """
        # TODO: Maybe try implementing other (smarter) methods (?)
        if self.init_method == 'forgy':
            # Pick K random points as the initial cluster centres
            indices = np.random.choice(points.shape[0], self.n_clusters, replace = False)
            return points[indices]
        else: 
            raise NotImplementedError("The given initialization method isnt implemented")


    def _assign_clusters(self, points, centroids):
        """ Assign points to their closest clusters"""
        distances = np.sqrt(((points - centroids[:, np.newaxis])**2).sum(axis=2))
        return np.argmin(distances, axis=0)


    def _update_centroids(self, points, labels):
        """ Update the positions of the centroids to be the mean of the points assigned to that closter """
        return np.array([points[labels == k].mean(axis=0) for k in range(self.n_clusters)])


# Example usage
if __name__ == "__main__":
    
    # Generate points
    points = np.random.uniform(-10, 10, (100, 2))

    # Cluster
    kmeans = KMeans(n_clusters = 5, n_iterations = 10)
    labels = kmeans.cluster(points, n_runs = 5)

    print(labels)

