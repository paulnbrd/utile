from functools import cache
import py_compile
import zipfile
import requests
from utile.module_manager.deps_manager.Provider import Provider
import utile.utils
import os
import io
import importlib.util
import termcolor


class PyPiProvider(Provider):
    def __init__(self, package_name: str) -> None:
        self.package_name = package_name
        
    def is_installed(self):
        if os.path.isdir(
            os.path.join(utile.utils.deps_dir, self.package_name)
        ):
            return True
        try:
            spec = importlib.util.find_spec(self.package_name)
            if spec is not None:
                return True
        except ImportError:
            pass
        return False
    
    def _get_download_url(self):
        pass
    
    def _get_package_json_url(self):
        url = "https://pypi.org/pypi/{}/json".format(self.package_name)
        return url
    
    @cache
    def _get_package_json(self):
        try:
            url = self._get_package_json_url()
            req = requests.get(url)
            req.raise_for_status()
            return req.json()
        except:
            return None
    
    def _package_exists(self):
        json = self._get_package_json()
        if json is None:
            return False
        return True
    
    def can_install(self) -> bool:
        if not self._package_exists():
            return False
        json = self._get_package_json()
        urls = json.get("urls", [])
        url = None
        for url_data in urls:
            if url_data["url"].endswith(".whl"):
                url = url_data["url"]
                break
        if url is None:
            return False
        return True
        
    def download(self, force: bool = False):
        if self.is_installed() and not force:
            return True
        print("Downloading package {}".format(termcolor.colored(self.package_name, "green")))
        try:
            if not self._package_exists():
                return False
            json = self._get_package_json()
            
            urls = json.get("urls", [])
            url = None
            for url_data in urls:
                if url_data["url"].endswith(".whl"):
                    url = url_data["url"]
                    break
            if url is None:
                return False
            result = self._install_from_url(url)
            if not result:
                print(termcolor.colored("Download failed", "red"))
                return False
            print(termcolor.colored("Download successful", "green"))
            return True
        except Exception as e:
            print(e)
            return False
        except KeyboardInterrupt as e:
            print(termcolor.colored("[User aborted]", "red"))
            return False
        
    def _install_from_url(self, url: str):
        with utile.utils.create_spinner() as spinner:
            spinner.text = "Downloading package {}..." \
                .format(termcolor.colored(self.package_name, "green"))
            resp = requests.get(url, stream=True)
            content = b""
            resp.raise_for_status()
            total_length = int(resp.headers["Content-Length"])
            read_total = 0
            for s in resp.iter_content(4096):
                content += s
                read_total += len(s)
                spinner.text = "Downloading package {}... ({}%)" \
                    .format(
                        termcolor.colored(self.package_name, "green"),
                        str(round(read_total / total_length * 100, 1))
                    )
            zip = zipfile.ZipFile(io.BytesIO(content))
            
            spinner.text = "Installing..."
            package_name_to_find = self.package_name
            starting_value = package_name_to_find + "/"
            files: list[zipfile.ZipInfo] = []  # Contains files in zipfile for this package
            for file in zip.filelist:
                if file.filename.startswith(starting_value):
                    files.append(file)
            
            if len(files) == 0:
                # No files found, cannot install package
                return False
            # Continue whl installation
            total_number_of_files = len(files)
            for current_file_index, file in enumerate(files):
                filepath = utile.utils.deps_dir
                zip.extract(file, filepath)
                full_filepath = os.path.join(filepath, file.filename)
                if os.path.isfile(full_filepath):
                    # If it is a file ending in .py, compile it
                    if full_filepath.endswith(".py"):
                        percentage = current_file_index/total_number_of_files * 100
                        percentage = round(percentage, 1)
                        spinner.text = "[{}%] Compiling {}...".format(
                            percentage,
                            termcolor.colored(file.filename, "green")
                        )
                        py_compile.compile(full_filepath, full_filepath + "c", optimize=2)
                        os.remove(full_filepath)
        return True


class Dependency:
    def __init__(self, package: str) -> None:
        """Represents a dependency that can be installed (and compiled)

        Args:
            package (str): Must be a two part dep, e.g.: pypi:yt-dlp
        """
        self.str_provider, self.package_name = package.split(":")
        
        if self.str_provider == "pypi":
            self.provider = PyPiProvider(self.package_name)
        else:
            raise RuntimeError("Could not resolve dependency provider {}".format(self.str_provider))
