#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_template_default

if __name__ == "__main__":

    builder = build_template_default.get_builder(pure_c=True)
    builder.remove_build_if(lambda build: build.settings["compiler"] == "Visual Studio" and build.options["libsamplerate:shared"] == False)
    for build in builder.items:
        if build.settings["compiler"] == "Visual Studio":
            del build.options["libsamplerate:shared"]
    builder.run()
