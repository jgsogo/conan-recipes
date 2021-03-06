import os
from conans import ConanFile

required_conan_version = ">=1.33.0"

class RenderContextConan(ConanFile):
    python_requires = "base_conanfile/v0.2.0@jgsogo/stable"
    python_requires_extend = "base_conanfile.BaseCMakeConanfile"

    name = "render_context"
    homepage = "https://github.com/jgsogo/render_context"
    description = "Utilities to draw elements using Magnum with ImGUI integration"
    topics = ("cpp20", "magnum", "imgui")
    license = "MIT"

    def validate(self):
        self._validate_cppstd("20")

    def requirements(self):
        self.requires("imgui/cci.20211117+docking@jgsogo/stable")
        self.requires("magnum/2020.06@jgsogo/stable")
        self.requires("magnum-integration/2020.06")

    def package_info(self):
        self.cpp_info.defines.append("IMGUI_USER_CONFIG=\"{}\"".format(str(os.path.join(self.package_folder, "include", "render", "imgui", "imconfig.h"))))
        self.cpp_info.requires = ['magnum::magnum_main', 'imgui::imgui', 'magnum-integration::imgui']
        self.cpp_info.libs = ['units', 'render_imgui']
