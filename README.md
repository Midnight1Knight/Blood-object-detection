# Steps: 
1. **Clone my repo** https://github.com/Midnight1Knight/Blood-object-detection
2. **Installing venv:**
<pre>
python3 -m venv .obj_det
# activate
source .obj_det/bin/activate # Linux
.\.obj_det\Scripts\activate # Windows 
</pre> 
3. **Install dependencies and add virtual environment to the Python Kernel**
<pre>
python3 -m pip install --upgrade pip
pip install ipykernel
python3 -m ipykernel install --user --name=obj_det
</pre>
4. **Install cuda drivers**
5. **Install protobuf**
For Linux:
<pre>
sudo apt-get install protobuf-compiler
</pre>
6. **Run notebooks**
