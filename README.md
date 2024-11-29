# stm32-with-cpp-20

该项目是用于自动配置STM32CubeMX生成的CMake项目，使其适配c++20标准。同时，内置由[creeper](https://github.com/creeper5820)开发的[`stm_hal`](https://github.com/creeper5820/stm32_hal)库，用于简化开发。

## 依赖

- [STM32CubeMX v6.12.0](https://www.st.com/en/development-tools/stm32cubemx.html)
- [Arm GNU Toolchain](https://developer.arm.com/downloads/-/gnu-rm)
- [VS Code](https://code.visualstudio.com/download)
- [CMake](https://cmake.org/download/)

## 使用

``` shell
chmod +x ./stm32-with-cpp-20.py
./stm32-with-cpp-20.py <project_path>
cd <project_path>
mkdir build
cd build
cmake ..
make
```
