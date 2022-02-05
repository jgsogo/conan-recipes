import os
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration

required_conan_version = ">=1.33.0"

class TemplateCppProjectConan(ConanFile):
    python_requires = "base_conanfile/v0.1.0@jgsogo/stable"
    python_requires_extend = "base_conanfile.BaseConanfile"

    name = "template-cpp-project"
    homepage = "https://github.com/jgsogo/template-cpp-project"
    description = "Recipe for the template repository"
    topics = ("cpp20", "template")
    license = "MIT"

    def validate(self):
        self._validate_cppstd("20")
