import os
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration

required_conan_version = ">=1.33.0"

class CompositeConan(ConanFile):
    python_requires = "base_conanfile/v0.2.0@jgsogo/stable"
    python_requires_extend = "base_conanfile.BaseCMakeConanfile"
    
    name = "composite"
    homepage = "https://github.com/jgsogo/composite"
    description = "Data structures with composite nodes"
    topics = ("cpp20", "tree", "graph")
    license = "MIT"

    def validate(self):
        self._validate_cppstd("20")

    def package_id(self):
        self.info.header_only()
