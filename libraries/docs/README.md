# SDK API Releases

This file contains the SDK release notes for SDK versions 2.X.X

---
## Version 2.5.0

Release date: 25.07.2023

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