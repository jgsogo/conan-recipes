import os
from conans import ConanFile, tools

required_conan_version = ">=1.33.0"

class DrawablesConan(ConanFile):
    python_requires = "base_conanfile/v0.2.0@jgsogo/stable"
    python_requires_extend = "base_conanfile.BaseCMakeConanfile"

    name = "drawables"
    homepage = "https://github.com/jgsogo/drawables"
    description = "Parsers and library loader"
    topics = ("cpp20", "parser",)
    license = "MIT"

    default_options = {
        'magnum-plugins:shared_plugins': False,
    }

    def validate(self):
        self._validate_cppstd("20")

    def requirements(self):
        self.requires("render_context/v0.2.9@jgsogo/stable")
        self.requires("rapidxml/1.13")
        self.requires("spdlog/1.9.2")
        self.requires("magnum-plugins/2020.06")
        self.requires("magnum/2020.06@jgsogo/stable", override=True)

    def package_info(self):
        self.cpp_info.requires = ['render_context::render_context', 'rapidxml::rapidxml', 'spdlog::spdlog']
