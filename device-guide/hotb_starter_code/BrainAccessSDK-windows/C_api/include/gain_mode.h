/**
 * @file gain_mode.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief Gain mode
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#include "dllexport.h"
#include <stdint.h>

#define BA_GAIN_MODE_X1      0    ///< 1x gain
#define BA_GAIN_MODE_X2      1    ///< 2x gain
#define BA_GAIN_MODE_X4      2    ///< 4x gain
#define BA_GAIN_MODE_X6      3    ///< 6x gain
#define BA_GAIN_MODE_X8      4    ///< 8x gain
#define BA_GAIN_MODE_X12     5    ///< 12x gain
#define BA_GAIN_MODE_UNKNOWN 0xFF ///< Unknown gain

/**
 * @brief Gain mode type
 */
typedef uint8_t ba_gain_mode;

#ifdef __cplusplus
extern "C"
{
#endif

	/**
	 * @brief Converts gain mode to integer multiplier representing the gain
	 * mode (ex: X12 returns 12)
	 *
	 * @param g Gain mode to convert to multiplier
	 * @return Integer multiplier representing the gain mode (ex: X12 returns
	 * 12)
	 */
	BA_CORE_DLL_EXPORT int ba_gain_mode_to_multiplier(ba_gain_mode g) NOEXCEPT;

	/**
	 * @brief Attempts to convert multiplier to gain mode (ex: 12 returns X12)
	 *
	 * @param g Multiplier to convert to gain mode
	 * @return Gain mode
	 */
	BA_CORE_DLL_EXPORT ba_gain_mode ba_multiplier_to_gain_mode(int g) NOEXCEPT;

#ifdef __cplusplus
}
#endif
