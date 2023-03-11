# -*- coding: utf-8 -*-
#
# Copyright 2023 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

class Vector3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self):
        return '<Vector3D instance>\n' + \
              f'    x = {self.x}\n' + \
              f'    y = {self.y}\n' + \
              f'    z = {self.z}'
    
    def __repr__(self):
        return f'Vector3D(x={self.x}, y={self.y}, z={self.z})'
    
    def dot(self, v):
        if not isinstance(v, Vector3D):
            raise ValueError(f'vector v: {v} is not a Vector3D instance')
        return self.x * v.x + self.y * v.y + self.z * v.z
