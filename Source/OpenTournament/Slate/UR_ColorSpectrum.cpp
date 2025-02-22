// Copyright (c) Open Tournament Project, All Rights Reserved.

/////////////////////////////////////////////////////////////////////////////////////////////////

#include "UR_ColorSpectrum.h"

#include "Widgets/DeclarativeSyntaxSupport.h"
#include "Widgets/Colors/SColorSpectrum.h"

#include UE_INLINE_GENERATED_CPP_BY_NAME(UR_ColorSpectrum)

/////////////////////////////////////////////////////////////////////////////////////////////////

void UUR_ColorSpectrum::ReleaseSlateResources(bool bReleaseChildren)
{
    MyColorSpectrum.Get()->Invalidate(EInvalidateWidgetReason::None);
    MyColorSpectrum.Reset();
    Super::ReleaseSlateResources(bReleaseChildren);
}

TSharedRef<SWidget> UUR_ColorSpectrum::RebuildWidget()
{
    MyColorSpectrum = SNew(SColorSpectrum)
        .SelectedColor_UObject(this, &ThisClass::GetColorHSV)
        .OnValueChanged(BIND_UOBJECT_DELEGATE(FOnLinearColorValueChanged, HandleColorSpectrumValueChanged))
        .OnMouseCaptureBegin(BIND_UOBJECT_DELEGATE(FSimpleDelegate, HandleOnMouseCaptureBegin))
        .OnMouseCaptureEnd(BIND_UOBJECT_DELEGATE(FSimpleDelegate, HandleOnMouseCaptureEnd));

    return MyColorSpectrum.ToSharedRef();
}
