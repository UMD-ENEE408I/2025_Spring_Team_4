# Turtlebot ROS Setup

Goes through how to start the turtlebot ros setup and run specific scripts in the catkin workspace.

## ROS Launch

Make sure the correct .bashrc is sources (it should already be). The .bashrc file should export environment variables corresponding to the turtlebot model, ros master ip, ros node ip, etc. 

Once the correct .bashrc is sourced, perform a turtlebot bringup by running this command: ```roslaunch turtlebot3_bringup turtlebot3_robot.launch```

## Running ROS Scripts

To run a ROS script, make sure that the script in the Catkin workspace has the correct execute permissions. If not, use ```chmod +x {filename}``` to add execution permissions to the script. 

When the script is ready to run, make sure the turtlebot has been brought up with instructions from the previous section then run the following command: ```rosrun {package name} {script name}```. 

