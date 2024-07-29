# Steps: 
1. **Clone my repo** https://github.com/Midnight1Knight/Blood-object-detection
2. **Installing venv:**
*Linux*
<pre>
python3 -m venv .obj_det
source .obj_det/bin/activate
</pre> 
*Windows*
<pre>
python -m venv .obj_det
.\.obj_det\Scripts\activate
</pre> 
3. **Install dependencies and add virtual environment to the Python Kernel**
*Linux*
<pre>
python3 -m pip install --upgrade pip
pip install ipykernel
python3 -m ipykernel install --user --name=obj_det
</pre>
*Windows*
<pre>
python -m pip install --upgrade pip
pip install ipykernel
python -m ipykernel install --user --name=obj_det
</pre> 
4. **Install cuda drivers**
5. **Install protobuf**
*Linux*
<pre>
sudo apt-get install protobuf-compiler
</pre>
*Windows* official github with releases: https://github.com/protocolbuffers/protobuf/releases

6. **Run notebooks**
