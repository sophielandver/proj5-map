##
## Except for installation, all commands should be run with 
## the virtual environment active
##

# Configuration 
#
PYVENV = /usr/local/bin/pyvenv-3.5  
##
## Install in a new environment:
##     We need to rebuild the Python environment to match
##     
install:
	# pyvenv-3.4 env ### BUGGY on ix
	echo "pyvenv without PIP to work around ubuntu bug"
	$(PYVENV) --without-pip env
	echo ""
	(.  env/bin/activate; curl https://bootstrap.pypa.io/get-pip.py | python)
	(.  env/bin/activate; pip install -r requirements.txt)

dist:
	pip freeze >requirements.txt