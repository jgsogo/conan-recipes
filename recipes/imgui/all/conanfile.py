from conans import ConanFile, CMake, tools
import os

required_conan_version = ">=1.33.0"


class IMGUIConan(ConanFile):
    name = "imgui"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/ocornut/imgui"
    description = "Bloat-free Immediate Mode Graphical User interface for C++ with minimal dependencies"
    topics = ("conan", "imgui", "gui", "graphical")
    license = "MIT"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "add_misc": [True, False],  # There are some utilities in the `misc` subdirectory
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "add_misc": True,
    }

    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)
        # Ensure we take into account export_headers
        tools.replace_in_file(
            os.path.join(self._source_subfolder, "imgui.h"),
            "#ifdef IMGUI_USER_CONFIG",
            "#ifdef IMGUI_EXPORT_HEADERS\n#include IMGUI_EXPORT_HEADERS\n#endif\n\n#ifdef IMGUI_USER_CONFIG"
        )

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["ADD_MISC"] = self.options.add_misc
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self._source_subfolder)
        use_backends = 'docking' in self.version or tools.Version(self.version) >= "1.80"
        backends_folder = os.path.join(
            self._source_subfolder,
            "backends" if use_backends else "examples"
        )
        self.copy(pattern="imgui_impl_*",
                  dst=os.path.join("res", "bindings"),
                  src=backends_folder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["imgui"]
        self.cpp_info.defines.append("IMGUI_EXPORT_HEADERS=\"imgui_export_headers.h\"")
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("m")
        self.cpp_info.srcdirs = [os.path.join("res", "bindings")]

        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH env var with : {}".format(bin_path))
        self.env_info.PATH.append(bin_path)
