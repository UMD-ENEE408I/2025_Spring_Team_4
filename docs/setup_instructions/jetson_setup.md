# Jetson Setup

Instructions for setting up the Jetson environment such as python, ROS, and other dependencies.

TODO:

- Set up ROS
- Download python (if not already there)
- Configure Ultralytics to use the Jetson GPU

1. Update OS
    - Run ```sudo apt-get update```
    - Then run ```sudo apt-get upgrade```
2. Configure Jetson to pull data from github
    - Run ```git config --global user.name XXXX```
    - Run ```git config --global user.email XXXX```
    - Generate ssh key if wanted, and add to github account:
        - Run ```ssh-keygen -t ed25519```
        - Copy the public key found in ~/.sss/ (or wherever you put the key file) to github. Make sure you only copy the contents of the *.pub file.
        - Then run ```git config --global core.sshCommand ssh -i *path to ssh key file (without .pub extension)*```
        - Run ```git clone XXX``` to get the repository.
3. Ensure python is configured correctly
    - Run ```which python```
        - If python is not installed, do it.
    - Run ```python -m pip```
        - If pip is not installed, follow this [link](https://pip.pypa.io/en/stable/installation/) to install pip.
        - When installing pip, if using the script, just use ```wget```
        - You may need to add a directory to your path variable after the install. Use ```export PATH=$PATH:/home/teamfoo/.local/bin``` to do so or add this line in .bashrc so it runs in every terminal.
4. Install ROS
    - 
