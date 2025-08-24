cmake_minimum_required(VERSION 3.13)
project(flipper_alert_app C)
include($ENV{FIRMWARE_DIR}/applications/cmake/app.cmake)

app(
    NAME "SpectrumAlert"
    SOURCES application.c
    STACK_SIZE 1024
)
