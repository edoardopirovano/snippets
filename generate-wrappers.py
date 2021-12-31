with open('functions.txt') as f:
    lines = f.readlines()
    versionsArm64 = ""
    versionsi386 = ""
    functions = ""
    wrappings = ""
    for line in lines:
        nameStart = line.index(' ')
        retType = line[0:nameStart]
        argsStart = line.index('(')
        funcName = line[nameStart+1:argsStart]
        args = line[argsStart+1:-3]
        versionConstant = funcName.upper() + "_VERSION"
        versionsArm64 += f"#define {versionConstant} \"GLIBC_2.2.5\"\n"
        versionsi386 += f"#define {versionConstant} \"GLIBC_2.0\"\n"
        functions += f"SET_GLIBC_VERSION({versionConstant}, {retType}, {funcName}, {args}) {{\n    return __real_{funcName}();\n}}\n\n"
        wrappings += f",--wrap={funcName}"
    print(versionsArm64)
    print("\n\n")
    print(versionsi386)
    print("\n\n")
    print(functions)
    print("\n\n")
    print(wrappings)