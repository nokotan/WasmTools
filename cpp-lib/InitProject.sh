#!/bin/bash

export CC=${EMSDK}/upstream/bin/clang
export CXX=${EMSDK}/upstream/bin/clang++
export LD=${EMSDK}/upstream/bin/wasm-ld

cmake .. -DCMAKE_CXX_LINK_EXECUTABLE="${LD} -o <TARGET> <LINK_FLAGS> <OBJECTS>"