const wasmParser = require("@webassemblyjs/wasm-parser");
const wasmAst = require("@webassemblyjs/ast");

import { readFileSync } from "fs";

interface Visitor {
    Func(path: any, block: any): void;
    ModuleExport(path: any): void;
    ModuleExportDescr(path: any): void;
}

interface FunctionDefinition {
    name: string;
    params: string[];
    results: string[];
}

class MyAstVisitor implements Visitor { 
    private exports: string[];
    private functionDefinitions: FunctionDefinition[];

    constructor() {
        this.exports = [];
        this.functionDefinitions = [];
    }

    Func(path: any, block: any): void {
        const node = path.node;

        this.functionDefinitions.push({
            name: node.name.value,
            params: node.signature.params.map((value: any) => value.valtype),
            results: node.signature.results
        });
    }

    ModuleExport(path: any): void {
        // nop
    }

    ModuleExportDescr(path: any): void {
        if (path.node.exportType == "Func") {
            this.exports.push(path.node.id.value)
        }
    }

    getExports(): FunctionDefinition[] {
        return this.functionDefinitions.filter((value) => this.exports.includes(value.name));
    }
}

class Executor {
    path: string;
    visitor: Visitor;

    constructor(visitor: Visitor) {
        this.visitor = visitor;
        this.path = "";
    }

    run(): void {
        const binary = readFileSync(this.path);

        const decoderOpts = {};
        const ast = wasmParser.decode(binary, decoderOpts);
        
        wasmAst.traverse(ast, this.visitor)
    }
}

function main(args: string[]) {
    const visitor = new MyAstVisitor();
    const executor = new Executor(visitor);

    executor.path = args[0];
    executor.run();

    const jsonSerialized = JSON.stringify(visitor.getExports(), undefined, 2);
    console.log(jsonSerialized);
}

main(process.argv.slice(2));