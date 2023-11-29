#!/bin/bash

for file in client server
do
    python -m grpc_tools.protoc -I./protos --python_out=$file --grpc_python_out=$file ./protos/*.proto
done