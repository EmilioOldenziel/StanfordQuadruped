sudo apt-get -y install libatlas-base-dev
pip install -r requirements.txt --user

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

wget https://github.com/joan2937/pigpio/archive/v76.zip
unzip v74.zip
cd pigpio-76
make
sudo make install
cd ..

cd StanfordQuadruped
sudo ln -s $(realpath .)/robot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable robot
sudo systemctl start robot
