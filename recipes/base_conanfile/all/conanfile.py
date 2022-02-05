import os
from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class BaseConanfile(object):
    url = "https://github.com/jgsogo/conan-recipes"
    settings = "os", "arch", "compiler", "build_type"

    @property
    def _compilers_minimum_version(self):
        return {"20": {
            "gcc": "8",
            "clang": "9",
            "apple-clang": "12",
            "Visual Studio": "16.11",
        }}

    def _validate_cppstd(self, cppstd):
        if self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, cppstd)

        def lazy_lt_semver(v1, v2):
            lv1 = [int(v) for v in v1.split(".")]
            lv2 = [int(v) for v in v2.split(".")]
            min_length = min(len(lv1), len(lv2))
            return lv1[:min_length] < lv2[:min_length]

        minimum_version = self._compilers_minimum_version[cppstd].get(str(self.settings.compiler), False)
        if minimum_version and lazy_lt_semver(str(self.settings.compiler.version), minimum_version):
            raise ConanInvalidConfiguration("{} requires C++{}, which your compiler does not support.".format(cppstd, self.name))

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join(self._source_subfolder, "src"))
        self.copy("*.hpp", dst="include", src=os.path.join(self._source_subfolder, "src"))
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)


class PyReq(ConanFile):
    name = "base_conanfile"
    version = "v0.1.0"