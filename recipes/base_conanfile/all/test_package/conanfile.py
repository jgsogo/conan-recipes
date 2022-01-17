from conans import ConanFile


class TestPackage(ConanFile):
    def test(self):
        self.output.info("Just to run 'conan test' for this reference")
