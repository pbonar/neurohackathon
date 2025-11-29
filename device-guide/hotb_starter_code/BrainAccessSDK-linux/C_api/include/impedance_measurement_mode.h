/**
 * @file impedance_measurement_mode.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief Impedance measurement mode constants
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#include <stdint.h>

#define BA_IMPEDANCE_MEASUREMENT_MODE_OFF     0 ///< No active impedance measurement
#define BA_IMPEDANCE_MEASUREMENT_MODE_HZ_7_8  1 ///< 7.8 Hz wave
#define BA_IMPEDANCE_MEASUREMENT_MODE_HZ_31_2 2 ///< 31.2 Hz wave
#define BA_IMPEDANCE_MEASUREMENT_MODE_DR_DIV4                                  \
	3 ///< Wave frequency of sample_rate/4

typedef uint8_t ba_impedance_measurement_mode;
