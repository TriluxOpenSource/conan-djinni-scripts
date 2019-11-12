[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Android status](https://github.com/rgpaul/conan-curl-scripts/workflows/Android/badge.svg)
![iOS status](https://github.com/rgpaul/conan-curl-scripts/workflows/iOS/badge.svg)

# Conan djinni

This repository contains a conan receipe that can be used to build djinni packages.

For Infos about djinni please visit [Github](https://github.com/dropbox/djinni).  
The library is licensed under the [Apache License](https://github.com/dropbox/djinni/blob/master/LICENSE).  
This repository is licensed under the [MIT License](LICENSE).

## Android

The environmental `ANDROID_NDK_PATH` must be set to the path of the android ndk.

To create a package for Android you can run the following commands like:

`export ANDROID_NDK_PATH='/opt/android-ndks/android-ndk-r20'`
`conan create . djinni/470@rgpaul/stable -s os=Android -s os.api_level=21 -s compiler=clang -s compiler.version=8.0 -s compiler.libcxx=libc++ -s build_type=Release -o android_ndk=r20 -o android_stl_type=c++_static -s arch=x86_64`

### Requirements

* [CMake](https://cmake.org/)
* [Conan](https://conan.io/)
* [Android NDK r20](https://developer.android.com/ndk/downloads/)

## iOS

To create a package for iOS you can run the conan command like this:

`conan create . djinni/470@rgpaul/stable -s os=iOS -s os.version=12.2 -s arch=armv8 -s build_type=Release -o shared=False`

### Requirements

* [CMake](https://cmake.org/)
* [Conan](https://conan.io/)
* [Xcode](https://developer.apple.com/xcode/)
