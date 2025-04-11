cmake_minimum_required(VERSION 3.16)

project(qt_app VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Quick)

qt_standard_project_setup(REQUIRES 6.8)

qt_add_executable(appqt_app
    main.cpp
)

qt_add_qml_module(appqt_app
    URI qt_app
    VERSION 1.0
    QML_FILES
        Main.qml
        Menu.qml
        MenuLogo.qml
        AutoLogo.qml
    RESOURCES
        images/germany.png
        images/icon.png
        images/logo.png
        images/russia.png
        images/usa.png
        images/wallpaper.jpg
        images/logo1c.png
)

# Qt for iOS sets MACOSX_BUNDLE_GUI_IDENTIFIER automatically since Qt 6.1.
# If you are developing for iOS or macOS you should consider setting an
# explicit, fixed bundle identifier manually though.
set_target_properties(appqt_app PROPERTIES
#    MACOSX_BUNDLE_GUI_IDENTIFIER com.example.appqt_app
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

target_link_libraries(appqt_app
    PRIVATE Qt6::Quick
)

include(GNUInstallDirs)
install(TARGETS appqt_app
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
