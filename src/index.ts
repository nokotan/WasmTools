import wasmModPromise from "../cpp-lib/bin/WasmLib";

async function main() {
    const wasmMod = await wasmModPromise;
    console.log(wasmMod.add(24, 74));
    console.log(wasmMod.sub(24, 74));
}

main();