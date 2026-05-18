import pybullet as p
import pybullet_data
import numpy as np
import time

def convert(camera_pos, camera_quat, distance):
    """
        camera_pos: [x, y, z] position of the camera lens.
        camera_quat: [x, y, z, w] quaternion for the camera's orientation.
        distance: float zoom in and out
    """
    # Ensure camera position is a numpy array
    camera_pos = np.array(camera_pos, dtype=float)
    
    # 1. Convert quaternion to a 3x3 rotation matrix using NumPy reshape
    rot_matrix = np.array(p.getMatrixFromQuaternion(camera_quat)).reshape(3, 3)
    
    # 2. Extract the Forward Vector. 
    # Your original indices [0, 3, 6] correspond to the first column of the 3x3 matrix.
    forward_vec = rot_matrix[:, 0] 
    
    # 3. Calculate the "fake" target position slightly in front of the camera using vector math
    target_pos = camera_pos + (forward_vec * distance)
    
    # 4. Mathematically extract PyBullet's specific Pitch and Yaw using NumPy
    # Clip the Z value between -1.0 and 1.0 to prevent math domain errors 
    fz_clamped = np.clip(forward_vec[2], -1.0, 1.0)
    pitch = np.degrees(np.arcsin(fz_clamped))
    
    # PyBullet's yaw is calculated relative to the Y axis
    yaw = np.degrees(np.arctan2(forward_vec[0], -forward_vec[1]))
    
    return pitch, yaw, target_pos

def move(camera_path, distance=1.0, speed=0.01):
    """
        camera_path: List of tuples ([x,y,z], [roll, pitch, yaw])
        distance: float zoom in and out
        speed: float determining step size
    """
    for camera_pos, rpy in camera_path:
        quat = p.getQuaternionFromEuler(rpy)
        pitch, yaw, pos = convert(camera_pos, quat, distance)
        p.resetDebugVisualizerCamera(
            cameraDistance=distance,
            cameraYaw=yaw,
            cameraPitch=pitch,
            cameraTargetPosition=pos
        )
        time.sleep(1.0)


        
 

#this doesnt work, it drifts because it doesnt convert the positions
def move_at_speed(camera_path, distance=1.0, speed=0.01):
    """
        camera_path: List of tuples ([x,y,z], [roll, pitch, yaw])
        distance: float zoom in and out
        speed: float determining step size
    """
    for camera_pos, rpy in camera_path:
        # Convert inputs to NumPy arrays
        camera_pos = np.array(camera_pos, dtype=float)
        rpy = np.array(rpy, dtype=float)
        
        # PyBullet still requires standard lists/tuples for its internal functions
        quat = p.getQuaternionFromEuler(rpy.tolist())
        target_pitch, target_yaw, target_pos = convert(camera_pos, quat, distance)
        
        _, pitch, yaw = rpy
        
        # Calculate the vector difference and its magnitude (distance)
        change = target_pos - camera_pos
        dist = np.linalg.norm(change)
        
        # Determine number of steps (ensure it is an integer and at least 1)
        num_steps = max(1, int(dist // speed))
        
        # --- NUMPY MAGIC ---
        # Instead of manually adding a step value in a loop, we use np.linspace
        # to generate the entire array of interpolation points evenly spaced.
        pos_trajectory = np.linspace(camera_pos, camera_pos + change, num_steps)
        yaw_trajectory = np.linspace(yaw, yaw + target_yaw, num_steps)
        pitch_trajectory = np.linspace(pitch, pitch + target_pitch, num_steps)
        
        # Step through the generated trajectories side-by-side
        for pos, current_yaw, current_pitch in zip(pos_trajectory, yaw_trajectory, pitch_trajectory):
            p.resetDebugVisualizerCamera(
                cameraDistance=distance,
                cameraYaw=current_yaw,
                cameraPitch=current_pitch,
                cameraTargetPosition=pos.tolist() # Convert back to list for PyBullet
            )
            time.sleep(0.05)


# Connect to GUI
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.loadURDF("plane.urdf")

# Example path: List of ( [x,y,z], [roll, pitch, yaw] in radians )
camera_path = [
    ([0, 0, 1], [0, 0, 0]),
    ([1, 1, 1], [0, 0, 0.5]),
    ([2, 2, 1], [0, 0, 1.0]),
    ([3, 3, 1], [0, 0, 1.57])
]

#move_at_speed(camera_path)
move(camera_path)