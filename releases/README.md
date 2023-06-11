# SDK API Releases

This file contains the Epsilon SDK release notes for SDK versions 2.X.X

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

---
## Version 2.4.2 (RC2)

Release date: 28.12.2022

### Highlights

Glasses Firmware 117 support

Built with Kotlin Version 1.7.20

Added low battery indication using led & boot screen

Added clip capability 

### Open Source List

- Kotlin: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- Swift: https://github.com/apple/swift/blob/main/LICENSE.txt (Apache)
- zlib: https://github.com/madler/zlib/
- jzlib: https://github.com/ymnk/jzlib/blob/master/LICENSE.txt (BSD-Style)
- androidx: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- android material: https://github.com/material-components/material-components-android/blob/master/LICENSE  (Apache)

### Bugs Fixes & Updates
#### SDK

Added UIElement clipping support (from firmware 117 and above)

Added Arrow UI Element

Added ability for more accurate font width calculation (fonts should be re-generated via the font2sif script, font json file should be added to the application assets)

Add the ability to control the brightness in predefined optimized steps using the IEvsDiscreteBrightnessController interface

Ambient & Proximity callbacks were removed from Screen. Listening to ambient and proximity events is now only via IEvsSensorsService/IEvsSensorsEvents

Added AutoBrightnessGainProvider auto brightness sample provider implementation

Bug Fix: Pen size wont update in rare cases

Performance optimizations
#### Firmware 117

Hold power button 0.6 seconds to turn on glasses (Instead of short click)

Charging & Low battery LED indication

Boot screen low battery indication

Sprite Image source size update: 640x400 pixels

BLE name update

Clipping support

Bug Fix: Transformed Polygon partial fill issue

Rendering optimizations and stability improvements
### API Compatibility

#### Main API Updates
| API        | Action  | Method Name\Notes |
| ------------ | ------- | ----------------- |
| UIElement|Modified|added timestampMs parameter to onBeforeDraw
| UIElement|Rename|draw renamed to onDraw
| UIElement|Add|showBorder
| UIElement|Add|setBorderStyle
| UIElement|Add|hasParent
| UIElement|Add|onLayout
| UIElement|Add|clip
| UIElement|Add|drawBorder (protected)
| UIElement|Add|getBoundingBoxTransformed
| UIElement|Add|removeSelf
| UIElement|Add|blink
| UIElement|Add|isBlinking
| UIElement|Add|onBlinkEnded (protected)
| UIElementGroup|Add| getElementsCount
| UIElementGroup|Add| addAll
| UIResource | Add| getMaxSizeBytes
| Path | Modified | setPath parameter was changed from Array\<Float\> to FloatArray
| Polygon | Modified | addMany parameter was changed from Array\<Float\> to FloatArray
| Polyline| Modified | input parameters were changed from Array\<Float\> to FloatArray
| Arrow | Add | Arrow ui element was added
| Svg   | Removed | Removed Svg (Beta) Support
| Screen | Removed | onAmbient (use IEvsSensorsEvents instead)
| Screen | Removed | onProximity  (use IEvsSensorsEvents instead)
| Screen | Add | clip
| Screen | Add | addAll
| Screen | Removed | onPowerButton  (use IEvsGlassesEvents instead)
| Screen | Removed | onDisplayState  (use IEvsGlassesEvents instead)
| IEvsGlassesEvents | Modified | onPowerButton parameter renamed to PowerButtonAction
| IEvsGlassesEvents | Add | onTouch (moved from IEvsSensorsEvents)
| IEvsSensorsEvents | Removed | onTouch (moved to IEvsGlassesEvents)
| IEvsDisplayService | Add | added desecrateBrightness method
| IEvsDiscreteBrightnessController| Add | added interface IEvsDiscreteBrightnessController
| AutoBrightnessGainProvider| Add | class added 
| ButtonActionType | Rename | PowerButtonAction
| PowerButtonAction | Add | add PowerButtonAction.before_shutdown event
| BatteryLevel.Critical | Add | added Critical battery level 
| TouchDirection.doubleTap | Removed | removed doubleTap enum (not supported by HW)
| Direction | Add | added Direction enum
| EVS_ADDON_NOTIFICATION | Add | added phone notification constant addon for supported SDKs

#### Inertial Sensors API Updates (For supported systems only)

| API        | Action  | Method Name\Notes |
| ------------ | ------- | ----------------- |
| IEvsSensorsService| Add | added enableSensorsFusion method
| IEvsSensorsService| Add |added disableInertialSensors method
| IEvsSensorsService| Add | added enableSensorsFusion method
| IEvsSensorsService| Add | added registerQuaternionSensorsEvents method
| IEvsSensorsService| Add | added unregisterQuaternionSensorsEvents method
| IEvsSensorsService| Add | added registerYprSensorsEvents method
| IEvsSensorsService| Add | added unregisterYprSensorsEvents method
| IEvsSensorsService| Removed | Removed registerRawInertialSensorsEvents method
| IEvsSensorsService| Removed | Removed unregisterRawInertialSensorsEvents method
| IEvsSensorsService| Removed | Removed getFusedLos method
| YprData| Add | class added 
| QuaternionData| Add | class added 
| CalibrationStatus| Add | enum added 
| IEvsQuaternionSensorsEvents|Add| interface added
| IEvsYprSensorsEvents|Add| interface added
| SensorRate | Modified | removed SensorRate.rate_off
| SensorRate | Modified | added toHz()
| ScreenRenderRate | Add | added los enum value


---
## Version 2.4.0 (RC1)

Release date: 20.09.2022

### New Features

Glasses Firmware 113 support

Built with Kotlin Version 1.6.0

Add controller accessory API

Add Arc2 UI Element

### Open Source List

- Kotlin: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- Swift: https://github.com/apple/swift/blob/main/LICENSE.txt (Apache)
- zlib: https://github.com/madler/zlib/
- jzlib: https://github.com/ymnk/jzlib/blob/master/LICENSE.txt (BSD-Style)
- androidx: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- android material: https://github.com/material-components/material-components-android/blob/master/LICENSE  (Apache)

### Bugs Fixes & Updates
#### SDK

UIElement animator timing fix

Add Arc2 UI Element

Resource upload callback fix when resource are already on glasses

Enable to set the Screen size via constructor

Screen rendering position reference point was changed from top\left to centerX\centerY

Add add-on API to receive interface for handling SDK add-ons (like controller or developer APIs)

Better rotated ellipse rendering

Performance optimizations
#### Firmware 113

Latin fonts rendering bug fix

Hold power button 1.5 seconds to turn on glasses (Instead of short click)

Ignore touch if glasses are off-face (when proximity is enabled)

Updated led indications

Sensors initialization sequence fix

CRC Check on resources upload

Updated battery scale

Rendering optimizations and stability improvements
### API Compatibility

| API        | Action  | Method Name\Notes |
| ------------ | ------- | ----------------- |
| UIElement    | Add   | setForegroundColor(EvsColor)
| UIElement    | Add   | setBackgroundColor(EvsColor)
| FillableElement    | Add   | setFillColor(EvsColor)
|Arc2           | Add | Class added
|Arc            |Add | setDirection
|Arc            |Add | getAngleFromDeg
|Arc            |Add | getAngleToDeg
|Arc            |Add | isBetween
|Arc            |Add | isBetweenOrEqual
|Arc            |Add | getDirection
|IEvsGlassesStateService|Add|batteryLevel
|IEvsGlassesStateService|Add|estimatedRemainingTime
|IEvsGlassesEvents|Modified|onPowerButton(Boolean)->onPowerButton(ButtonActionType)
|Screen |Add|constructor(screenWidth:Float,screenHeight: Float)
|Screen | Add | constructor(name:String,screenWidth:Float,screenHeight: Float)
|Screen|Add|isResumed
|IEvsApp|Add|getAddOn
|IEvsApp|Removed|developer (can be received via IEvsApp.getAddOn)
|Font|Added|getMeasuredContentWidth
|Font|Added|getMeasuredContentHeight
|IEvsScreenService | Modified | setScreenOffSetY->setRenderingCenterY
|IEvsScreenService | Modified | getScreenOffSetY->getRenderingCenterY
|IEvsScreenService | Modified | setScreenOffSetX->setRenderingCenterX
|IEvsScreenService | Modified | getScreenOffSetX->getRenderingCenterX
|IEvsScreenService | Removed | renderingWidth (get the info from Screen.getWidth())
|IEvsScreenService | Removed | renderingHeight (get the info from Screen.getHeight())
|IEvsScreenService | Removed | getMaxOffsetMarginX
|IEvsScreenService | Removed | getMaxOffsetMarginY
|IEvsScreenService | Add | getEnforceRenderingBorders
|IEvsScreenService | Add | setEnforceRenderingBorders
|IEvsSensorsEvents | Add | onSensorEnableRequested
|BatteryLevel|Add|enum added
|RotationDirection|Add|enum added
|ButtonActionType|Add|add long_pressed enum value
|IEvsController|Add| Interface added
|IEvsScanCallback|Add| Interface added
|IEvsSystemLogger|Add|setDebugMode
|IEvsSystemLogger|Add|isDebug
|IEvsAddOn|Add|Interface added
|IEvsDeveloperService|Modified|Moved to package UIKit.addons, implements IEvsAddOn
|EVS_ADDON_CONTROLLER|Add|Constant added
|EVS_ADDON_DEVELOPER|Add|Constant added
|EVS_ADDON_TECH|Add|Constant added

---
## Version 2.3.0 (Beta)

Release date: 19.05.2022

### New Features

Glasses Firmware 107 support

Built with Kotlin Version 1.6.0

Sprite Images Support (Slot 0 Only)

Compressed sif fonts support (sifz)

Auto brightness controller

### Open Source List

- Kotlin: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- Swift: https://github.com/apple/swift/blob/main/LICENSE.txt (Apache)
- zlib: https://github.com/madler/zlib/
- jzlib: https://github.com/ymnk/jzlib/blob/master/LICENSE.txt (BSD-Style)
- androidx: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- android material: https://github.com/material-components/material-components-android/blob/master/LICENSE  (Apache)

### Bugs Fixes & Updates
#### SDK

Performance optimizations

Bluetooth zlib streams reset issue in rare cases

IOS zlib library replacement

`ScreenRenderRate.Normal` Rendering rate was changed to about 5Hz
#### Firmware 107

Glasses battery led indication fix

Rendering optimizations
### API Compatibility

| Class        | Action  | Method Name\Notes |
| ------------ | ------- | ----------------- |
| ScreenRenderRate    | Modified     | normal rate changed to about 5Hz          |
| SpriteImgSrc| Added | Added support for Sprite image source |
| FontType | Modified | Add sif_4bpp_zipped and sif_2bpp_zipped values |
| IEvsAutoBrightnessController | Added| interface added|
| IEvsAutoBrightnessEvents | Added| interface added|
| IEvsAutoBrightnessProvider | Added| interface added|
| IEvsDisplayService|Modified| added autoBrightness() method
| IEvsOtaService|Modified| add getAvailableOta method
| IEvsRawInertialSensorsEvents | Added| interface added|
| IEvsSensorsService | Modified| Added registerRawInertialSensorsEvents|
| IEvsSensorsService | Modified| Added unregisterRawInertialSensorsEvents|
| IEvsSensorsEvents | Modified | Removed onSensor, onTemperature
| UIElement | Modified | Add getPenShape, getLineStyle, getPenThickness, tag
| Polyline| Add | Class Added
| Path | Modified | Add getSequentialPathMaxPoints

---
## Version 2.2.0 (Beta)

Release date: 13.01.2022

### New Features

Glasses Firmware 101 support
Built with Kotlin Version 1.6.0

### Bugs Fixes

Performance optimizations

### API Compatibility

| Class        | Action  | Method Name\Notes |
| ------------ | ------- | ----------------- |
| IEvsGlassesEvents    | added     | onBrightnessChangeRequested()          |
| Screen    | modified     | onUpdateUI() -> onUpdateUI(timestampMs)|
| IEvsColors    | added     | interface added for support color utilities functions          |
| EvsColors    | added     | class added for support color utilities functions          |
| EvsColor    | removed     | fromHexString(), fromRgb(), fromRgba(), fromSvgColor() (moved to EvsColors)          |
| UIElement    | modified     | setPenThickness(byte)->setPenThickness(int)          |

---

## Version 2.0.3 (Beta)

Release date: 09.09.2021

### New Features

UI Element Alpha support was removed from the API

### Bugs Fixes

Performance optimizations

Ellipse drawing optimization

### API Compatibility

| Class        | Action  | Method Name\Notes |
| ------------ | ------- | ----------------- |
| UIElement    | removed | setAlpha          |
| UIElement    | removed | getAlpha          |
| Animator     | removed | getCurrentAlpha   |
| Animator     | removed | alpha             |
| Animator     | removed | alpha             |
| CanvasBuffer | added   | setLineStyle      |
| CanvasBuffer | added   | setPenShape       |

---

## Version 2.0.2 (Beta)

Release date: 25.07.2021

### New Features

None

### Bugs Fixes

Connect-disconnect loop when switching connected glasses

Resources uploading optimizations

### API Compatibility

Fully Back Compatible

| Class   | Action | Method Name\Notes |
| ------- | ------ | ----------------- |
| IEvsApp | added  | isReady           |

---

## Version 2.0.1 (Beta)

Release date: 20.06.2021

### New Features

None

### Bugs Fixes

onBeginAuth does not call in rare cases

IOS images better handling

### API Compatibility

Fully Compatible

---

## Version 2.0.0 (Beta)

Release date: 17.06.2021

### New Features

Supports both A-Protos and B-Protos Hardware

Additional Images Slots: up-to 32 (B Protos only)

Screen is paused when the glasses display turns off

Added support for proximity and ambient sensors for supported hardware

Better resources slots handling

Stability & Performance Improvements

#### Pairing Support:

This SDK version supports pairing

When pairing is required:

- Use: `IEvsCommunicationChannel::connectSecured`
- Don't use: `IEvsCommunicationChannel::connect`

### Bugs Fixes

Bluetooth disconnection handling when wrong api key is provided

Popup layout is wrong is some cases

### API Compatibility

| Class                | Action  | Method Name\Notes           |
| -------------------- | ------- | --------------------------- |
| IEvsApp              | added   | setApiKeyName               |
| IEvsAppEvents        | added   | onBeginAuth                 |
| UIElement            | added   | setPenShape (B Proto Only)  |
|                      | added   | setLineStyle (B Proto Only) |
| IEvsDeveloperService | removed | isOptimizeRendering         |
|                      | removed | setOptimizeRendering        |
