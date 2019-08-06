from conans import ConanFile, CMake, tools
from shutil import copy2
import os

class DjinniConan(ConanFile):
    name = "djinni"
    version = "470"
    author = "Ralph-Gordon Paul (gordon@rgpaul.com)"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "android_ndk": "ANY", 
        "android_stl_type":["c++_static", "c++_shared"]}
    default_options = "shared=False", "android_ndk=None", "android_stl_type=c++_static"
    description = "A tool for generating cross-language type declarations and interface bindings."
    url = "https://github.com/Manromen/conan-djinni-scripts"
    license = "Apache-2.0"
    exports_sources = "cmake-modules/*", "djinni/*", "djinni.jar"

    # compile using cmake
    def build(self):
        cmake = CMake(self)
        library_folder = "%s/djinni" % self.source_folder
        cmake.verbose = True
        variants = []

        if self.settings.os == "Android":
            android_toolchain = os.environ["ANDROID_NDK_PATH"] + "/build/cmake/android.toolchain.cmake"
            cmake.definitions["CMAKE_SYSTEM_NAME"] = "Android"
            cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = android_toolchain
            cmake.definitions["ANDROID_NDK"] = os.environ["ANDROID_NDK_PATH"]
            cmake.definitions["ANDROID_ABI"] = tools.to_android_abi(self.settings.arch)
            cmake.definitions["ANDROID_STL"] = self.options.android_stl_type
            cmake.definitions["ANDROID_NATIVE_API_LEVEL"] = self.settings.os.api_level
            cmake.definitions["ANDROID_TOOLCHAIN"] = "clang"
            cmake.definitions["DJINNI_WITH_JNI"] = "ON"

        if self.settings.os == "iOS":
            ios_toolchain = "cmake-modules/Toolchains/ios.toolchain.cmake"
            cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = ios_toolchain
            cmake.definitions["DJINNI_WITH_OBJC"] = "ON"
            
            # define all architectures for ios fat library
            if "arm" in self.settings.arch:
                variants = ["armv7", "armv7s", "armv8"]

            # apply build config for all defined architectures
            if len(variants) > 0:
                archs = ""
                for i in range(0, len(variants)):
                    if i == 0:
                        archs = tools.to_apple_arch(variants[i])
                    else:
                        archs += ";" + tools.to_apple_arch(variants[i])
                cmake.definitions["CMAKE_OSX_ARCHITECTURES"] = archs

            if self.settings.arch == "x86":
                cmake.definitions["IOS_PLATFORM"] = "SIMULATOR"
            elif self.settings.arch == "x86_64":
                cmake.definitions["IOS_PLATFORM"] = "SIMULATOR64"
            else:
                cmake.definitions["IOS_PLATFORM"] = "OS"

        if self.options.shared == False:
            cmake.definitions["DJINNI_STATIC_LIB"] = "ON"

        cmake.configure(source_folder=library_folder)
        cmake.build()

        # execute ranlib for all static universal libraries (required for fat libraries)
        if self.settings.os == "iOS" and len(variants) > 0:
            if self.options.shared == False:
                for f in os.listdir(self.build_folder):
                    if f.endswith(".a") and os.path.isfile(os.path.join(self.build_folder,f)) and not os.path.islink(os.path.join(self.build_folder,f)):
                        self.run("xcrun ranlib %s" % os.path.join(self.build_folder,f))

        # we have to create the include structure ourself, because there is no install in the djinni cmakelists
        include_folder = os.path.join(self.build_folder, "include")
        os.mkdir(include_folder)
        include_djinni_folder = os.path.join(include_folder, "djinni")
        os.mkdir(include_djinni_folder)

        # copy common support lib headers
        support_lib_folder = os.path.join(self.build_folder, "djinni", "support-lib")
        for f in os.listdir(support_lib_folder):
            if f.endswith(".hpp") and not os.path.islink(os.path.join(support_lib_folder,f)):
                copy2(os.path.join(support_lib_folder,f), os.path.join(include_djinni_folder,f))

        # copy objc specific header files
        if self.settings.os == "iOS":
            include_objc_folder = os.path.join(include_djinni_folder, "objc")
            os.mkdir(include_objc_folder)
            support_lib_objc_folder = os.path.join(support_lib_folder, "objc")
            for f in os.listdir(support_lib_objc_folder):
                if f.endswith(".h") and not os.path.islink(os.path.join(support_lib_objc_folder,f)):
                    copy2(os.path.join(support_lib_objc_folder,f), os.path.join(include_objc_folder,f))

        # copy jni specific header files
        if self.settings.os == "Android":
            include_jni_folder = os.path.join(include_djinni_folder, "jni")
            os.mkdir(include_jni_folder)
            support_lib_jni_folder = os.path.join(support_lib_folder, "jni")
            for f in os.listdir(support_lib_jni_folder):
                if f.endswith(".hpp") and not os.path.islink(os.path.join(support_lib_jni_folder,f)):
                    copy2(os.path.join(support_lib_jni_folder,f), os.path.join(include_jni_folder,f))

    def package(self):
        self.copy("*", dst="include", src='include')
        self.copy("*.lib", dst="lib", src='', keep_path=False)
        self.copy("*.dll", dst="bin", src='', keep_path=False)
        self.copy("*.so", dst="lib", src='', keep_path=False)
        self.copy("*.dylib", dst="lib", src='', keep_path=False)
        self.copy("*.a", dst="lib", src='', keep_path=False)
        self.copy("djinni.jar", dst="bin", src='', keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ['include']

    def package_id(self):
        if "arm" in self.settings.arch and self.settings.os == "iOS":
            self.info.settings.arch = "AnyARM"

    def config_options(self):
        # remove android specific option for all other platforms
        if self.settings.os != "Android":
            del self.options.android_ndk
            del self.options.android_stl_type
