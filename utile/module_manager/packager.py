import importlib
import os
import sys
import base64
import json
import py_compile


class InvalidModuleError(Exception):
    def __init__(self, message) -> None:
        self.message = message
    
class ModuleDecodeError(Exception):
    def __init__(self, message) -> None:
        self.message = message

class ModuleInstallError(Exception):
    def __init__(self, message) -> None:
        self.message = message
        

def package(module_directory: str, dirty_module_check: bool = False):
    if not os.path.isdir(module_directory):
        raise InvalidModuleError("Cannot package module: invalid directory {}".format(module_directory))
    
    manifest_path = os.path.join(module_directory, "manifest.json")
    if not os.path.isfile(manifest_path):
        raise InvalidModuleError("Could not find manifest ({})".format(module_directory))
    entrypoint_path = os.path.join(module_directory, "module.py")
    if not os.path.isfile(entrypoint_path):
        raise InvalidModuleError("Could not find module entrypoint ({})".format(entrypoint_path))
    if dirty_module_check:
        sys.path.append(module_directory)
        module = importlib.import_module("module")
        try:
            print(getattr(module, "MODULE"))
        except AttributeError:
            raise InvalidModuleError("Entrypoint has no object named MODULE")
    else:
        print("[WARNING] MODULE object presence not checked")
    
    def scan(root, directories, files):
        result = []
        print("* Scanning {}...".format(root))
        for file in files:
            print("* Adding {}...".format(file))
            result.append(os.path.join(os.path.join(root, file)))
        for directory in directories:
            if directory == "__pycache__":
                print("* Ignoring __pycache__ directory")
                continue
            for r, d, f in os.walk(os.path.join(root, directory)):
                result.extend(scan(
                    r, d, f
                ))
        return result
    
    walk = os.walk(module_directory)
    packaged = {}
    to_package = []
    for root, dirs, files in walk:
        to_package.extend(scan(root, dirs, files))
    relative_paths = [os.path.relpath(file, module_directory) for file in to_package]
    
    for file in relative_paths:
        print("* Packaging {}...".format(file))
        abs_path = os.path.join(module_directory, file)
        try:
            with open(abs_path, "rb") as f:
                content = f.read()
                packaged[file] = base64.b64encode(content).hex()
        except Exception as e:
            raise InvalidModuleError(str(e))
            
    encoded = json.dumps(packaged).encode()
    return base64.b64encode(encoded).hex()

    
def unpackage(packaged: str, write_package_in_dir: str = None):
    print("* Unpackaging...")
    try:
        json_encoded = base64.b64decode(bytes.fromhex(packaged))
        decoded_json = json.loads(json_encoded)
        
        for key, encoded in decoded_json.items():
            decoded = base64.b64decode(bytes.fromhex(encoded))
            decoded_json[key] = decoded
    except Exception as e:
        raise ModuleDecodeError(str(e))

    if write_package_in_dir is not None:
        print("* Installing...")
        real_path = os.path.realpath(write_package_in_dir)
        parent_dir = os.path.dirname(real_path)
        if not os.path.isdir(parent_dir):
            raise ModuleInstallError("Parent directory doesn't exist on install")
        if os.path.isdir(real_path):
            raise ModuleInstallError("Target directory already exists")
        os.makedirs(real_path)
        for file, content in decoded_json.items():
            real_file_path = os.path.join(real_path, file)
            os.makedirs(os.path.dirname(real_file_path), exist_ok=True)
            with open(real_file_path, "wb") as f:
                f.write(content)
            # Now we compile the file
            if real_file_path.endswith(".py"):
                print("* Compiling {}...".format(os.path.basename(real_file_path)))
                py_compile.compile(real_file_path, real_file_path + "c")
                os.remove(real_file_path)
    
    return decoded_json


if __name__ == "__main__":
    packaged = package("modules/cloudflare")
    print(packaged)
    print(40*"=")
    unpackage(packaged, "_module_cloudflare")
