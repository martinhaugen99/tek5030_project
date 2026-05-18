# TEK5030 project

1. Get stereo video form Realsense D435 and calibrate camera 


### Get RealSense to work inside wsl:

In WSL:
- `sudo isaac-ros init docker`

In powershell as admin:
- `usbipd list`
- `usbipd bind --busid <busid>`
- `usbipd attach --wsl --busid <busid>`

In WSL:
- `lsusb # to check if usb is recognised`
- `isaac-ros activate`

- `ros2 launch isaac_ros_visual_slam isaac_ros_visual_slam_realsense.launch.py \
    tracking_mode:=0`
