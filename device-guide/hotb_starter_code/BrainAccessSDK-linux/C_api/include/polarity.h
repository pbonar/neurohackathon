/**
 * @file polarity.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief polarity modes constants
 *
 * @copyright Copyright (c) 2024 Neurotechnology
 */

#pragma once

#include <stdint.h>

typedef uint8_t ba_polarity;

#define BA_POLARITY_NONE     0 ///< Polarity mode none
#define BA_POLARITY_BOTH     1 ///< Polarity mode both (positive and negative)
#define BA_POLARITY_POSITIVE 2 ///< Polarity mode positive
#define BA_POLARITY_NEGATIVE 3 ///< Polarity mode negative
