file(GLOB hdrs "*.h*" "../../headers/*.h")
file(GLOB srcs "*.cpp" "../../src/*.cpp")

add_library(SolveHeatEquation STATIC ${srcs} ${hdrs})