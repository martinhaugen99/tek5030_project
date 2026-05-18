import pybullet as p

#input_mesh = "pointcloud.obj"
#output_mesh = "pointcloud_thick.obj"
input_mesh = "room.obj"
output_mesh = "room_thick.obj"
log_file = "log.txt" # Good for debugging if it fails

# Connect to a physics server (required for some internal PyBullet functions)
p.connect(p.DIRECT) 

p.vhacd(
    input_mesh, 
    output_mesh, 
    log_file,
    resolution=5000, #500000
    concavity=0.001,
    alpha=0.04
)
p.disconnect()