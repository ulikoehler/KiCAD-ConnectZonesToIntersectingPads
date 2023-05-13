#!/usr/bin/env python3
import pcbnew
from collections import Counter

class ConnectZonesToIntersectingPadsPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Connect zones to intersecting pads"
        self.category = "A descriptive category name"
        self.description = "A description of the plugin and what it does"
        self.show_toolbar_button = False # Optional, defaults to False

    def Run(self):
        selected_zones: list[pcbnew.ZONE] = [
            footprint for footprint in pcbnew.GetCurrentSelection()
            if type(footprint).__name__ == 'ZONE'
        ]
        
        for i, zone in enumerate(selected_zones):
            print(f"Selected zone #{i+1}:")
            zone_outline = zone.Outline()
            zone_possible_netcodes = Counter() # possible connected pads
            for footprint in list(pcbnew.GetBoard().GetFootprints()):
                for pad in list(footprint.Pads()):
                    # Example of what to do with [pad]
                    pad_shape = pad.GetEffectivePolygon()
                    # If pad intersects zone
                    if zone_outline.Collide(pad_shape):
                        print(f"\tFootprint {footprint.GetReference()}/Pad {pad.GetName()} (Net {pad.GetNetname()}) intersects selected zone")
                        zone_possible_netcodes[pad.GetNetCode()] += 1
            # If we found no nets, skip this zone
            if not zone_possible_netcodes:
                print(f"\tZone has no pads intersecting it - ignoring")
            # If we found more than one, warn
            elif len(zone_possible_netcodes) > 1:
                # Map zone_possible_netcodes to netnames
                zone_possible_netnames_and_counts = {
                    pcbnew.GetBoard().FindNet(netcode).GetNetname(): count
                    for netcode, count in zone_possible_netcodes.most_common()
                }
                print(f"\tZone has multiple nets intersecting it: {zone_possible_netnames_and_counts}")
                # Select most common one
                zone_netcode = zone_possible_netcodes.most_common(1)[0][0]
                zone.SetNetCode(zone_netcode)
                print(f"\tSetting zone net to {pcbnew.GetBoard().FindNet(zone_netcode).GetNetname()}")
                zone.SetNeedRefill(True)
            else: # We found exactly one net(code)
                zone_netcode = zone_possible_netcodes.most_common(1)[0][0]
                print(f"\tSetting zone net to {pcbnew.GetBoard().FindNet(zone_netcode).GetNetname()}")
                zone.SetNetCode(zone_netcode)
                zone.SetNeedRefill(True)
        pcbnew.Refresh()

ConnectZonesToIntersectingPadsPlugin().register() # Instantiate and register to Pcbnew
