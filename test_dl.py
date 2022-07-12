from utile.module_manager.deps_manager.Dependency import Dependency

package = Dependency("pypi:yt_dlp")
print("Is installed", package.provider.is_installed())
print(package.provider.download(force=True))
package = Dependency("pypi:requests")
print("Is installed", package.provider.is_installed())
print(package.provider.download(force=True))
