import networkx as nx
import numpy as np
from scipy.spatial import distance
from itertools import combinations

from abssimcomplex import SimplicialComplex


def circumradius(points):
    points = np.array(points)
    n, d = points.shape
    
    if n == 1:
        return 0.0
    elif n == 2:
        return distance.euclidean(points[0], points[1]) / 2.0
    else:
        # For higher dimensions, use more complex circumradius calculation
        # This is a simplified version - in practice you'd want more robust geometry
        try:
            # Center of circumsphere is equidistant from all points
            A = points[1:] - points[0]
            b = 0.5 * np.sum(A**2, axis=1)
            center = points[0] + np.linalg.lstsq(A, b, rcond=None)[0]
            radius = distance.euclidean(center, points[0])
            return radius
        except np.linalg.LinAlgError:
            # Fallback: max pairwise distance / 2
            max_dist = max(distance.euclidean(p1, p2) 
                          for p1, p2 in combinations(points, 2))
            return max_dist / 2.0


class CechComplex(SimplicialComplex):
    def __init__(
            self,
            points,
            epsilon,
            labels=None,
            distfcn=distance.euclidean
    ):
        super(CechComplex, self).__init__()
        self.pts = points
        self.labels = (list(range(len(self.pts)))
                       if labels is None or len(labels) != len(self.pts)
                       else labels)
        self.epsilon = epsilon
        self.distfcn = distfcn
        
        # does not use a network, directly constructs simplices
        self.import_simplices(self.construct_simplices())

    def construct_simplices(self):
        simplices = []
        n = len(self.pts)
        
        # Add all individual points
        for i in range(n):
            simplices.append((self.labels[i],))
        
        # Check all possible subsets of points
        for size in range(2, n + 1):
            for indices in combinations(range(n), size):
                # Get the actual points
                subset_points = [self.pts[i] for i in indices]
                subset_labels = [self.labels[i] for i in indices]
                
                # Check if circumradius ≤ epsilon
                if circumradius(subset_points) <= self.epsilon:
                    simplices.append(tuple(sorted(subset_labels)))
        
        return simplices
