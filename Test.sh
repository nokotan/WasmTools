#!/bin/bash

./wasm-js-bridge/gen-bridge.py "./cpp-lib/bin/WasmLib.wasm" "./cpp-lib/src/Main.cpp" > ./cpp-lib/bin/WasmLib.d.ts