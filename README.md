# Example Reddit gRPC API

## Setup

You may have to give the scripts execute privielidges. Run ```./setup.sh```. The comments inside give information about the script.

It runs ```./gen_API.sh``` which remakes the protos in the necessary `client` and `server` modules.

## Start

In one terminal, change directories to `server` and run ```python reddit_server.py```.

In another terminal, change directories to `client` and run ```python reddit_client.py```. This sends a pre-defined request to the server.

Both can be run with command-line arguments. The argumets can be listed with the swiches `-h` or `--help`.