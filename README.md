# KiCAD-ConnectZonesToIntersectingPads
KiCAD plugin to connect zones to intersecting pads

For all selected zones, this plugin will find all pads that are intersecting the zone, perform a majority vote on the selected nets and connect the zone to whatever net is shared by the largest number of intersecting pads.

This plugin is *not* intended to be used for your bog-standard GND fill zone, but for thermal relief zones for LEDs or high-current "zones used as thick traces" which are prevalent in higher power SMPS, for example. For those boards, it is often extremely tedious to assign each zone to the correct pads - making it quite time-consuming if you have hundreds of zones. This plugin competely automates this process, assigning one or multiple zones with a single click.

### State of the plugin

At the moment, this plugin is provided as-is on Github only for local installation. The reason for this is purely that I currently don't have time to make this into a "proper" published KiCAD plugin (it might happen in the future, depending on how often I use this plugin).

Pull requests are always welcome & encouraged.
