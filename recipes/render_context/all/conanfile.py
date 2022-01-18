import os
from conans import ConanFile, tools, CMake
from conans.errors import ConanInvalidConfiguration

required_conan_version = ">=1.33.0"

class RenderContextConan(ConanFile):
    python_requires = "base_conanfile/v0.1.0@jgsogo/stable"
    python_requires_extend = "base_conanfile.BaseConanfile"

    name = "render_context"
    homepage = "https://github.com/jgsogo/render_context"
    description = "Utilities to draw elements using Magnum with ImGUI integration"
    topics = ("cpp20", "magnum", "imgui")
    license = "MIT"

    exports_sources = ["CMakeLists.txt",]
    generators = "cmake", "cmake_find_package"

    _cmake = None

    def validate(self):
        self._validate_cppstd("20")

    def requirements(self):
        self.requires("imgui/cci.20211117+docking@jgsogo/stable")
        self.requires("magnum/2020.06@jgsogo/stable")
        self.requires("magnum-integration/2020.06")
        self.requires("catch2/2.13.7")

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package_info(self):
        self.cpp_info.defines.append("IMGUI_USER_CONFIG=\"{}\"".format(str(os.path.join(self.package_folder, "include", "render", "imgui", "imconfig.h"))))
