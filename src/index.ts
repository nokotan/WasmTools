import wasmModPromise from "../cpp-lib/bin/WasmLib";
import { WASIInstance } from "../js-bindings/WASIModule";

async function main() {
    const wasmMod = await wasmModPromise;
    WASIInstance.instance.setMemory(wasmMod.memory);

    console.log(wasmMod.add(24, 74));
    console.log(wasmMod.sub(24, 74));

    console.log(await WASIInstance.fs.getStdOut());
}

main();