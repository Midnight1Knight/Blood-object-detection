# Steps: 
1. **Clone my repo** https://github.com/Midnight1Knight/Blood-object-detection /n
2. **Inside this library make another library *./Tensorflow/* and clone Object detection API inside this** https://github.com/tensorflow/models.git
3. **Installing venv:**
<pre>
python3 -m venv tfod
# activate
source tfod/bin/activate # Linux
.\tfod\Scripts\activate # Windows 
</pre> 
4. **Install dependencies and add virtual environment to the Python Kernel**
<pre>
python3 -m pip install --upgrade pip
pip install ipykernel
python3 -m ipykernel install --user --name=obj_det
</pre>
5. **Install protobuf**
For Linux:
<pre>
sudo apt-get install protobuf-compiler
</pre>
