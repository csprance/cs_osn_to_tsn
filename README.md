# Object Space Normals To Tangent Space Normals
A modo kit by @csprance to convert an OSN to a TSN directly inside of modo using xNormal.

> [xNormal](https://xnormal.net/) must be installed on the users system in order to convert between the two different maps.


![Preview](https://csprance.com/shots/2019-02-18_d4d2ee68-5619-4c95-b39d-f8319e0b499e.gif)

## Installation
This is a modo kit so install it like normal. I've only tested this on Modo 12, but I don't think it's doing anything
fancy. Let me know if you run into any issues and if it works on other versions of modo!
* Extract/Clone into `%appdata%/Luxology/Kits`
* Restart modo

## How to use
* Select low poly meshes to use
* `Right Click` on the Object Space normal texture in the clips browser in modo and select "Convert OSN -> TSN"
* On first run you will need to set your xNormal path from the dialog that opens up
* Texture will be converted and imported into the clip browser

## Uninstallation process
* Delete `cs_osn_to_tsn` from `%appdata%/Luxology/Kits`

## Credits
* Chris Sprance - All the Things
* Thanks to the guys in the modo Developers Channel. Super friendly bunch of dudes helped me a lot.

