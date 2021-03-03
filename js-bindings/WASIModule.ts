import { WASI } from "@wasmer/wasi"
// import wasiBindings from "@wasmer/wasi/lib/bindings/browser";
import { WasmFs } from "@wasmer/wasmfs";

const fs = new WasmFs();

export class WASIInstance {

    static fs = fs;

    static instance = new WASI({
        args: [],
        env: {},
        bindings: {
          ...WASI.defaultBindings,
          fs: fs.fs
        } 
    });
}