# A util CLI to easily package modules,
# To use like that
# py utile-module.py package C:/path/to/module/directory/
# It will create a directory named packaged-module, and a directory named like the current version of the module
# In it will be a packaged.module file (the packaged module),
# As well as a minified version of the manifest.json file
# ===
# As a second argument, you can also pass the destination of the packaged module
import utile
import fire
import os
import utile.module_manager.packager
import json


class Packager:
    def package(self, path: str, output_directory: str = None, force: bool = False):
        print("Loading...")
        real_path = os.path.realpath(path)
        
        if output_directory:
            packaged_module_directory = os.path.realpath(output_directory)
        else:
            packaged_module_directory = os.path.realpath(os.path.join(real_path, "packaged-module"))
        
        manifest_file_path = os.path.join(real_path, "manifest.json")
        with open(manifest_file_path, "r") as f:
            content = json.load(f)
        dest_dir = os.path.join(packaged_module_directory, content["version"])
        if os.path.isdir(dest_dir):
            print("A module is already packaged at {}".format(dest_dir))
            if force:
                print("--force present, continuing anyway")
            else:
                print("Aborting. Add the --force flag to package the module anyway")
                return
        minified_manifest_path = os.path.join(dest_dir, "manifest.json")
        real_output_file_path = os.path.join(dest_dir, "packaged.module")
        
        print("Packaging...")
        packaged = utile.module_manager.packager.package(real_path)
        
        os.makedirs(dest_dir, exist_ok=True)
        
        minified_manifest = json.dumps(content, separators=(',', ':'))
        with open(minified_manifest_path, "w") as f:
            f.write(minified_manifest)
        with open(real_output_file_path, "w") as f:
            f.write(packaged)
            
        print("Module packaged to {}".format(dest_dir))
        

if __name__ == "__main__":
    fire.Fire(Packager)
