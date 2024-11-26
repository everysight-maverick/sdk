# SDK API Releases

This file contains the SDK release notes for SDK versions 2.X.X

---
## Version 2.6.0

Release date: 25 NOV 2024

### Highlights

**Libraries are now available via Maven (Android) and SPM (iOS).** In version 2.5.0 the libraries were manually downloaded from our GitHub repository.

Glasses Firmware v121

Sensors API fixes to enable better sensors support

Includes beta features and samples for Line of sight (LOS) Subsystem & API and Auto-layout UIElements

Built with Kotlin Version 2.0.0

### Open Source List

#### Common

- Kotlin: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- zlib: https://github.com/madler/zlib/

#### IOS 
- Swift: https://github.com/apple/swift/blob/main/LICENSE.txt (Apache)
- JSONWebToken: https://github.com/kreactive/JSONWebToken/tree/master (MIT)

#### Android
- androidx: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- android material: https://github.com/material-components/material-components-android/blob/master/LICENSE  (Apache)
- jjwt: https://github.com/jwtk/jjwt (Apache)

### Bugs Fixes & Updates
#### SDK

The version, in addition to bug fixes, include the following main updates:

1. Sensors API fixes to enable better sensors support
2. (Beta) Line of sight (LOS) Subsystem & API
3. Auto-layouts based UIElements

#### Firmware 121

- Updated BLE stack (BLE 5.4 certified)
- Rendering bug fixes
- Inertial sensors calibration params saving

#### Main fixed bugs

| Fixed Bugs          
| ------------ 
| Enabling just the Gyro Sensor - no callback is triggered
| Rotating Ellipse more then 180 deg make it disappear
| Sensors calibration information not saving properly
| sdk key validation error code is sometimes wrong
| Several performance issues
| Crash while connecting in iOS 15

### API Compatibility

The following API changes have been made

#### Main API Updates
| API          | Change |
| ------------ | ----------------- |
|IEvsAppEvents| Add callback method onUnReady
|Viewport| New Base class for both Screen and ArScreen classes
|Drawable|New base class for all elements that can be drawn on the glasses HUD like UIElement and ArModel
|Screen | Screen new inherit from the Viewport class
|ScreenRenderRate       | namespace changed to UIKit.app.data
| Font          |Added methods for handling supported chars within the font: trimUncovered, countCharsCoverage
|IEvsGlassesStateService| glasses type property was removed
|IEvsScreenService| The interface exposes the Viewport class instead of the Screen class
|UIElement| Added removeAfter method
|UIElement| Added getYBottom method
|UIElement| Added getXEnd method
|UIElement| Rename addToScreen & addToGroup to addTo
|IEvsSensorsService| enableSensorsFusion method removed. Use enableInertialSensors, enableGyro, enableMagnetometer or enableAccelerometer instead
|IEvsSensorsService|setSensorsRate added to enable overriding the default sensors rate
|IEvsSensorsService|getSensorsRate added to receive the sensors rate
|IEvsSensorsService|setUsePrediction to enable prediction when getting LOS data via registerYprSensorsEvents or registerQuaternionSensorsEvents
|TextBlock| New UIElement. Represents a multiline text control
|AutoLayout| AutoLayout is a layout manager that handles automatic layout for UI elements.
|Column|Column is a layout manager that arranges its children in a vertical sequence.
|Row | Row is a layout manager that arranges its children in a horizontal sequence.
|Modifier| Modifier is used to modify the properties of a UIElement, including padding, gravity, and visibility. This should only be used for a UIElement that resides inside an AutoLayout

#### Line of Sight (LOS) API (beta)
| API          | Notes |
| ------------ | ----------------- |
|ArScreen | Represents a screen for augmented reality (AR) content to be displayed on the glasses.
|IArElement|Interface of an element that can be drawn in ArScreen
|ArWindow|Represents a board in an Augmented Reality (AR) environment, capable of displaying 2D UI elements and place them at 3D position.
|ArModel|Represents a collection of 3D primitives to be rendered in an augmented reality (AR) environment.
|ArPrimitive|Represents a 3D primitive composed of world coordinates
|ArLines|A class representing lines in a 3D space.
|ArPoints|A class representing a collection of points in a 3D space.
|ArTriangles|Class representing a set of triangles in 3D space.
|ArFactory|Helper class. Responsible for creating 3D models and objects for use in augmented reality (AR) environments. It provides functions to create cubes, stars, and arrows with customizable properties.
|BoundingSphere|Represents a BoundingSphere in 3D space defined by a center position and radius.
|M| A utility class providing various mathematical operations for 3x3 and 4x4 matrices, vectors, and rotations.
|Quaternion|Represents a quaternion, a mathematical concept used to represent rotations in 3D space.


---
## Version 2.5.0

Release date: 25 JUL 2023

### Highlights

Glasses Firmware 119 support

Built with Kotlin Version 1.8.10


### Open Source List

#### Common

- Kotlin: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- zlib: https://github.com/madler/zlib/

#### IOS 
- Swift: https://github.com/apple/swift/blob/main/LICENSE.txt (Apache)
- https://github.com/Kitura/Swift-JWT (Apache)

#### Android
- androidx: https://www.apache.org/licenses/LICENSE-2.0.txt (Apache)
- android material: https://github.com/material-components/material-components-android/blob/master/LICENSE  (Apache)
- https://github.com/jwtk/jjwt (Apache)

### Bugs Fixes & Updates
#### SDK

This version mainly handles performance optimizations

#### Firmware 119

Rendering performance optimizations

### API Compatibility

Several API changes as follows*:

#### Main API Updates
| API          | Action  | Method Name\Notes |
| ------------ | ------- | ----------------- |
|IEvsAuthService       |New | added the `IEvsAuthService` interface
|IEvsInertialSensorsEvents       |New | added the `IEvsInertialSensorsEvents` interface
|ControllerAction               |New|enum added
|IEvsApp       |Modified | added `auth` to expose the `IEvsAuthService` 
|IEvsApp       |Modified | removed `setApiKey`(moved to `IEvsAuthService`)
|IEvsApp       |Modified | removed `setApiKeyName`(moved to `IEvsAuthService`)
|UIElement       |Modified | added `addToScreen`
|UIElement       |Modified | added `addToGroup`
|IEvsSensorsService       |Modified | added `enableMagneticDeclinationCorrection`
|IEvsSensorsService       |Modified | added `unregisterInertialSensorsEvents`
|IEvsOtaService       |Modified | added `pauseOtaAvailableNotification`
|IEvsOtaService       |Modified | added `isOtaAvailableNotificationPaused`
|UIResource       |Modified | added `retryUpload` method
|ScreenRenderRate       |Modified | rendering rates were updated
|Screen       |Modified | `onResourcesUploadStart` removed
|Screen       |Modified | `resourcesToUploadCount` removed
|Screen       |Modified | `hasResourcesToUpload` removed
|AppErrorCode       |Modified | `ActivationError` added
|BTConstants               |Renamed|epsilonServiceUUID->serviceUUID

<sup>*The API changes in version 2.5.0 have been compared with version 2.4.3 limited release</sup>