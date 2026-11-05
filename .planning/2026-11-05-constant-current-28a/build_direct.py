"""Clean build of every uvprojx source using installed Keil command-line tools."""
from pathlib import Path
import argparse
import subprocess
import sys
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument("--variant", choices=("ac5", "ac6"), default="ac6")
args = parser.parse_args()
task_dir = Path(__file__).resolve().parent
root = task_dir.parent.parent
project_dir = root / "KEIL_PRJ"
target = ET.parse(project_dir / "MM32SPIN0230_Demo.uvprojx").find("./Targets/Target")
out = task_dir / (args.variant + "-direct")
objects = out / "Objects"
objects.mkdir(parents=True, exist_ok=True)
tool_dir = Path("D:/Users/mym02/AppData/Local/Keil_v5/ARM") / (
    "ARMCLANG" if args.variant == "ac6" else "ARMCC"
) / "bin"
inc_text = target.findtext("./TargetOption/TargetArmAds/Cads/VariousControls/IncludePath")
includes = [(project_dir / name).resolve() for name in inc_text.split(";")]
includes.append(root / "CMSIS/Core/Include")
defines = target.findtext("./TargetOption/TargetArmAds/Cads/VariousControls/Define").split(",")
defines.append("__MICROLIB")
if args.variant == "ac6":
    compiler = tool_dir / "armclang.exe"
    flags = ["--target=arm-arm-none-eabi", "-mcpu=cortex-m0", "-mthumb",
             "-mfloat-abi=soft", "-std=c99", "-O1", "-g", "-fshort-enums",
             "-fshort-wchar", "-ffunction-sections"]
else:
    compiler = tool_dir / "armcc.exe"
    flags = ["--cpu", "Cortex-M0", "--apcs=interwork", "--c90", "-O1",
             "-g", "--split_sections", "--library_type=microlib"]
for inc in includes:
    flags.extend(["-I", str(inc)])
flags.extend("-D" + name.strip() for name in defines if name.strip())

log_path = out / "rebuild.log"
with log_path.open("w", encoding="utf-8") as log:
    def run(command):
        log.write("COMMAND: " + subprocess.list2cmdline([str(x) for x in command]) + "\n")
        result = subprocess.run([str(x) for x in command], cwd=root, capture_output=True)
        output = result.stdout.decode("utf-8", errors="replace") + result.stderr.decode("utf-8", errors="replace")
        log.write(output + "\n")
        log.flush()
        if result.returncode:
            print(output[-10000:])
            raise RuntimeError(f"Tool failed ({result.returncode}): {command[0]}")
        return output

    run([compiler, "--version" if args.variant == "ac6" else "--vsn"])
    object_paths = []
    libraries = []
    for file in target.findall("./Groups/Group/Files/File"):
        if file.findtext("./FileOption/CommonProperty/IncludeInBuild") == "0":
            continue
        source = (project_dir / file.findtext("FilePath").replace("\\", "/")).resolve()
        if source.suffix.lower() in (".c", ".s"):
            obj = objects / (source.stem.lower() + ".o")
            if obj in object_paths:
                raise RuntimeError("Duplicate object basename: " + str(obj))
            if source.suffix.lower() == ".c":
                run([compiler, *flags, "-c", source, "-o", obj])
            else:
                run([tool_dir / "armasm.exe", "--cpu", "Cortex-M0", "-g",
                     "--apcs=interwork", "--pd", "__MICROLIB SETA 1", source, "-o", obj])
            object_paths.append(obj)
            print("Compiled " + source.name, flush=True)
        elif source.suffix.lower() == ".lib":
            libraries.append(source)

    scatter = out / "memory.sct"
    scatter.write_text("""LR_IROM1 0x08000000 0x00008000 {
  ER_IROM1 0x08000000 0x00008000 {
    *.o (RESET, +First)
    *(InRoot$$Sections)
    .ANY (+RO)
    .ANY (+XO)
  }
  RW_IRAM1 0x20000000 0x00001000 {
    .ANY (+RW +ZI)
  }
}
""", encoding="ascii")
    axf = objects / "SPIN0230_DEMO.axf"
    map_file = out / "SPIN0230_DEMO.map"
    summary = run([tool_dir / "armlink.exe", "--cpu", "Cortex-M0", *object_paths,
                   *libraries, "--library_type=microlib", "--strict", "--scatter", scatter,
                   "--summary_stderr", "--info", "summarysizes,sizes,totals,unused,veneers",
                   "--map", "--xref", "--callgraph", "--symbols", "--list", map_file,
                   "-o", axf])
    print(summary[-2500:])
    hex_file = objects / "SPIN0230_DEMO.hex"
    run([tool_dir / "fromelf.exe", "--i32combined", "--output", hex_file, axf])
    disassembly = run([tool_dir / "fromelf.exe", "--text", "-c", "--output",
                      out / "SPIN0230_DEMO.disasm.txt", axf])
    print(f"Clean rebuild completed: {len(object_paths)} sources, {len(libraries)} core libraries")
    print("AXF: " + str(axf))
    print("HEX: " + str(hex_file))
    print("LOG: " + str(log_path))
