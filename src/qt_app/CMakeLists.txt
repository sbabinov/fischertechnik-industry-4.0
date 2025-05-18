cmake_minimum_required(VERSION 3.16)

project(qt_app VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Quick Widgets)

qt_standard_project_setup(REQUIRES 6.8)

set(app_icon_resource_windows "${CMAKE_CURRENT_SOURCE_DIR}/images/icon.png")

qt_add_executable(appqt_app
  main.cpp
  ${app_icon_resource_windows}
)

qt_add_qml_module(appqt_app
  URI qt_app
  VERSION 1.0
  QML_FILES
    Main.qml
    Menu.qml
    AutoMode.qml
    About.qml
    Header.qml
    Footer.qml
    BackButton.qml
    ManualMode.qml
    Settings.qml
  RESOURCES
    images/german.png
    images/logo.png
    images/russian.png
    images/american.png
    images/wallpaper.jpg
    images/logo1c.png
    images/command.png
    images/wallpaper1.jpg
    images/icon.png
  SOURCES
    network_manager.hpp
    network_manager.cpp
    storage_monitor.hpp
    storage_monitor.cpp
)

set_target_properties(appqt_app PROPERTIES
  MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
  MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
  MACOSX_BUNDLE TRUE
  WIN32_EXECUTABLE TRUE
)

target_link_libraries(appqt_app
  PRIVATE Qt6::Quick
  PRIVATE Qt6::Widgets
)

include(GNUInstallDirs)
install(TARGETS appqt_app
  BUNDLE DESTINATION .
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
