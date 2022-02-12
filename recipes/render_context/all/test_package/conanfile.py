import os
from conans import ConanFile, CMake, tools


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package_multi"
    # NOTE: If using 'cmake_find_package' + 'conan_basic_setup(TARGETS)' some of the targets' properties are being overriden and
    #       the targets created by 'cmake_find_package' will be modified!!!! Here it happens that via conan_basic_setup(TARGETS)
    #       additional libraries are added to Magnum::Magnum and those libraries cannot be found without adding extra library
    #       folders (exactly the problem we fixed with the 'conan-bugfix-global-target.cmake' build-module in magnum recipe)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self):
            bin_path = os.path.join("bin", "test_package")
            self.run(bin_path, run_environment=True)
