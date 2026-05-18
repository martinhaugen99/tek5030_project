import open3d as o3d
import numpy as np

# Load point cloud
pcd = o3d.io.read_point_cloud("pointcloud.ply")

#define radius' for
pcd.estimate_normals()
distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 3 * avg_dist

# 3. Create Mesh
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
    pcd, o3d.utility.DoubleVector([radius, radius * 2])
)

o3d.io.write_triangle_mesh("pointcloud_high_res.obj", mesh)

print(f"Original triangles: {len(mesh.triangles)}")
mesh = mesh.simplify_quadric_decimation(target_number_of_triangles=50000)
print(f"New triangles: {len(mesh.triangles)}")
mesh.translate(-mesh.get_center())
print(mesh)

o3d.io.write_triangle_mesh("pointcloud.obj", mesh)
o3d.visualization.draw_geometries([mesh]) # visualize mesh