# Catkin Commands

This file contains some common commands for creating catkin packages. 

## Create a Catkin Package

First, make sure that you are in the src folder in your catkin workspace. Then run the following command: 

```catkin_create_pkg {package name} {dependencies}```

Some common dependencies are:

- rospy
- geometry_msg
- std_msg

Once the catkin package has been created, add a script folder to the catkin package. You may put python scripts in this folder then use ```chmod +x {filename}``` to make the file executable. 

Then, move to the top root folder for the catkin workspace and run the following command to build the workspace: ```catkin_make```.

This command may be run before or after the scripts have been installed. It only needs to run once after the package has been created. 

## Deleting Catkin Packages

Just delete the directory of the package. 