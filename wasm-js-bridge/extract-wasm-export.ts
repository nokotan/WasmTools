const wasmParser = require("@webassemblyjs/wasm-parser");
const wasmAst = require("@webassemblyjs/ast");

import { readFileSync } from "fs";

interface Visitor {
    ModuleImport?(path: any): void;
    Func?(path: any, block: any): void;
    ModuleExport?(path: any): void;
    ModuleExportDescr?(path: any): void;
}

interface FunctionDefinition {
    name: string;
    params: string[];
    results: string[];
}

interface ExportDefinition {
    name: string;
    id: number;
}

class MyAstVisitor implements Visitor { 
    private exports: ExportDefinition[];
    private functionDefinitions: FunctionDefinition[];

    constructor() {
        this.exports = [];
        this.functionDefinitions = [];
    }

    ModuleImport(path: any): void {
        const node = path.node;

        if (node.descr.type == "FuncImportDescr") {
            this.functionDefinitions.push({
                name: node.name.value,
                params: node.descr.signature.params.map((value: any) => value.valtype),
                results: node.descr.signature.results
            });
        }
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
        const node = path.node;

        if (node.descr.exportType == "Func") {
            this.exports.push({
                name: node.name,
                id: node.descr.id.value
            })
        }
    }

    getExports(): FunctionDefinition[] {
        return this.exports.map(_export => {
            const funcDef = this.functionDefinitions[_export.id];
            funcDef.name = _export.name;
            return funcDef;
        });
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