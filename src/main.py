import subprocess
import shlex
import os

def decompile(cfr_jar_path: str,
              input_path: str,
              output_dir: str,
              jvm_opts=None,
              cfr_opts=None) -> None:
    if jvm_opts is None:
        jvm_opts = []
    if cfr_opts is None:
        cfr_opts = []
    cmd = ['java'] + jvm_opts + ['-jar', cfr_jar_path, input_path,
                                 '--outputdir', output_dir]

    print("Running command:", " ".join(shlex.quote(arg) for arg in cmd))

    os.makedirs(output_dir, exist_ok=True)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: CFR exited with code", result.returncode)
        print("Stdout:", result.stdout)
        print("Stderr:", result.stderr)
        raise RuntimeError("CFR failed")
    else:
        print("CFR finished successfully.")

if __name__ == "__main__":
    # Get the absolute path to the project's root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    default_cfr_path = os.path.join(project_root, "libs", "cfr-0.152.jar")

    # The output directory is relative to the script's location
    script_dir = os.path.dirname(__file__)
    output_base_dir = os.path.join(script_dir, 'gen')

    cfr_path = input("cfr path(no '.jar'):") + '.jar'

    if not os.path.exists(cfr_path):
        print("CFR path", cfr_path, "does not exist.")
        print("Using default path:", default_cfr_path)
        cfr_path = default_cfr_path

    decompile(cfr_path,
              input_path=input("input path:"),
              output_dir=os.path.join(output_base_dir, input("output dir:")))
