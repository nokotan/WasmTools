#!/usr/bin/python3

import subprocess
from io import StringIO

class Executor:
    def __init__(self):
        self.nodeFilePath = "node"
        self.compilerPath = "wasm-js-bridge/extract-wasm-export.js"
        self.targetFilePath = ""

    def run(self):
        commandLine = [ self.nodeFilePath, self.compilerPath, self.targetFilePath ]
        result = subprocess.run(commandLine, stdout=subprocess.PIPE, text=True)
        
        return result.stdout
