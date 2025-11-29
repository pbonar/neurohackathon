/**
 * @file eeg_channel.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief EEG data stream channel ID constants
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#include <stdint.h>

/**
 * @brief Type for representing EEG data stream channel IDs
 */
typedef uint16_t ba_eeg_channel;
/**
 * @brief The number of the sample starting from 0 at the stream start
 *
 * @details Data type: `size_t`
 */
#define BA_EEG_CHANNEL_ID_SAMPLE_NUMBER 0

/**
 * @brief EEG electrode measurement value (uV)
 *
 * @details Data type: `double`
 */
#define BA_EEG_CHANNEL_ID_ELECTRODE_MEASUREMENT 1

/**
 * @brief Whether the positive (P) electrode is making contact with the
 * skin
 *
 * @details Data type: `bool`
 */
#define BA_EEG_CHANNEL_ID_ELECTRODE_CONTACT_P 513

/**
 * @brief Whether the electrode is making contact with the skin
 *
 * @details Data type: `bool`
 *
 * If the device has separate P and N electrodes, the value will be true only if
 * both electrodes are making contact.
 */
#define BA_EEG_CHANNEL_ID_ELECTRODE_CONTACT 1025

/**
 * @brief Whether the negative (N) electrode is making contact with the
 * skin
 *
 * @details Data type: `bool`
 */
#define BA_EEG_CHANNEL_ID_ELECTRODE_CONTACT_N 1537

/**
 * @brief Digital IO pin state
 *
 * @details Data type: `bool`
 */
#define BA_EEG_CHANNEL_ID_DIGITAL_INPUT 2049

/**
 * @brief Gyroscope value
 *
 * @details Data type: `float`
 */
#define BA_EEG_CHANNEL_ID_GYROSCOPE 2497

/**
 * @brief Accelerometer value
 *
 * @details Data type: `float`
 */
#define BA_EEG_CHANNEL_ID_ACCELEROMETER 2561

/**
 * @brief check if Sample is from a stream
 *
 * @details Data type: `bool`
 */
#define BA_EEG_CHANNEL_ID_STREAMING 2625
