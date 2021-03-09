#!/bin/bash

case ${1} in
emscripten)
  emcmake cmake ..;;
emclang)
  export CC=${EMSDK}/upstream/bin/clang
  export CXX=${EMSDK}/upstream/bin/clang++
  export LD=${EMSDK}/upstream/bin/wasm-ld

  cmake .. -DCMAKE_CXX_LINK_EXECUTABLE="${LD} -o <TARGET> <LINK_FLAGS> <OBJECTS>";;
wasi)
  PARENT_DIR=$(dirname "$(pwd)")
  WASI_SDK_ROOT=$(dirname "${PARENT_DIR}")

  cmake .. \
    -DCMAKE_TOOLCHAIN_FILE="${WASI_SDK_ROOT}/wasi/share/cmake/wasi-sdk.cmake" \
    -DWASI_SDK_PREFIX="${WASI_SDK_ROOT}/wasi"                                 \
    -DCMAKE_C_FLAGS="--sysroot=\"${WASI_SDK_ROOT}/wasi/share/wasi-sysroot\""  \
    -DCMAKE_CXX_FLAGS="--sysroot=\"${WASI_SDK_ROOT}/wasi/share/wasi-sysroot\"";;
*)
  printf "InitProject.sh <template>\n"
  printf "template:\n"
  printf "  emscripten\n"
  printf "  emclang\n"
  printf "  wasi\n"
esac
