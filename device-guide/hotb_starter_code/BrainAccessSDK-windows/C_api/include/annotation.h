/**
 * @file annotation.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief Annotation
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#include <stddef.h>

/**
 * @brief Struct containing annotation information
 */
typedef struct
{
	size_t timestamp; ///< Sample number corresponding to the time the
					  ///< annotation was recorded
	char* annotation; ///< Annotation text
} ba_annotation;
