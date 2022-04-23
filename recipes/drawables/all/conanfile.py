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

    def validate(self):
        self._validate_cppstd("20")

    def requirements(self):
        self.require("render_context/v0.2.9@jgsogo/stable")
        self.require("rapidxml/1.13")

    def package_info(self):
        self.cpp_info.requires = ['render_context::render_context', 'rapidxml::rapidxml']
