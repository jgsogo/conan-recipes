import os
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration

required_conan_version = ">=1.33.0"

class CompositeConan(ConanFile):
    python_requires = "base_conanfile/v0.1.0@jgsogo/stable"
    python_requires_extend = "base_conanfile.BaseConanfile"

    name = "composite"
    homepage = "https://github.com/jgsogo/composite"
    description = "Data structures with composite nodes"
    topics = ("cpp20", "tree", "graph")
    license = "MIT"

    def validate(self):
        self._validate_cppstd("20")

    def package_id(self):
        self.info.header_only()

    def package(self):
        self.copy("*.hpp", dst="include", src=os.path.join(self._source_subfolder, "src"))
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
