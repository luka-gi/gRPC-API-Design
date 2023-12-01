#!/bin/bash

for file in client server .
do
    # remove existing protos
    rm $file/protos/*_pb2*
    # recreate protos
    python -m grpc_tools.protoc -I./proto_definitions --python_out=$file/protos --grpc_python_out=$file/protos ./proto_definitions/*.proto
done