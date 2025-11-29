/**
 * @file version.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief Version numbers
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#ifndef __cplusplus
#include <stdbool.h>
#endif //__cplusplus

#include "dllexport.h"
#include <stdint.h>

/**
 * @brief Struct describing version numbers
 *
 * @details Uses semantic versioning
 */
typedef struct
{
	uint8_t major; ///< API-breaking changes
	uint8_t minor; ///< Feature updates
	uint8_t patch; ///< Bugfixes
} ba_version;

#ifdef __cplusplus
extern "C"
{
#endif //__cplusplus

	/**
	 * @brief Check if versions are compatible
	 *
	 * @details Uses semantic versioning
	 *
	 * @param expected
	 * @param actual
	 * @return `true` if compatible
	 */
	BA_CORE_DLL_EXPORT bool ba_is_version_compatible(
		const ba_version* expected, const ba_version* actual) NOEXCEPT;

#ifdef __cplusplus
}
#endif //__cplusplus
