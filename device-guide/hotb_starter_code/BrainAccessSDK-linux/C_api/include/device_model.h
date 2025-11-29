/**
 * @file device_model.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief BrainAccess device model numbers
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

#include <stdint.h>

/**
 * @brief BrainAccess MINI V2
 */
#define BA_DEVICE_MODEL_MINI_V2 0

/**
 * @brief BrainAccess MIDI (16 Channels)
 */
#define BA_DEVICE_MODEL_MIDI 1

/**
 * @brief BrainAccess MAXI (32 Channels)
 */
#define BA_DEVICE_MODEL_MAXI 2

/**
 * @brief BrainAccess EMG
 */
#define BA_DEVICE_MODEL_EMG 3

/**
 * @brief BrainAccess Halo
 */
#define BA_DEVICE_MODEL_HALO 4

/**
 * @brief BrainAccess Halo V2
 */
#define BA_DEVICE_MODEL_HALO_V2 5

/**
 * @brief Unknown device
 */
#define BA_DEVICE_MODEL_UNKNOWN 0xFF

/**
 * @brief Device model type
 */
typedef uint8_t ba_device_model;
