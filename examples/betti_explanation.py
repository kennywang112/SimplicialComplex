import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from abssimcomplex import SimplicialComplex

# Your example
e1 = [(0, 1), (1, 2), (2, 0)]
sc1 = SimplicialComplex(e1)

print("=== INPUT SIMPLICES ===")
print("Given simplices:", e1)
print("All simplices (after adding faces):", sorted(sc1.simplices))
print("Face set:", sorted(sc1.face_set))

print("\n=== FACES BY DIMENSION ===")
print("0-faces (vertices):", sc1.n_faces(0))
print("1-faces (edges):", sc1.n_faces(1))
print("2-faces (triangles):", sc1.n_faces(2))

print("\n=== BETTI NUMBERS ===")
print("β₀ (connected components):", sc1.betti_number(0))
print("β₁ (1D holes/loops):", sc1.betti_number(1))
print("β₂ (2D holes/cavities):", sc1.betti_number(2))

print("\n=== WHAT THIS REPRESENTS ===")
print("This is a TRIANGLE BOUNDARY (3 edges forming a loop)")
print("- It's a 1-dimensional structure (graph/cycle)")
print("- NOT a filled triangle (that would include the 2-face)")

print("\n=== TOPOLOGICAL INTERPRETATION ===")
print("β₀ = 1: One connected component (all vertices connected)")
print("β₁ = 1: One loop (the triangle cycle: 0→1→2→0)")
print("β₂ = 0: No 2D cavities (it's just the boundary, not filled)")

print("\n=== COMPARISON: If it were a FILLED triangle ===")
filled_triangle = [(0, 1), (1, 2), (2, 0), (0, 1, 2)]
sc_filled = SimplicialComplex(filled_triangle)
print("Filled triangle simplices:", sorted(sc_filled.simplices))
print("Filled triangle β₁:", sc_filled.betti_number(1), "(no loop - it's filled!)")

print("\n=== VISUALIZING THE DIFFERENCE ===")
print("Your example (e1):     ○-----○")
print("                       |     |  ")  
print("                       |     |  ")
print("                       ○-----○  <- Just the edges (loop)")
print()
print("Filled triangle:       ○-----○")
print("                       |\\   /|  ")
print("                       | \\ / |  ") 
print("                       |  ○  |  <- Includes the interior")
print("                       ○-----○")
