#!/usr/bin/python3
# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *
from boxes.edges import Bolts
import inspect

class Box(Boxes):
    """Simple open box with raised floor"""

    def __init__(self):
        Boxes.__init__(self)
        self.buildArgParser("top_edge", "bottom_edge", "x", "y", "h")
        self.argparser.add_argument(
            "--chestlid",  action="store", type=bool, default=False,
            help="add chest lid (needs hinges)")
        self.angle = 0
        self.argparser.set_defaults(
            fingerjointfinger=3.0,
            fingerjointspace=3.0
            )

    def getR(self):
        x, y, h, angle = self.x, self.y, self.h, self.angle
        t = self.thickness
        d = x - 2*math.sin(math.radians(angle)) * (3*t)

        r = d / 2.0 / math.cos(math.radians(angle))
        return r

    def side(self, move=""):
        x, y, h, angle = self.x, self.y, self.h, self.angle
        t = self.thickness
        r = self.getR()
        if self.move(x+3*t, 0.5*x+5*t, move, True):
            return

        self.ctx.save()
        self.moveTo(1.5*t, t)
        self.edge(x)
        self.corner(90+angle)
        self.edges["g"](3*t)
        self.corner(180-2*angle, r)
        self.edges["g"](3*t)
        self.corner(90+angle)
        self.ctx.restore()

        self.move(x+3*t, 0.5*x+5*t, move, False)

    def top(self):
        x, y, h = self.x, self.y, self.h
        t = self.thickness
        angle = 30

        l = math.radians(180-2*angle) * self.getR()

        self.edges["G"](3*t)
        self.edges["X"](l, y+2*t)
        self.edges["G"](3*t)
        self.corner(90)
        self.edge(y+2*t)
        self.corner(90)
        self.edges["G"](3*t)
        self.edge(l)
        self.edges["G"](3*t)
        self.corner(90)
        self.edge(y+2*t)
        self.corner(90)

    def render(self):
        x, y, h = self.x, self.y, self.h

        self.open()
        # generate g,G finger joints with default settings
        s = edges.FingerJointSettings(self.thickness)
        g = edges.FingerJointEdge(self, s)
        g.char = 'g'
        self.addPart(g)
        G = edges.FingerJointEdgeCounterPart(self, s)
        G.char = 'G'
        self.addPart(G)

        b = self.edges.get(self.bottom_edge, self.edges["F"])
        t = self.edges.get(self.top_edge, self.edges["e"])

        d2 = Bolts(2)
        d3 = Bolts(3)

        d2 = d3 = None

        self.moveTo(self.thickness, self.thickness)
        self.rectangularWall(x, h, [b, "F", t, "F"],
                             bedBolts=[d2], move="right")
        self.rectangularWall(y, h, [b, "f", t, "f"],
                             bedBolts=[d3], move="up")
        self.rectangularWall(y, h, [b, "f", t, "f"],
                             bedBolts=[d3])
        self.rectangularWall(x, h, [b, "F", t, "F"],
                             bedBolts=[d2], move="left up")
        
        self.rectangularWall(x, y, "ffff", bedBolts=[d2, d3, d2, d3], move="right")
        if self.top_edge == "c":
            self.rectangularWall(x, y, "CCCC", bedBolts=[d2, d3, d2, d3], move="up")
        else:
            self.rectangularWall(x, y, "CCCC", bedBolts=[d2, d3, d2, d3], move="up only")
            
        if self.chestlid:
            self.side()
            self.side(move="left up")
            self.top()

        self.close()

def main():
    b = Box()
    b.parseArgs()
    b.render()

if __name__ == '__main__':
    main()