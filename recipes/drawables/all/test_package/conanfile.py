import os
from conans import ConanFile


class TestPackageConan(ConanFile):
    python_requires = "base_conanfile/v0.2.0@jgsogo/stable"
    python_requires_extend = "base_conanfile.BaseCMakeTestPackageConanfile"

    generators = "cmake", "cmake_find_package_multi"
    # NOTE: If using 'cmake_find_package' + 'conan_basic_setup(TARGETS)' some of the targets' properties are being overriden and
    #       the targets created by 'cmake_find_package' will be modified!!!! Here it happens that via conan_basic_setup(TARGETS)
    #       additional libraries are added to Magnum::Magnum and those libraries cannot be found without adding extra library
    #       folders (exactly the problem we fixed with the 'conan-bugfix-global-target.cmake' build-module in magnum recipe)
