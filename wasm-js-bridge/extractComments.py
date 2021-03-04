#!/usr/bin/python3

from clang.cindex import Index, Config, CursorKind
import json as JsonUtil
import os, io, sys



class SimpleTreeWalker:
    def __init__(self):
        self.namespace = []

    def walkThroughClass(self, cursor, visitor):
        if cursor.kind == CursorKind.CXX_METHOD:
            name = "::".join(self.namespace + [ cursor.spelling ])
            visitor.visitClassFunction(name, cursor)
        elif cursor.kind in ( CursorKind.STRUCT_DECL, CursorKind.CLASS_DECL, CursorKind.CLASS_TEMPLATE ):
            self.namespace += [ cursor.spelling ]

            name = "::".join(self.namespace + [ cursor.spelling ])
            visitor.visitClassDefinition(name, cursor)

            for child in cursor.get_children():
                self.walkThroughClass(child, visitor)

            self.namespace.pop()

    def walkThrough(self, cursor, visitor):
        if cursor.kind == CursorKind.NAMESPACE:
            self.namespace += [ cursor.spelling ]

            for child in cursor.get_children():
                self.walkThrough(child, visitor)
            
            self.namespace.pop()
        elif cursor.kind in ( CursorKind.LINKAGE_SPEC, CursorKind.UNEXPOSED_DECL ):
            for child in cursor.get_children():
                self.walkThrough(child, visitor)
        elif cursor.kind in ( CursorKind.STRUCT_DECL, CursorKind.CLASS_DECL, CursorKind.CLASS_TEMPLATE ):
            self.namespace += [ cursor.spelling ]

            name = "::".join(self.namespace + [ cursor.spelling ])
            visitor.visitClassDefinition(name, cursor)

            for child in cursor.get_children():
                self.walkThroughClass(child, visitor)

            self.namespace.pop()
        elif cursor.kind == CursorKind.FUNCTION_DECL:
            name = "::".join(self.namespace + [ cursor.spelling ])
            visitor.visitGlobalFunction(name, cursor)

    def startWalk(self, cursor, visitor):  
        if cursor.kind == CursorKind.TRANSLATION_UNIT:
            for child in cursor.get_children():
                self.walkThrough(child, visitor)



class DictionaryGeneratingVisitor:
    def __init__(self):
        self.definitions = []

    def visitGlobalFunction(self, name, cursor):
        comment = cursor.raw_comment
        mangledName = cursor.mangled_name
        params = [ 
            { "name": child.spelling, "type": child.type.spelling } 
            for child in cursor.get_children() if child.kind == CursorKind.PARM_DECL 
        ]

        if mangledName and comment:
            self.definitions.append({ "name": name, "mangledName": mangledName, "params": params, "comment": comment })

    def visitClassDefinition(self, name, cursor):
        pass
    
    def visitClassFunction(self, name, cursor):
        comment = cursor.raw_comment
        mangledName = cursor.mangled_name
        params = [ 
            { "name": child.spelling, "type": child.type.spelling } 
            for child in cursor.get_children() if child.kind == CursorKind.PARM_DECL 
        ]
        
        if mangledName and comment:
            self.definitions.append({ "name": name, "mangledName": mangledName, "params": params, "comment": comment })

    def getDefinitions(self):
        return self.definitions

    def serializeTo(self, stream):
        JsonSerialized = JsonUtil.dumps(self.definitions, ensure_ascii=False, indent=2)
        stream.write(JsonSerialized)



def FindLibClang():
    import platform
    name = platform.system()

    if name == 'Darwin':
        dynamicLibPathCandicates = [
            os.environ.get("EMSDK") + "/upstream/lib/libclang.dylib" if os.environ.get("EMSDK") else None
        ]
    elif name == 'Windows':
        dynamicLibPathCandicates = [
            os.environ.get("EMSDK") + "/upstream/lib/libclang.dll" if os.environ.get("EMSDK") else None
        ]
    else:
        dynamicLibPathCandicates = [
            os.environ.get("EMSDK") + "/upstream/lib/libclang,dylib" if os.environ.get("EMSDK") else None,
            "/usr/lib/llvm-7/lib/libclang.so",
            "/usr/lib/llvm-7/lib/libclang.so.1",
            "/usr/lib/x86_64-linux-gnu/libclang-7.so",
            "/usr/lib/x86_64-linux-gnu/libclang-7.so.1",
        ]

    for candicate in dynamicLibPathCandicates:
        if os.path.exists(candicate):
            return candicate
    
    raise RuntimeError("There is no libclang installation")

class Executor:
    def __init__(self, walker, generator):
        self.walker = walker
        self.generator = generator

        self.libClangPath = FindLibClang()
        self.path = None
        self.args = None

    def run(self):
        Config.set_library_file(self.libClangPath)
        
        index = Index.create()
        tree = index.parse(self.path, args=self.args)

        self.walker.startWalk(tree.cursor, self.generator)



def main(argv):
    path = argv[1]
    args = argv[2:]

    executor = Executor(SimpleTreeWalker(), DictionaryGeneratingVisitor())
    executor.path = path
    executor.args = args
    executor.run()

    executor.generator.serializeTo(sys.stdout)

if __name__ == "__main__":
    main(sys.argv)
