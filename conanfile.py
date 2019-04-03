import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment


class LibsamplerateConan(ConanFile):
    name = "libsamplerate"
    version = "0.1.9"
    license = "BSD-2-Clause"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libsamplerate here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    source_subfolder = "libsamplerate-%s" % version

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared

    def source(self):
        url = "http://www.mega-nerd.com/libsamplerate/libsamplerate-%s.tar.gz" % self.version
        tools.get(url)

    def build(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            tools.replace_in_file("%s/Win32/Makefile.msvc" % self.source_subfolder, "/machine:I386", "") 
            vcvars = tools.vcvars_command(self.settings)
            self.run('%s && nmake -f Win32/Makefile.msvc libsamplerate-0.dll' % vcvars, cwd=self.source_subfolder)
        else:
            with tools.chdir(self.source_subfolder):
                env_build = AutoToolsBuildEnvironment(self)
                def option_value(b):
                    return "yes" if b else "no"
                args = [
                    "--enable-shared=" + option_value(self.options.shared),
                    "--enable-static=" + option_value(not self.options.shared),
                ]
                env_build.configure(args=args)
                env_build.make()
                env_build.install()

    def package(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            src = os.path.join(self.source_subfolder, "src")
            self.copy("samplerate.h", dst="include", src=src, keep_path=False)
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["libsamplerate-0"]
        else:
            self.cpp_info.libs = ["samplerate"]
