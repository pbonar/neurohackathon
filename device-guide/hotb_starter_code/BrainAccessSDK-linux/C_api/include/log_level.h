/**
 * @file log_level.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief Defines constants for different log levels used in the library.
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#include <stdint.h>

/**
 * @brief Log level for verbose messages.
 */
#define BA_LOG_LEVEL_VERBOSE 0

/**
 * @brief Log level for debug messages.
 */
#define BA_LOG_LEVEL_DEBUG 1

/**
 * @brief Log level for informational messages.
 */
#define BA_LOG_LEVEL_INFO 2

/**
 * @brief Log level for warning messages.
 */
#define BA_LOG_LEVEL_WARNING 3

/**
 * @brief Log level for error messages.
 */
#define BA_LOG_LEVEL_ERROR 4

/**
 * @brief Type definition for log level.
 */
typedef uint8_t ba_log_level;
