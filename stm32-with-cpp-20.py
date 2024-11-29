#! /usr/bin/python3
import shutil
import os, re
import sys

def refactor_dir(dir:str)->None:
    filelist = os.listdir(dir) 
    
    hal_dir = os.path.join(dir, 'hal')
    if not os.path.exists(hal_dir):
        os.mkdir(hal_dir)

        for file in filelist:
            if file != "hal":
                old_path = os.path.join(dir, file)
                shutil.move(old_path, os.path.join(dir, 'hal', file))

def new_cmakelists(dir:str)->None:
    path  = os.path.join(dir, 'CMakeLists.txt')
    if os.path.exists(path):
        os.remove(path)

    shutil.copyfile(os.path.join(dir,'hal' , 'CMakeLists.txt'),path)
    
    with open(path, "r", encoding="utf-8") as f1,open("%s.bak" % path, "w", encoding="utf-8") as f2:
        for line in f1:
            line = re.sub('cmake/','hal/cmake/',line)
            line = line.replace('set(CMAKE_C_EXTENSIONS ON)\n','set(CMAKE_C_EXTENSIONS ON)\nset(CMAKE_CXX_STANDARD_REQUIRED ON)\nset(CMAKE_CXX_STANDARD 20)\n')
            line = line.replace('# Add include paths',
"""
file(GLOB_RECURSE PROJECT_CPP "src/*.cc")

# Add sources to executable
target_sources(${CMAKE_PROJECT_NAME} PRIVATE
    # Add user sources here
    ${PROJECT_CPP}
)

# Add include paths"""
                                )
            f2.write(line)
        f2.write('\ninclude_directories(src)\n')
    os.remove(path)
    os.rename("%s.bak" % path, path)


def new_ld(dir:str)->None:
    path = os.path.join(dir, 'hal/cmake/gcc-arm-none-eabi.cmake')
    with open(path, "r", encoding="utf-8") as f1,open("%s.bak" % path, "w", encoding="utf-8") as f2:
        for line in f1:
            line = line.replace(r'${CMAKE_SOURCE_DIR}/STM32',r'${CMAKE_SOURCE_DIR}/hal/STM32')
            f2.write(line)
    os.remove(path)
    os.rename("%s.bak" % path, path)

entrypoint_hh = """
#pragma once

#ifdef __cplusplus
extern "C" {
#endif

void entrypoint();

#ifdef __cplusplus
}
#endif
"""

entrypoint_cc = """
#include "entrypoint.hh"

void entrypoint() {
  while (true) {
  }
}
"""

def add_sources(dir:str)->None:
    dir = os.path.join(dir, 'src')
    if not os.path.exists(dir):
        os.mkdir(dir)

    path = os.path.join(dir, 'entrypoint.cc')
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(entrypoint_cc)

    path = os.path.join(dir, 'entrypoint.hh')
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(entrypoint_hh)

def add_main(dir:str)->None:
    path = os.path.join(dir, 'hal/Core/Src/main.c')
    
    with open(path, "r", encoding="utf-8") as f1,open("%s.bak" % path, "w", encoding="utf-8") as f2:
        for line in f1:
            line = line.replace('/* USER CODE END Includes */', '#include "entrypoint.hh"\n/* USER CODE END Includes */')
            line = line.replace('/* USER CODE END 2 */', '\tentrypoint();\n/* USER CODE END 2 */')
            f2.write(line)
    os.remove(path)
    os.rename("%s.bak" % path, path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception('No project specified')
    
    dir = sys.argv[1]

    if not os.path.exists(dir):
        raise FileNotFoundError('Project not found')
    
    refactor_dir(dir)
    
    new_cmakelists(dir)

    new_ld(dir)

    add_sources(dir)

    add_main(dir)