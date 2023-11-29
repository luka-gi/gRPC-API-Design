#!/bin/bash

for file in client server
do
    # remove existing protos
    rm $file/*_pb2*
    # recreate protos
    python -m grpc_tools.protoc -I./protos --python_out=$file --grpc_python_out=$file ./protos/*.proto
done