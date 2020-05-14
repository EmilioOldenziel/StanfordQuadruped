# start with clean raspbian lite
sudo apt-get update
sudo apt-get install -y git

# set python 3 and pip3 as default
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
sudo update-alternatives --config python

sudo apt-get install python3-pip
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
sudo update-alternatives --config pip

# lib atlas for numpy
sudo apt-get -y install libatlas-base-dev

# install python requirements
pip install -r requirements.txt --user
pip install git+https://github.com/joan2937/pigpio

cd ..
git clone https://github.com/stanfordroboticsclub/PupperCommand.git
cd PupperCommand
sudo bash install.sh
cd ..

git clone https://github.com/stanfordroboticsclub/PS4Joystick.git
cd PS4Joystick
sudo bash install.sh
cd ..
sudo systemctl enable joystick

cd StanfordQuadruped
sudo ln -s $(realpath .)/robot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable robot
sudo systemctl start robot
