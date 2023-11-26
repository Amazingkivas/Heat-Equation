add_executable(sample ../../samples/main.cpp)

target_include_directories(sample PUBLIC ../../headers)
target_link_directories(sample PUBLIC ../HeatEquationLib)
target_link_libraries(sample SolveHeatEquation)

set_target_properties(sample PROPERTIES RUNTIME_OUTPUT_DIRECTORY "../../interface")