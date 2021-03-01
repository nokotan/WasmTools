"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var wasmParser = require("@webassemblyjs/wasm-parser");
var wasmAst = require("@webassemblyjs/ast");
var fs_1 = require("fs");
var MyAstVisitor = /** @class */ (function () {
    function MyAstVisitor() {
        this.exports = [];
        this.functionDefinitions = [];
    }
    MyAstVisitor.prototype.Func = function (path, block) {
        var node = path.node;
        this.functionDefinitions.push({
            name: node.name.value,
            params: node.signature.params.map(function (value) { return value.valtype; }),
            results: node.signature.results
        });
    };
    MyAstVisitor.prototype.ModuleExport = function (path) {
        // nop
    };
    MyAstVisitor.prototype.ModuleExportDescr = function (path) {
        if (path.node.exportType == "Func") {
            this.exports.push(path.node.id.value);
        }
    };
    MyAstVisitor.prototype.getExports = function () {
        var _this = this;
        return this.functionDefinitions.filter(function (value) { return _this.exports.includes(value.name); });
    };
    return MyAstVisitor;
}());
var Executor = /** @class */ (function () {
    function Executor(visitor) {
        this.visitor = visitor;
        this.path = "";
    }
    Executor.prototype.run = function () {
        var binary = fs_1.readFileSync(this.path);
        var decoderOpts = {};
        var ast = wasmParser.decode(binary, decoderOpts);
        wasmAst.traverse(ast, this.visitor);
    };
    return Executor;
}());
function main(args) {
    var visitor = new MyAstVisitor();
    var executor = new Executor(visitor);
    executor.path = args[0];
    executor.run();
    var jsonSerialized = JSON.stringify(visitor.getExports(), undefined, 2);
    console.log(jsonSerialized);
}
main(process.argv.slice(2));
