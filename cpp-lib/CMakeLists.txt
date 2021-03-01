cmake_minimum_required(VERSION 3.13)

project(WasmLib)

add_executable(WasmLib)

target_sources(WasmLib
    PRIVATE
        src/Main.cpp
)

set_target_properties(WasmLib
    PROPERTIES 
        COMPILE_FLAGS "-O2 --target=wasm32-wasm"
        LINK_FLAGS "-O2 --no-entry --export add --export sub"
        CXX_STANDARD 17
        SUFFIX ".wasm"
)