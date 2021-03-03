import { add, sub, memory } from "../cpp-lib/bin/WasmLib.wasm";
import { fs, wasiInstance } from "../js-bindings/WASIModule";

function preMain() {
    // Redirect WASI's stdout to `console.log`.
    const textDecoder = new TextDecoder();

    fs.volume.fds[1].node.write = (buf, off, len, pos) => {
        console.log(textDecoder.decode(buf.buffer));
        return len ?? 0;
    };

    // Pass WemAssembly.Memory instance to WASI default instance
    // so that WASI works properly. 
    wasiInstance.setMemory(memory);
}

function main() {
    console.log(add(24, 74));
    sub(24, 74);
}

preMain();
main();