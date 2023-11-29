#!/bin/bash

python -m grpc_tools.protoc -I. --python_out=client --pyi_out=client --grpc_python_out=client ./reddit.proto
python -m grpc_tools.protoc -I. --python_out=server --pyi_out=server --grpc_python_out=server ./reddit.proto