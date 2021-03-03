import { WASI } from "@wasmer/wasi"
import { WasmFs } from "@wasmer/wasmfs";

export const fs = new WasmFs();

export const wasiInstance = new WASI({
    args: [],
    env: {},
    bindings: {
        ...WASI.defaultBindings,
        fs: fs.fs
    } 
});