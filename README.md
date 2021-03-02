# WasmTools

## Overview

This repository aims to 

## Dependencies

- emscripten [^1.39.1]

If you want to install dependencies manually,

- python3
- node.js [^10.0.0]
- clang [^8.0.0]
- libclang

## Installing Dependent Packages

```sh
# Install Python Dependent Packages
pip install clang

# Install node.js Dependent Packages
npm install
```

## Building C++ Project

```sh
mkdir cpp-lib/bin && cd cpp-lib/bin
make
```

## Generating WebAssembly Type Definition

```sh
./wasm-js-bridge/gen-bridge.py "./cpp-lib/bin/WasmLib.wasm" "./cpp-lib/src/Main.cpp" > ./cpp-lib/bin/WasmLib.d.ts
```

## Bundling WebSite

```sh
npx webpack
```
