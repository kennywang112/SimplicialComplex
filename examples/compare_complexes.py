import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from vrcomplex import VietorisRipsComplex
from alphacomplex import AlphaComplex
from cechcomplex import CechComplex

# Simple 4-point square
points = np.array([
    [0, 0],    # Point 0
    [1, 0],    # Point 1  
    [1, 1],    # Point 2
    [0, 1]     # Point 3
])

epsilon = 1.5  # Distance threshold
alpha = 1.5    # Alpha threshold
cech = 0.5  # Cech threshold

# Create both complexes
vr_complex = VietorisRipsComplex(points, epsilon)
alpha_complex = AlphaComplex(points, alpha)
cech_complex = CechComplex(points, cech)

print("=== INPUT POINTS ===")
for i, point in enumerate(points):
    print(f"Point {i}: {point}")

print(f"\n=== VIETORIS-RIPS COMPLEX (ε={epsilon}) ===")
print("Simplices:", sorted(vr_complex.simplices))
print("Number of simplices:", len(vr_complex.simplices))

print(f"\n=== ALPHA COMPLEX (α={alpha}) ===") 
print("Simplices:", sorted(alpha_complex.simplices))
print("Number of simplices:", len(alpha_complex.simplices))

print(f"\n=== ČECH COMPLEX (c={cech}) ===")
print("Simplices:", sorted(cech_complex.simplices))
print("Number of simplices:", len(cech_complex.simplices))

print("\n=== COMPARISON ===")
vr_set = set(vr_complex.simplices)
alpha_set = set(alpha_complex.simplices)
cech_set = set(cech_complex.simplices)

print("Vietoris-Rips Set:", vr_set)
print("Alpha Set:", alpha_set)
print("Čech Set:", cech_set)
