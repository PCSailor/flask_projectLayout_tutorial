'''
Terminal Commands
lsb_release -d
sudo apt update && sudo apt upgrade
cd /mnt/<drive letter>
mkdir <folder_project structure>
python3 --version
sudo apt upgrade python3
sudo apt install python3-pip
sudo apt install python3-venv
-Navigate inside project folder
python3 -m venv .venv (Permission issues? elevate prompt: sudo -i  (& exit))
source .venv/bin/activate (.venv prompt) (deactivate to end)
code . (may need restart) (run this in .venv or not)
Install Python ext within VSC-WSL:Linux if necessary
Test Python in VSC terminal
python3 -m pip install flask
python3 -m flask --version
touch app.py
Ensure correct VSC interpreter (Python...'.venv':venv) (bottom-left)
'''
# use this code in the app.py file
from flask import Flask
app = Flask(__name__) # creates an instance of Flask object

@app.route("/")
def home():
    return "Hello World from Flask test.py"

#  Terminal: python3 -m flask run
# in browser, open http://127.0.0.1:5000/
#  Terminal: Ctrl C to quit flask run
