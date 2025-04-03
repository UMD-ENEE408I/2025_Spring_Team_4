# Jetson Setup

Instructions for setting up the Jetson environment such as python, ROS, and other dependencies.

TODO:

- Set up ROS
- Download python (if not already there)
- Configure Ultralytics to use the Jetson GPU

1. Update os
    - Run ```sudo apt-get update```
    - Then run ```sudo apt-get upgrade```
2. Configure Jetson to pull data from github
    - Run ```git config --global user.name XXXX```
    - Run ```git config --global user.email XXXX```
    - Generate ssh key if wanted and add to github account:
        - Run ```ssh-keygen -t ed25519```
