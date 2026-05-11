import pybullet as p
import pybullet_data
import time

# Start the simulation
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# 0. Load a floor (Optional but recommended)
p.loadURDF("plane.urdf")

# 1. Create the Bowl
# Note: Ensure bowl_convex.obj was created via p.vhacd() previously
collision_id = p.createCollisionShape(p.GEOM_MESH, fileName="bowl_convex.obj")
visual_id = p.createVisualShape(p.GEOM_MESH, fileName="bowl.obj") 

bowl_body = p.createMultiBody(
    baseMass=0, # Changed to 0 so the bowl stays stationary on the floor
    baseCollisionShapeIndex=collision_id,
    baseVisualShapeIndex=visual_id,
    basePosition=[0, 0, 0]
)

# 2. Create the Ball
ball_collision = p.createCollisionShape(p.GEOM_SPHERE, radius=0.1)
ball_id = p.createMultiBody(
    baseMass=1, 
    baseCollisionShapeIndex=ball_collision, 
    basePosition=[0, 0, 2] # Lowered height slightly for better visibility
)

# 3. Enable Bounciness (Restitution)
# Fixed the variable name here from mesh_id to bowl_body
p.changeDynamics(bodyUniqueId=bowl_body, linkIndex=-1, restitution=0.8)
p.changeDynamics(bodyUniqueId=ball_id, linkIndex=-1, restitution=0.8)

# Run the simulation
while True:
    p.stepSimulation()
    time.sleep(1./240.)