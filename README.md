stability test case lib
==============
1: env
sudo apt-get install pyhton-opencv
sudo apt-get install python-numpy
sudo pip install -r requirements.txt
2: execute test case:
nosetests --with-plan-loader --plan-file plan --loop 100 --with-file-output --verbosity 2