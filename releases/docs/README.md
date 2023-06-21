# SDK API Releases

This file contains the SDK release notes for SDK versions 2.X.X

---
## Version 2.4.3 (RC3)

Release date: 21.03.2023

### Highlights

Glasses Firmware 118 support

Built with Kotlin Version 1.8.0

Performance updates

### Open Source List

- Kotlin: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- Swift: https://github.com/apple/swift/blob/main/LICENSE.txt (Apache)
- zlib: https://github.com/madler/zlib/
- jzlib: https://github.com/ymnk/jzlib/blob/master/LICENSE.txt (BSD-Style)
- androidx: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- android material: https://github.com/material-components/material-components-android/blob/master/LICENSE  (Apache)

### Bugs Fixes & Updates
#### SDK

This version mainly handles performance optimizations at high rendering rates

#### Firmware 118

Rendering performance optimizations

### API Compatibility

Most Bytes & Short data types were changed to Int (performance related issues at high rendering rates)

Blink animation was moved from UIElement to Animator

Several API changes as follows:

#### Main API Updates
| API        | Action  | Method Name\Notes |
| ------------ | ------- | ----------------- |
|AppErrorCode               |Add|added `FailedPairing` error code
|Various Enums              |Modified | Changed data type from Byte to Int
|Polyline                   |Modified|ctor parameters change _xs,_ys -> _xys
|Path                       |Modified|ctor parameters change _xs,_ys -> _xys
|Path                       |Modified|setPath parameters change _xs,_ys -> _xys
|UIElement                  |Add| added setXY, setWidthHeight, setDimensions methods
|UIElement                  |Removed|Blink functionality was moved to Animator
|UIElement                  |Removed|onTouch (use IEvsGlassesEvents instead)
|UIElement                  |Removed|getBoundingBoxTransformed (use getBoundingBox instead)
|UIElementGroup             |Removed| cancelAnimationsTree
|IEvsAutoBrightnessEvents   |Add|added onAutoBriGainChanged callback method
|IEvsAutoBrightnessController|Add| added methods getGain, addGain
|IEvsGlassesStateService    |Add| added method getSerialInfo
|IEvsScreenService          |Add| added method removeTopmostScreen
|Animator                   |Add|added blink,isBlinking methods 
|IEvsSensorsService         |Modified|added usePredication parameter to enableSensorsFusion
|CanvasBuffer               |Modified|drawPath xyPoints as a single array
|CanvasBuffer               |Modified|drawPolygon xyPoints as a single array, added stride
|BoundingBox                |Modified | IsEmpty->isEmpty
|BoundingBox                |Add | isSameAs, isValid,isInside, union,intersect
|FastQue                    |Add|classes added

