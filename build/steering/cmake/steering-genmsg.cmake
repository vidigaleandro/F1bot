# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "steering: 1 messages, 0 services")

set(MSG_I_FLAGS "-Isteering:/home/ubuntu/F1bot/src/steering/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(steering_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/ubuntu/F1bot/src/steering/msg/steer.msg" NAME_WE)
add_custom_target(_steering_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "steering" "/home/ubuntu/F1bot/src/steering/msg/steer.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(steering
  "/home/ubuntu/F1bot/src/steering/msg/steer.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/steering
)

### Generating Services

### Generating Module File
_generate_module_cpp(steering
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/steering
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(steering_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(steering_generate_messages steering_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/F1bot/src/steering/msg/steer.msg" NAME_WE)
add_dependencies(steering_generate_messages_cpp _steering_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(steering_gencpp)
add_dependencies(steering_gencpp steering_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS steering_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(steering
  "/home/ubuntu/F1bot/src/steering/msg/steer.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/steering
)

### Generating Services

### Generating Module File
_generate_module_eus(steering
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/steering
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(steering_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(steering_generate_messages steering_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/F1bot/src/steering/msg/steer.msg" NAME_WE)
add_dependencies(steering_generate_messages_eus _steering_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(steering_geneus)
add_dependencies(steering_geneus steering_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS steering_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(steering
  "/home/ubuntu/F1bot/src/steering/msg/steer.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/steering
)

### Generating Services

### Generating Module File
_generate_module_lisp(steering
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/steering
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(steering_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(steering_generate_messages steering_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/F1bot/src/steering/msg/steer.msg" NAME_WE)
add_dependencies(steering_generate_messages_lisp _steering_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(steering_genlisp)
add_dependencies(steering_genlisp steering_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS steering_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(steering
  "/home/ubuntu/F1bot/src/steering/msg/steer.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/steering
)

### Generating Services

### Generating Module File
_generate_module_nodejs(steering
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/steering
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(steering_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(steering_generate_messages steering_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/F1bot/src/steering/msg/steer.msg" NAME_WE)
add_dependencies(steering_generate_messages_nodejs _steering_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(steering_gennodejs)
add_dependencies(steering_gennodejs steering_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS steering_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(steering
  "/home/ubuntu/F1bot/src/steering/msg/steer.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/steering
)

### Generating Services

### Generating Module File
_generate_module_py(steering
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/steering
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(steering_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(steering_generate_messages steering_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/ubuntu/F1bot/src/steering/msg/steer.msg" NAME_WE)
add_dependencies(steering_generate_messages_py _steering_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(steering_genpy)
add_dependencies(steering_genpy steering_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS steering_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/steering)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/steering
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(steering_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/steering)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/steering
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(steering_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/steering)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/steering
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(steering_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/steering)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/steering
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(steering_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/steering)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/steering\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/steering
    DESTINATION ${genpy_INSTALL_DIR}
    # skip all init files
    PATTERN "__init__.py" EXCLUDE
    PATTERN "__init__.pyc" EXCLUDE
  )
  # install init files which are not in the root folder of the generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/steering
    DESTINATION ${genpy_INSTALL_DIR}
    FILES_MATCHING
    REGEX "${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/steering/.+/__init__.pyc?$"
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(steering_generate_messages_py std_msgs_generate_messages_py)
endif()
