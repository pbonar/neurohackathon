/**
 * @file stream_rate.h
 * @brief Defines data stream rate constants and type for BA core.
 *
 * This header provides symbolic constants for various data stream rates (in Hz)
 * and a typedef for the data stream rate type used throughout the BA core
 * system.
 */

#pragma once

#include <stdint.h>

#define BA_DATA_STREAM_RATE_16K_HZ 0 ///< 16 kHz data stream rate
#define BA_DATA_STREAM_RATE_8K_HZ  1 ///< 8 kHz data stream rate
#define BA_DATA_STREAM_RATE_4K_HZ  2 ///< 4 kHz data stream rate
#define BA_DATA_STREAM_RATE_2K_HZ  3 ///< 2 kHz data stream rate
#define BA_DATA_STREAM_RATE_1K_HZ  4 ///< 1 kHz data stream rate
#define BA_DATA_STREAM_RATE_500_HZ 5 ///< 500 Hz data stream rate
#define BA_DATA_STREAM_RATE_250_HZ 6 ///< 250 Hz data stream rate

typedef uint8_t ba_data_stream_rate;
