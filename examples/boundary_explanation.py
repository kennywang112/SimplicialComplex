from abssimcomplex import SimplicialComplex
import numpy as np

# Create a simple triangle simplicial complex
# Triangle with vertices 1, 2, 3
triangle_simplices = [(1, 2, 3), (1, 2), (2, 3), (1, 3), (1,), (2,), (3,)]
sc = SimplicialComplex(triangle_simplices)

print("=== SIMPLICIAL COMPLEX: Triangle ===")
print("All simplices:", sorted(sc.simplices))
print("Face set:", sorted(sc.face_set))

print("\n=== FACES BY DIMENSION ===")
print("0-faces (vertices):", sc.n_faces(0))
print("1-faces (edges):", sc.n_faces(1)) 
print("2-faces (triangles):", sc.n_faces(2))

print("\n=== BOUNDARY OPERATORS ===")

# Boundary operator ∂₁: edges → vertices
print("\n--- ∂₁: 1-faces → 0-faces (edges → vertices) ---")
boundary_1 = sc.boundary_operator(1)
print("Matrix shape:", boundary_1.shape)
print("Matrix (dense form):")
print(boundary_1.toarray())

print("\nInterpretation:")
edges = sc.n_faces(1)
vertices = sc.n_faces(0)
print("Columns (source - edges):", edges)
print("Rows (target - vertices):", vertices)

# Boundary operator ∂₂: triangles → edges  
print("\n--- ∂₂: 2-faces → 1-faces (triangles → edges) ---")
boundary_2 = sc.boundary_operator(2)
print("Matrix shape:", boundary_2.shape)
print("Matrix (dense form):")
print(boundary_2.toarray())

print("\nInterpretation:")
triangles = sc.n_faces(2)
edges = sc.n_faces(1)
print("Columns (source - triangles):", triangles)
print("Rows (target - edges):", edges)

# Boundary operator ∂₀: vertices → empty (special case)
print("\n--- ∂₀: 0-faces → (-1)-faces (vertices → empty) ---")
boundary_0 = sc.boundary_operator(0)
print("Matrix shape:", boundary_0.shape)
print("Matrix (dense form):")
print(boundary_0.toarray())

print("\nInterpretation:")
print("This is the special case where target_simplices is empty")
print("All vertices map to the 'empty boundary'")

print("\n=== MANUAL VERIFICATION FOR ∂₁ ===")
print("For edge (1,2): boundary should be vertex 2 - vertex 1")
print("For edge (1,3): boundary should be vertex 3 - vertex 1") 
print("For edge (2,3): boundary should be vertex 3 - vertex 2")
print("The ±1 pattern comes from the alternating sum formula: ∂(v₀,v₁) = v₁ - v₀")
