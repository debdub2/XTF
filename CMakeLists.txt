cmake_minimum_required(VERSION 3.0.2)
project(sss_data_generator)

find_package(catkin REQUIRED COMPONENTS dynamic_reconfigure
  roscpp
  rospy
  std_msgs
  message_generation
)

add_message_files(
   FILES
   hydroacoustic_ping.msg
   channel_data.msg
)

add_service_files(
  FILES
  PlayService.srv
)

generate_messages(
   DEPENDENCIES
   std_msgs
)

generate_dynamic_reconfigure_options(
   cfg/Params.cfg
)

catkin_package(
   CATKIN_DEPENDS dynamic_reconfigure roscpp rospy message_runtime std_msgs

)

include_directories(
  include ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS src/gen.py src/__main__.py DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

