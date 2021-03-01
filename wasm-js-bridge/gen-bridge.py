#!/usr/bin/python3

import extractWasmExport
import extractComments
from io import StringIO
import json as JsonUtil
import sys

class FunctionDefinition:
    def __init__(self, item):
        self.parameters = item["params"]
        self.returnType = item["returnTypes"][0] if len(item["returnTypes"]) > 0 else "void"
        self.name = item["name"]
        self.comment = item["comment"]

    def toModuleDef(self):
        parameterDefinition = ", ".join([ f"{ param['name'] }: { param['type'] }" for param in self.parameters ])
        return f"{ self.comment }\nexport function { self.name }({ parameterDefinition }): {self.returnType};"

    def toClassFunctionDef(self):
        parameterDefinition = ", ".join([ f"{ param['name'] }: { param['type'] }" for param in self.parameters ])
        return f"{ self.comment }\n{ self.name }({ parameterDefinition }): {self.returnType};"



class FunctionDefinitionFilter:
    def __init__(self, comments):
        self.comments = comments

    def filterByExports(self, exports):
        exportsName = [ export["name"] for export in exports ]
        self.comments = [ comment for comment in self.comments if comment["name"] in exportsName ]

    def addFunctionTypeDefinition(self, exports):
        for comment in self.comments:
            correspondingExports = [ export for export in exports if comment["name"] == export["name"] ]

            assert len(correspondingExports) == 1
            correspondingExport = correspondingExports[0]

            comment["params"] = [ 
                    { "name": nativeDef["name"], "type": nativeDef["type"], "exportType": wasmTypeName } 
                    for nativeDef, wasmTypeName in zip(comment["params"], correspondingExport["params"]) 
                ]
            comment["returnTypes"] = correspondingExport["results"]

    def transformType(self):
        for comment in self.comments:
            comment["params"] = [ 
                { "name": param["name"], "type": "number" } 
                for param in comment["params"]
            ]
            comment["returnTypes"] = [
                "number" for _ in comment["returnTypes"]
            ] 



def main(argv):
    path = argv[1]
    sourcePath = argv[2]
    args = argv[3:]

    commentsExecutor = extractComments.Executor(extractComments.SimpleTreeWalker(), extractComments.DictionaryGeneratingVisitor())
    commentsExecutor.path = sourcePath
    commentsExecutor.args = args
    commentsExecutor.run()

    exportExecutor = extractWasmExport.Executor()
    exportExecutor.targetFilePath = path
    exportOutput = exportExecutor.run()

    commentsDefinition = commentsExecutor.generator.getDefinitions()
    exportDefinition = JsonUtil.loads(exportOutput)
    merger = FunctionDefinitionFilter(commentsDefinition)

    merger.filterByExports(exportDefinition)
    merger.addFunctionTypeDefinition(exportDefinition)
    merger.transformType()

    classDefs = "\n".join([ FunctionDefinition(comment).toClassFunctionDef() for comment in merger.comments ])
    indentedClassDefs =  "\n".join([ f"  { line }" for line in classDefs.split("\n") ])
    
    print(f"""
/* Auto-gererated type definition. */

export declare class WasmModule {{
{ indentedClassDefs }
}}
    """)

if __name__ == "__main__":
    main(sys.argv)
