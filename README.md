## Everysight's Maverick SDK

<img src="https://everysight.github.io/maverick_docs/assets/index-maverick2.jpg" width="300">

### Welcome, Developers!  

The Maverick SDK repository is your go-to resource for release notes, issue tracking, and tools to support your development.  

For the complete SDK documentation, API reference, and more, visit our [SDK Developer Portal](https://everysight.github.io/maverick_docs/).

As always, the SDK release notes can be found [here](./libraries/docs/README.md)

### So, how to start your Maverick application development?

1. Order your Maverick Smartglasses and get your developer key at [www.everysight.com/developer](https://www.everysight.com/developer)
2. Read our documentation within the [developers portal](https://everysight.github.io/maverick_docs/)
3. Configure the latest SDK libraries for [iOS & Android](https://everysight.github.io/maverick_docs/libraries-api/overview/)
4. Explor and try our samples for iOS and Android in the [samples repository](https://github.com/everysight-maverick/samples)


Enjoy!

For any additional issues or questions we didn't answer, please contact us at support@everysight.com

_Everysight Team_

``` kotlin 
class HelloDeveloperScreen:Screen() {
    // 'Hello Developer' will be displayed on the glasses.
    // As simple as that!
    override fun onCreate() {

        Text()
          .setText("Hello Developer")
          .setResource(Font.StockFont.Medium)
          .setTextAlign(Align.center)
          .setXY(getWidth()/2,getHeight()/2)
          .setForegroundColor(EvsColor.Green.rgba)
          addTo(this)
    }
}
```
