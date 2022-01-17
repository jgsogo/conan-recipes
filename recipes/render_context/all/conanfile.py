import os
from conans import ConanFile, tools, CMake
from conans.errors import ConanInvalidConfiguration

required_conan_version = ">=1.33.0"

class RenderContextConan(ConanFile):
    name = "render_context"
    url = "https://github.com/jgsogo/conan-recipes"
    homepage = "https://github.com/jgsogo/render_context"
    description = "Utilities to draw elements using Magnum with ImGUI integration"
    topics = ("cpp20", "magnum", "imgui")
    license = "MIT"

    settings = "os", "arch", "compiler", "build_type"
    exports_sources = ["CMakeLists.txt",]
    generators = "cmake", "cmake_find_package"

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _compilers_minimum_version(self):
        return {
            "gcc": "8",
            "clang": "9",
            "apple-clang": "12",
            "Visual Studio": "16.11",
        }

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, "20")

        def lazy_lt_semver(v1, v2):
            lv1 = [int(v) for v in v1.split(".")]
            lv2 = [int(v) for v in v2.split(".")]
            min_length = min(len(lv1), len(lv2))
            return lv1[:min_length] < lv2[:min_length]

        minimum_version = self._compilers_minimum_version.get(str(self.settings.compiler), False)
        if minimum_version and lazy_lt_semver(str(self.settings.compiler.version), minimum_version):
            raise ConanInvalidConfiguration("{} requires C++20, which your compiler does not support.".format(self.name))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)

    def requirements(self):
        self.requires("imgui/cci.20211117+docking@jgsogo/stable")
        self.requires("magnum/2020.06@jgsogo/stable")
        self.requires("magnum-integration/2020.06")
        self.requires("catch2/2.13.7")

        # Some overrides
        self.requires("libalsa/1.2.5.1")

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("*.hpp", dst="include", src=os.path.join(self._source_subfolder, "src"))
        self.copy("*.h", dst="include", src=os.path.join(self._source_subfolder, "src"))
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.defines.append("IMGUI_USER_CONFIG=\"{}\"".format(str(os.path.join(self.package_folder, "include", "render", "imgui", "imconfig.h"))))
