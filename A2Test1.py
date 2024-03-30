#!/usr/bin/env python3

import math
import Physics


table = Physics.Table()

pos = Physics.Coordinate(0.0, 0.0)

pos.x = Physics.TABLE_WIDTH / 2.0 - math.sqrt(Physics.BALL_DIAMETER * Physics.BALL_DIAMETER / 2.0)
pos.y = Physics.TABLE_WIDTH / 2.0 - math.sqrt(Physics.BALL_DIAMETER * Physics.BALL_DIAMETER / 2.0)

sb = Physics.StillBall(1, pos)

pos.x = Physics.TABLE_WIDTH / 2.0
pos.y = Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2.0
vel = Physics.Coordinate(0.0, -1000.0)
acc = Physics.Coordinate(0.0, 180.0)

rb = Physics.RollingBall(0, pos, vel, acc)

table += sb

table += rb

print(table)

while table:

    table = table.segment()
    print(table)