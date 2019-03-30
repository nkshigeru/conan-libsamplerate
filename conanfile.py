import os
from conans import ConanFile, tools


class LibsamplerateConan(ConanFile):
    name = "libsamplerate"
    version = "0.1.9"
    license = "BSD-2-Clause"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libsamplerate here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    source_subfolder = "source_subfolder"

    def source(self):
        url = "http://www.mega-nerd.com/libsamplerate/libsamplerate-%s.tar.gz" % self.version
        tools.get(url)
        os.rename("libsamplerate-%s" % self.version, self.source_subfolder)

    def build(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            tools.replace_in_file("%s/Win32/Makefile.msvc" % self.source_subfolder, "/machine:I386", "") 
            vcvars = tools.vcvars_command(self.settings)
            self.run('%s && nmake -f Win32/Makefile.msvc libsamplerate-0.dll' % vcvars, cwd=self.source_subfolder)

    def package(self):
        src = os.path.join(self.source_subfolder, "src")
        self.copy("samplerate.h", dst="include", src=src, keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["libsamplerate-0"]

