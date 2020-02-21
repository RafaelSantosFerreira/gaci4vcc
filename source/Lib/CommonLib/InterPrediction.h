/* The copyright in this software is being made available under the BSD
 * License, included below. This software may be subject to other third party
 * and contributor rights, including patent rights, and no such rights are
 * granted under this license.
 *
 * Copyright (c) 2010-2018, ITU/ISO/IEC
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *  * Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *  * Neither the name of the ITU/ISO/IEC nor the names of its contributors may
 *    be used to endorse or promote products derived from this software without
 *    specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */

/** \file     InterPrediction.h
    \brief    inter prediction class (header)
*/

#ifndef __INTERPREDICTION__
#define __INTERPREDICTION__


// Include files
#include "InterpolationFilter.h"
#include "WeightPrediction.h"

#include "Buffer.h"
#include "Unit.h"
#include "Picture.h"

#include "RdCost.h"
#include "ContextModelling.h"
// forward declaration
class Mv;

//! \ingroup CommonLib
//! \{


// ====================================================================================================================
// Class definition
// ====================================================================================================================

class InterPrediction : public WeightPrediction
{
private:

#if JVET_L0256_BIO
  Distortion  m_bioDistThres;
  Distortion  m_bioSubBlkDistThres;
  Distortion  m_bioPredSubBlkDist[MAX_NUM_PARTS_IN_CTU];

  int m_dotProduct1[BIO_TEMP_BUFFER_SIZE];
  int m_dotProduct2[BIO_TEMP_BUFFER_SIZE];
  int m_dotProduct3[BIO_TEMP_BUFFER_SIZE];
  int m_dotProduct5[BIO_TEMP_BUFFER_SIZE];
  int m_dotProduct6[BIO_TEMP_BUFFER_SIZE];
#endif

protected:
  InterpolationFilter  m_if;

  Pel*                 m_acYuvPred            [NUM_REF_PIC_LIST_01][MAX_NUM_COMPONENT];
  Pel*                 m_filteredBlock        [LUMA_INTERPOLATION_FILTER_SUB_SAMPLE_POSITIONS][LUMA_INTERPOLATION_FILTER_SUB_SAMPLE_POSITIONS][MAX_NUM_COMPONENT];
  Pel*                 m_filteredBlockTmp     [LUMA_INTERPOLATION_FILTER_SUB_SAMPLE_POSITIONS][MAX_NUM_COMPONENT];


  ChromaFormat         m_currChromaFormat;

  ComponentID          m_maxCompIDToPred;      ///< tells the predictor to only process the components up to (inklusive) this one - useful to skip chroma components during RD-search

  RdCost*              m_pcRdCost;

  int                  m_iRefListIdx;
#if JVET_L0124_L0208_TRIANGLE
  PelStorage           m_triangleBuf;
#endif
#if JVET_L0265_AFF_MINIMUM4X4
  Mv*                  m_storedMv;
#endif
 
#if JVET_L0256_BIO
  Pel*                 m_gradX0;
  Pel*                 m_gradY0;
  Pel*                 m_gradX1;
  Pel*                 m_gradY1;
  bool                 m_subPuMC;

  int             rightShiftMSB(int numer, int    denom);
  void            applyBiOptFlow(const PredictionUnit &pu, const CPelUnitBuf &yuvSrc0, const CPelUnitBuf &yuvSrc1, const int &refIdx0, const int &refIdx1, PelUnitBuf &yuvDst, const BitDepths &clipBitDepths);
  bool            xCalcBiPredSubBlkDist(const PredictionUnit &pu, const Pel* yuvSrc0, const int src0Stride, const Pel* yuvSrc1, const int src1Stride, const BitDepths &clipBitDepths);
  void            bioSampleExtendBilinearFilter(Pel const* src, int srcStride, Pel *dst, int dstStride, int width, int height, int dim, int fracX, int fracY, bool isLast, const ChromaFormat fmt, const ClpRng& clpRng);
#endif

  void xPredInterUni            ( const PredictionUnit& pu, const RefPicList& eRefPicList, PelUnitBuf& pcYuvPred, const bool& bi 
#if JVET_L0256_BIO
                                  , const bool& bioApplied 
#endif
#if JVET_L0293_CPR
                                  , const bool luma, const bool chroma
#endif
  );
  void xPredInterBi             ( PredictionUnit& pu, PelUnitBuf &pcYuvPred );
  void xPredInterBlk            ( const ComponentID& compID, const PredictionUnit& pu, const Picture* refPic, const Mv& _mv, PelUnitBuf& dstPic, const bool& bi, const ClpRng& clpRng
#if JVET_L0256_BIO
                                 , const bool& bioApplied
#endif
#if JVET_L0293_CPR
                                 , bool isCPR
#endif
                                 );

#if JVET_L0256_BIO
  void xAddBIOAvg4              (const Pel* src0, int src0Stride, const Pel* src1, int src1Stride, Pel *dst, int dstStride, const Pel *gradX0, const Pel *gradX1, const Pel *gradY0, const Pel*gradY1, int gradStride, int width, int height, int tmpx, int tmpy, int shift, int offset, const ClpRng& clpRng);
  void xBioGradFilter           (Pel* pSrc, int srcStride, int width, int height, int gradStride, Pel* gradX, Pel* gradY);
  void xCalcBIOPar              (const Pel* srcY0Temp, const Pel* srcY1Temp, const Pel* gradX0, const Pel* gradX1, const Pel* gradY0, const Pel* gradY1, int* dotProductTemp1, int* dotProductTemp2, int* dotProductTemp3, int* dotProductTemp5, int* dotProductTemp6, const int src0Stride, const int src1Stride, const int gradStride, const int widthG, const int heightG);
  void xCalcBlkGradient         (int sx, int sy, int    *arraysGx2, int     *arraysGxGy, int     *arraysGxdI, int     *arraysGy2, int     *arraysGydI, int     &sGx2, int     &sGy2, int     &sGxGy, int     &sGxdI, int     &sGydI, int width, int height, int unitSize);
  void xWeightedAverage         ( const PredictionUnit& pu, const CPelUnitBuf& pcYuvSrc0, const CPelUnitBuf& pcYuvSrc1, PelUnitBuf& pcYuvDst, const BitDepths& clipBitDepths, const ClpRngs& clpRngs, const bool& bioApplied );
#else
  void xWeightedAverage         ( const PredictionUnit& pu, const CPelUnitBuf& pcYuvSrc0, const CPelUnitBuf& pcYuvSrc1, PelUnitBuf& pcYuvDst, const BitDepths& clipBitDepths, const ClpRngs& clpRngs );
#endif
  void xPredAffineBlk( const ComponentID& compID, const PredictionUnit& pu, const Picture* refPic, const Mv* _mv, PelUnitBuf& dstPic, const bool& bi, const ClpRng& clpRng );

#if JVET_L0124_L0208_TRIANGLE
  void xWeightedTriangleBlk     ( const PredictionUnit &pu, const uint32_t width, const uint32_t height, const ComponentID compIdx, const bool splitDir, const bool weights, PelUnitBuf& predDst, PelUnitBuf& predSrc0, PelUnitBuf& predSrc1 );
#endif

  static bool xCheckIdenticalMotion( const PredictionUnit& pu );

  void xSubPuMC(PredictionUnit& pu, PelUnitBuf& predBuf, const RefPicList &eRefPicList = REF_PIC_LIST_X);
  void destroy();


  MotionInfo      m_SubPuMiBuf[(MAX_CU_SIZE * MAX_CU_SIZE) >> (MIN_CU_LOG2 << 1)];
#if JVET_L0293_CPR
  void xChromaMC(PredictionUnit &pu, PelUnitBuf& pcYuvPred);
#endif
public:
  InterPrediction();
  virtual ~InterPrediction();

  void    init                (RdCost* pcRdCost, ChromaFormat chromaFormatIDC);

  // inter
  void    motionCompensation  (PredictionUnit &pu, PelUnitBuf& predBuf, const RefPicList &eRefPicList = REF_PIC_LIST_X
#if JVET_L0293_CPR
    , const bool luma = true, const bool chroma = true
#endif
  );
  void    motionCompensation  (PredictionUnit &pu, const RefPicList &eRefPicList = REF_PIC_LIST_X
#if JVET_L0293_CPR
    , const bool luma = true, const bool chroma = true
#endif
  );
  void    motionCompensation  (CodingUnit &cu,     const RefPicList &eRefPicList = REF_PIC_LIST_X
#if JVET_L0293_CPR
    , const bool luma = true, const bool chroma = true
#endif
  );

#if JVET_L0124_L0208_TRIANGLE
  void    motionCompensation4Triangle( CodingUnit &cu, MergeCtx &triangleMrgCtx, const bool splitDir, const uint8_t candIdx0, const uint8_t candIdx1 );
  void    weightedTriangleBlk        ( PredictionUnit &pu, bool weights, const bool splitDir, int32_t channel, PelUnitBuf& predDst, PelUnitBuf& predSrc0, PelUnitBuf& predSrc1 );
#endif

#if JVET_J0090_MEMORY_BANDWITH_MEASURE
  void    cacheAssign( CacheModel *cache );
#endif

};

//! \}

#endif // __INTERPREDICTION__
