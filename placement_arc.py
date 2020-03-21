#!/usr/bin/env python2

# Random placement helpers because I'm tired of using spreadsheets for doing this
#
# Originally by Kevin Cuzner
# now supporting an arc of any angle up to 360°
# by Optoisolated

import math
from pcbnew import *

def place_arc_rev(refdes, start_angle, center, radius, component_offset=0, arc=360,hide_ref=True, lock=False):
    """
    Places components in a circle
    refdes: List of component references
    start_angle: Starting angle
    center: Tuple of (x, y) mils of circle center
    radius: Radius of the circle in mils
    component_offset: Offset in degrees for each component to add to angle
    hide_ref: Hides the reference if true, leaves it be if None
    lock: Locks the footprint if true
	arc: specify the arc size in degrees. Leave empty for a full circle.
    """
    pcb = GetBoard()
    deg_per_idx = arc / (len(refdes))
    for idx, rd in enumerate(refdes):
        part = pcb.FindModuleByReference(rd)
        angle = (deg_per_idx * idx + start_angle) % 360;
        print "{0}: {1}".format(rd, angle)
        xmils = center[0] + math.cos(math.radians(angle)) * radius
        ymils = center[1] + math.sin(math.radians(angle)) * radius
        part.SetPosition(wxPoint(FromMils(xmils), FromMils(ymils)))
        part.SetOrientation(((angle+180) % 360) * -10)
        if hide_ref is not None:
            part.Reference().SetVisible(not hide_ref)
    print "Placement finished. Press F11 to refresh."
