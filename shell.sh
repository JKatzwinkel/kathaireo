#!/bin/bash

# check python version
pyver=$(python -c "import sys;print '.'.join([str(d) for d in sys.version_info[:3]])")
if [[ "$pyver" < "2.7.0" ]]; then
	echo "Version of standard python interpreter is $pyver, but"
	echo "2.7.0 is required..."
	py=$(which python2.7)
	if [ -n "$py" ]; then
		echo "Ok. found python2.7 at $py."
	else
		echo "aborting.."
		exit 1
	fi
else
	py=$(which python)
fi

echo "starting kathaireo shell..."
$py kathaireo/kathaireo.py

