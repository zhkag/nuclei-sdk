/*
 * Copyright (c) 2019 Nuclei Limited. All rights reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the License); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an AS IS BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef __CORE_FEATURE_VECTOR__
#define __CORE_FEATURE_VECTOR__

/*!
 * @file     core_feature_vector.h
 * @brief    Vector feature API header file for Nuclei N/NX Core
 */
/*
 * Vector Feature Configuration Macro:
 * 1. __VECTOR_PRESENT:  Define whether Vector Unit is present or not
 *   * 0: Not present
 *   * 1: Present
 */
#ifdef __cplusplus
 extern "C" {
#endif

#include "core_feature_base.h"

#if defined(__VECTOR_PRESENT) && (__VECTOR_PRESENT == 1)

/* ###########################  CPU Vector Intrinsic Functions ########################### */
/**
 * \defgroup NMSIS_Core_Vector_Intrinsic   Intrinsic Functions for Vector Instructions
 * \ingroup  NMSIS_Core
 * \brief    Functions that generate RISC-V Vector instructions.
 * \details
 *
 * RISC-V Vector Intrinsic APIs are provided directly through compiler generated intrinsic function.
 *
 * This intrinsic function support in compiler is introduced in nuclei riscv gcc 10.2.
 *
 * API header file can be found in lib/gcc/riscv-nuclei-elf/<gcc_ver>/include/riscv_vector.h
 *
 * API Reference Manual can be found here:
 *
 * - https://github.com/riscv-non-isa/rvv-intrinsic-doc/blob/master/rvv-intrinsic-api.md
 *
 *   @{
 */
/** @} */ /* End of Doxygen Group NMSIS_Core_Vector_Intrinsic */

#if defined(__INC_INTRINSIC_API) && (__INC_INTRINSIC_API == 1)
#include <riscv_vector.h>
#endif

#endif /* defined(__VECTOR_PRESENT) && (__VECTOR_PRESENT == 1) */

#ifdef __cplusplus
}
#endif

#endif /* __CORE_FEATURE_VECTOR__ */
