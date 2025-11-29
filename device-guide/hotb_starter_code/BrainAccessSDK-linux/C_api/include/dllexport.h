/**
 * @file dllexport.h
 * @author Neurotechnology (brainaccess@neurotechnology.com)
 * @brief Macros used to export/import library functions
 *
 * @copyright Copyright (c) 2022 Neurotechnology
 */

#pragma once

/**
 * @brief Macro to define export/import for Windows and GCC
 *
 * @details This macro is used to define the export/import symbols for Windows
 * and GCC. When compiling the library, define BA_CORE_DLL_IS_EXPORTING to
 * export the symbols. When using the library, do not define
 * BA_CORE_DLL_IS_EXPORTING.
 *
 * @note This macro is used to ensure that the library functions are properly
 * exported/imported on Windows and GCC.
 */
// Check if we're building a static library
#ifdef LIBRARY_TYPE_STATIC
#define BA_CORE_DLL_EXPORT // Empty for static builds
#define NOT_BA_CORE_DLL_EXPORT
#pragma message("Compiling with STATIC LIBRARY - BA_CORE_DLL_EXPORT is empty")
#else
#if defined _WIN32 || defined __CYGWIN__
#ifdef BA_CORE_DLL_IS_EXPORTING
// Exporting...
#ifdef __GNUC__
#define BA_CORE_DLL_EXPORT __attribute__((dllexport))
#else
// Note: actually gcc seems to also support this syntax.
#define BA_CORE_DLL_EXPORT __declspec(dllexport)
#endif
#else
#ifdef __GNUC__
#define BA_CORE_DLL_EXPORT __attribute__((dllimport))
#else
// Note: actually gcc seems to also support this syntax.
#define BA_CORE_DLL_EXPORT __declspec(dllimport)
#endif
#endif
#define NOT_BA_CORE_DLL_EXPORT
#else
#if __GNUC__ >= 4
#define BA_CORE_DLL_EXPORT     __attribute__((visibility("default")))
#define NOT_BA_CORE_DLL_EXPORT __attribute__((visibility("hidden")))
#else
#define BA_CORE_DLL_EXPORT
#define NOT_BA_CORE_DLL_EXPORT
#endif
#endif
#endif

/**
 * @brief Macro to define 'NOEXCEPT' for C++ and 'NOTHROW' for C
 *
 * @details This macro is used to define the 'NOEXCEPT' keyword for C++ and
 * 'NOTHROW' for C. It ensures that the library functions are properly marked
 * as noexcept or nothrow, depending on the language being used.
 */
#ifdef __cplusplus
#define NOEXCEPT noexcept
#else
#define NOEXCEPT
#endif
