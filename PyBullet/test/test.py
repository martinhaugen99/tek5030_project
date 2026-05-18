import pybullet as p
import pybullet_data
import numpy as np
import time

# starting the simulation
physicsClient = p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0) # Disable logs
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0) # Hides the sidebars
p.configureDebugVisualizer(p.COV_ENABLE_KEYBOARD_SHORTCUTS, 0) # Disables built-in hotkeys
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")#floor plane

# setting up the mesh object
#collision_id = p.createCollisionShape(p.GEOM_MESH, fileName="room.obj", flags=p.GEOM_FORCE_CONCAVE_TRIMESH)
#visual_id = p.createVisualShape(p.GEOM_MESH, fileName="room.obj") 
collision_id = p.createCollisionShape(
    p.GEOM_MESH, 
    fileName="pointcloud.obj", 
    flags=p.GEOM_FORCE_CONCAVE_TRIMESH,
    meshScale=[3, 3, 3]
    )
visual_id = p.createVisualShape(p.GEOM_MESH, 
    fileName="pointcloud_high_res.obj",
    meshScale=[3, 3, 3]
    )
body = p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=collision_id,
    baseVisualShapeIndex=visual_id,
    basePosition=[0, 0, 3]
)

# creating the Ball
ball_collision = p.createCollisionShape(p.GEOM_SPHERE, radius=0.1)
ball_id = p.createMultiBody(
    baseMass=1, 
    baseCollisionShapeIndex=ball_collision, 
    basePosition=[0, -2, 5] # Lowered height slightly for better visibility
)

# adding bounciness
p.changeDynamics(bodyUniqueId=body, linkIndex=-1, restitution=0.8)
p.changeDynamics(bodyUniqueId=ball_id, linkIndex=-1, restitution=0.8)


def shoot_ball_from_camera(ball_id, speed=10.0):
    """
    Sets the ball's position to the camera center and 
    launches it in the vewing direction pluss some change.
    """
    cam_data = p.getDebugVisualizerCamera()

    # The world to camera transform
    T_wc = np.array(cam_data[2]).reshape(4, 4, order='F')

    # The camera to world transform
    T_cw = np.linalg.inv(T_wc)
    
    #camera position vector from the translation(three first values in last column) in the homogenius matrix
    camera_pos = T_cw[:3, 3] 
    
    # Row 2 (Z-axis) of the rotation matrix, but it is the backward direction, so we negate it
    forward_vector = -T_wc[2, :3] 
    
    # Position the ball slightly in front of the camera to avoid clipping
    spawn_pos = camera_pos + (forward_vector * 0.5) #0.5m
    
    # Set the ball's position and orientation
    p.resetBasePositionAndOrientation(ball_id, spawn_pos, [0, 0, 0, 1])
    
    # Velocity is the forward vector(length=1) scaled by speed
    # adding some upwards speed aswell, as we can only look at the origin
    velocity = forward_vector * speed + [0, 5, 0]@T_wc[:3, :3]
    p.resetBaseVelocity(ball_id, linearVelocity=velocity)


def get_and_print_ball_position(ball_id):
    """
    Prints, and returns the current (x, y, z) position of the ball.
    """
    # getBasePositionAndOrientation returns a tuple: (position, orientation_quaternion)
    position, _ = p.getBasePositionAndOrientation(ball_id)
    
    # Print the coordinates (formatted to 3 decimal places for readability)
    print(f"Ball Position -> X: {position[0]:.3f}, Y: {position[1]:.3f}, Z: {position[2]:.3f}")
    
    # Return just the (x, y, z) position tuple
    return position

    


# run the simulation
while True:
    key = p.getKeyboardEvents()
    
    # Fire the ball with 'f'
    if ord('f') in key and key[ord('f')] & p.KEY_WAS_TRIGGERED:
        print("Ball fired!")
        shoot_ball_from_camera(ball_id, speed=10.0)

    # Print the ball position with 'p'
    if ord('p') in key and key[ord('p')] & p.KEY_WAS_TRIGGERED:
        current_pos = get_and_print_ball_position(ball_id)

    p.stepSimulation()
    time.sleep(1./240.)