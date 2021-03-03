# WasmTools

## Overview

This repository aims to build websites with webpack, WebAssembly in C/C++, WASI.

## Dependencies

### With WASI

- [WASI SDK](https://github.com/WebAssembly/wasi-sdk)
- python3
- node.js [^10.0.0]
- libclang

### With Emscripten

- emscripten [^1.39.1]

## Installing Dependent Packages

```sh
# Install Python Dependent Packages
pip install clang

# Install node.js Dependent Packages
npm install
```

## Building C++ Project

### With WASI

```sh
mkdir cpp-lib/bin && cd cpp-lib/bin
cmake cmake .. \
    -DCMAKE_TOOLCHAIN_FILE=../../wasi/share/cmake/wasi-sdk.cmake \
    -DWASI_SDK_PREFIX="<ProjectDir>/wasi" \
    -DCMAKE_C_FLAGS="--sysroot=\"<ProjectDir>/wasi/share/wasi-sysroot\"" \
    -DCMAKE_CXX_FLAGS="--sysroot=\"<ProjectDir>/wasi/share/wasi-sysroot\""
make
```

### With Emscripten

Now Preparing...

## Generating WebAssembly Type Definition

```sh
./wasm-js-bridge/gen-bridge.py "./cpp-lib/bin/WasmLib.wasm" "./cpp-lib/src/Main.cpp" > ./cpp-lib/bin/WasmLib.wasm.d.ts
# Or, npm run gen-dts
```

## Bundling WebSite

```sh
npx webpack
# Or, npm run build
```
