
from itertools import combinations
import warnings

import numpy as np
from scipy.sparse import dok_matrix
from scipy.sparse.linalg import aslinearoperator
from scipy.linalg.interpolative import estimate_rank
import networkx as nx
import matplotlib.pyplot as plt

from utils import faces


class SimplicialComplex:
    def __init__(self, simplices=[]):
        self.import_simplices(simplices=simplices)

    def import_simplices(self, simplices=[]):
        # self.simplices = list(map(lambda simplex: tuple(sorted(simplex)), simplices))
        self.simplices = [tuple(sorted(simplex)) for simplex in simplices]
        self.face_set = faces(self.simplices)

    def n_faces(self, n):
        # return list(filter(lambda face: len(face) == n + 1, self.face_set))
        return [face for face in self.face_set if len(face) == n+1]

    # get the lower dimension faces of a simplex
    # so we get k-1 faces from k faces
    # for example a triangle (2-face) has 3 edges (1-faces) and 3 vertices (0-faces)
    # Boundary operator is used to calculate betti numbers
    def boundary_operator(self, i):
        source_simplices = self.n_faces(i)
        target_simplices = self.n_faces(i - 1)

        if len(target_simplices) == 0:
            # Dictionary of Keys matrix
            S = dok_matrix((1, len(source_simplices)), dtype=np.float64)
            # S = [1 1 1 1 ]
            S[0, 0:len(source_simplices)] = 1
        else:
            # 增加索引:
            source_simplices_dict = {
                source_simplices[j]: j for j in range(len(source_simplices))
            }
            target_simplices_dict = {
                target_simplices[i]: i for i in range(len(target_simplices))
            }
            # 建立k維simplex到k-1維simplex的boundary矩陣
            S = dok_matrix(
                (len(target_simplices), len(source_simplices)), dtype=np.float64
            )
            for source_simplex in source_simplices:
                for a in range(len(source_simplex)):
                    target_simplex = source_simplex[:a] + source_simplex[(a + 1) :]
                    i = target_simplices_dict[target_simplex]
                    j = source_simplices_dict[source_simplex]
                    S[i, j] = -1 if a % 2 == 1 else 1  # S[i, j] = (-1)**a
        return S

    def betti_number(self, i, eps=None):
        # i: dimension of the simplices
        boundop_i = self.boundary_operator(i)
        boundop_ip1 = self.boundary_operator(i + 1)

        if i == 0:
            boundop_i_rank = 0
        else:
            if eps is None:
                try:
                    # Use exact rank calculation
                    boundop_i_rank = np.linalg.matrix_rank(boundop_i.toarray())
                except (np.linalg.LinAlgError, ValueError):
                    boundop_i_rank = boundop_i.shape[1]
            else:
                # estimate the rank of matrix without computing the full SVD
                # calculate the rank of the boundary operator because the image dimension is the rank of the matrix
                boundop_i_rank = estimate_rank(aslinearoperator(boundop_i), eps)

        if eps is None:
            try:
                boundop_ip1_rank = np.linalg.matrix_rank(boundop_ip1.toarray())
            except (np.linalg.LinAlgError, ValueError):
                boundop_ip1_rank = boundop_ip1.shape[1]
        else:
            boundop_ip1_rank = estimate_rank(aslinearoperator(boundop_ip1), eps)

        return (boundop_i.shape[1] - boundop_i_rank) - boundop_ip1_rank

    def euler_characteristics(self):
        # χ = Σ (-1)^k * β_k
        # χ = 2: Sphere-like surfaces
        # χ = 1: Disk-like spaces
        # χ = 0: Torus-like or circle-like spaces
        # χ < 0: Surfaces with multiple handles
        max_n = max(map(len, self.simplices))
        return sum(
            [(-1 if a % 2 == 1 else 1) * self.betti_number(a) for a in range(max_n)]
        )

    def generate_graph(self, simplices=None):
        """ Generate edges and vertices in sets """
        if len(self.simplices) == 0 and simplices is None:
            raise Exception("No simplices to create a graph from. Please specify one.")
        elif simplices is not None:
            self.import_simplices(simplices=simplices)

        vertices = set()
        edges = set()

        for simplex in self.simplices:
            for vertex1, vertex2 in combinations(simplex, 2):
                vertices.add(vertex1)
                vertices.add(vertex2)
                edges.add(tuple(sorted([vertex1, vertex2])))
        return vertices, edges

    def draw(self, vertex_labels=True, edge_labels=False):
        """ Draw the Simplicial Complex """
        vertices, edges = self.generate_graph()

        if len(vertices) + len(edges) > 1000:
            warnings.warn(
                "The number of elements to draw exceeds 100. To still draw the plot, call the function with override_100_limit = True. "
            )
        else:
            G = nx.Graph()
            for vertex in vertices:
                G.add_node(vertex)
            for edge in edges:
                G.add_edge(edge[0], edge[1])
            pos = nx.spring_layout(G)

            nx.draw(G, pos)

            labels = {}
            if vertex_labels is True:
                for vertex in vertices:
                    labels[vertex] = str(vertex)
            nx.draw_networkx_labels(G, pos, labels, font_size=16)

            if edge_labels is True:
                edge_labels = {}
                for edge in edges:
                    edge_labels[edge] = "{}:{}".format(edge[0], edge[1])
                nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=3)
            plt.plot()
