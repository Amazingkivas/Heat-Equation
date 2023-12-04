file(GLOB hdrs "*.h*" "../../headers/*.h")

add_executable(sample ../../samples/main.cpp ${hdrs})

target_include_directories(sample PUBLIC ../../headers)

set_target_properties(sample PROPERTIES RUNTIME_OUTPUT_DIRECTORY "../../interface")