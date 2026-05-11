import pybullet as p

# Define your file paths
input_mesh = "bowl.obj"
output_mesh = "bowl_convex.obj"
log_file = "log.txt"

# This command generates the decomposed mesh
p.vhacd(input_mesh, output_mesh, "")