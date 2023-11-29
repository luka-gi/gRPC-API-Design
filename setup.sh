#!/bin/bash

# create virtual environment
python3 -m venv venv
# activate environment
source venv/bin/activate
# install grpc dependencies
python -m pip install grpcio grpcio-tools

# compile protos
pushd reddit
./gen_API.sh
popd