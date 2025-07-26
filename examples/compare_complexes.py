import numpy as np
from vrcomplex import VietorisRipsComplex
from alphacomplex import AlphaComplex

# Simple 4-point square
points = np.array([
    [0, 0],    # Point 0
    [1, 0],    # Point 1  
    [1, 1],    # Point 2
    [0, 1]     # Point 3
])

epsilon = 1.5  # Distance threshold
alpha = 1.5    # Alpha threshold

# Create both complexes
vr_complex = VietorisRipsComplex(points, epsilon)
alpha_complex = AlphaComplex(points, alpha)

print("=== INPUT POINTS ===")
for i, point in enumerate(points):
    print(f"Point {i}: {point}")

print(f"\n=== VIETORIS-RIPS COMPLEX (ε={epsilon}) ===")
print("Simplices:", sorted(vr_complex.simplices))
print("Number of simplices:", len(vr_complex.simplices))

print(f"\n=== ALPHA COMPLEX (α={alpha}) ===") 
print("Simplices:", sorted(alpha_complex.simplices))
print("Number of simplices:", len(alpha_complex.simplices))

print("\n=== COMPARISON ===")
vr_set = set(vr_complex.simplices)
alpha_set = set(alpha_complex.simplices)

print("Common simplices:", sorted(vr_set & alpha_set))
print("Only in VR:", sorted(vr_set - alpha_set))
print("Only in Alpha:", sorted(alpha_set - vr_set))
