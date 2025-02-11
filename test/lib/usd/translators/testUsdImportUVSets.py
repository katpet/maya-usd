#!/usr/bin/env mayapy
#
# Copyright 2016 Pixar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from pxr import Gf
from pxr import Tf

import mayaUsd.lib as mayaUsdLib

from maya import cmds
from maya import standalone
from maya.api import OpenMaya as OM

import os
import unittest

import fixturesUtils

class testUsdImportUVSets(unittest.TestCase):

    def _AssertUVSet(self, mesh, uvSetName, expectedValues,
            expectedNumValues=None, expectedNumUVShells=None):
        """
        Verifies that the UV values for the uv set named uvSetName on the
        MFnMesh mesh match the values in expectedValues. expectedValues should
        be a dictionary mapping mesh-level face vertex indices to UV values.
        A face vertex index missing from the dictionary means that that face
        vertex should NOT have an assigned UV value on the Maya mesh.
        If multiple face vertices map to the same UV value and the number of UV
        values in the UV set is smaller than the number of assignments, pass in
        the expected number of UV values in the UV set as expectedNumValues.
        """
        if expectedNumValues is None:
            expectedNumValues = len(expectedValues)
        actualNumValues = mesh.numUVs(uvSetName)
        self.assertEqual(expectedNumValues, actualNumValues)

        itMeshFV = OM.MItMeshFaceVertex(mesh.object())
        itMeshFV.reset()
        fvi = 0
        while not itMeshFV.isDone():
            expectedUV = expectedValues.get(fvi)
            if expectedUV is None:
                self.assertFalse(itMeshFV.hasUVs(uvSetName))
            else:
                self.assertTrue(itMeshFV.hasUVs(uvSetName))

                actualUV = itMeshFV.getUV(uvSetName)
                self.assertAlmostEqual(expectedUV, actualUV)

            itMeshFV.next() # pylint: disable=next-method-called
            fvi += 1

        if expectedNumUVShells is not None:
            (numUVShells, shellIndices) = mesh.getUvShellsIds(uvSetName)
            self.assertEqual(expectedNumUVShells, numUVShells)

    @classmethod
    def setUpClass(cls):
        cls.asFloat2 = mayaUsdLib.ReadUtil.ReadFloat2AsUV()

        cls.inputPath = fixturesUtils.readOnlySetUpClass(__file__)

        if cls.asFloat2: 
            usdFile = os.path.join(cls.inputPath, "UsdImportUVSetsFloatTest", "UsdImportUVSetsTest_Float.usda")
        else:
            usdFile = os.path.join(cls.inputPath, "UsdImportUVSetsTest", "UsdImportUVSetsTest.usda")

        cmds.usdImport(file=usdFile, shadingMode=[["none", "default"], ], remapUVSetsTo=[['','']])

    @classmethod
    def tearDownClass(cls):
        standalone.uninitialize()

    @staticmethod
    def _GetMayaMesh(meshNodePath):
        selectionList = OM.MSelectionList()
        selectionList.add(meshNodePath)
        mObj = selectionList.getDependNode(0)
        return OM.MFnMesh(mObj)

    def testImportNoUVSets(self):
        """
        Tests that importing a USD cube mesh with no UV set primvars results in
        the default 'map1' UV set on the Maya mesh being empty.
        """
        mayaCubeMesh = testUsdImportUVSets._GetMayaMesh('NoUVSetsCubeShape')
        expectedValues = {}
        self._AssertUVSet(mayaCubeMesh, 'map1', expectedValues)

    def testImportDefaultUVSet(self):
        """
        Tests that a USD cube mesh with the Maya default values for the default
        UV set (named 'st' in USD) gets imported correctly.
        """
        mayaCubeMesh = testUsdImportUVSets._GetMayaMesh('DefaultUVSetCubeShape')

        # These are the default UV values for a regular Maya polycube.
        expectedValues = {
            0: Gf.Vec2f(0.375, 0.0),
            1: Gf.Vec2f(0.625, 0.0),
            2: Gf.Vec2f(0.625, 0.25),
            3: Gf.Vec2f(0.375, 0.25),
            4: Gf.Vec2f(0.375, 0.25),
            5: Gf.Vec2f(0.625, 0.25),
            6: Gf.Vec2f(0.625, 0.5),
            7: Gf.Vec2f(0.375, 0.5),
            8: Gf.Vec2f(0.375, 0.5),
            9: Gf.Vec2f(0.625, 0.5),
            10: Gf.Vec2f(0.625, 0.75),
            11: Gf.Vec2f(0.375, 0.75),
            12: Gf.Vec2f(0.375, 0.75),
            13: Gf.Vec2f(0.625, 0.75),
            14: Gf.Vec2f(0.625, 1.0),
            15: Gf.Vec2f(0.375, 1.0),
            16: Gf.Vec2f(0.625, 0.0),
            17: Gf.Vec2f(0.875, 0.0),
            18: Gf.Vec2f(0.875, 0.25),
            19: Gf.Vec2f(0.625, 0.25),
            20: Gf.Vec2f(0.125, 0.0),
            21: Gf.Vec2f(0.375, 0.0),
            22: Gf.Vec2f(0.375, 0.25),
            23: Gf.Vec2f(0.125, 0.25)
        }

        self._AssertUVSet(mayaCubeMesh, "st", expectedValues,
            expectedNumValues=14, expectedNumUVShells=1)

    def testImportMap1UVSet(self):
        """
        Tests that a USD cube mesh with the Maya default values for the default
        UV set (map1) gets imported correctly.
        """
        mayaCubeMesh = testUsdImportUVSets._GetMayaMesh('Map1UVSetCubeShape')

        # These are the default UV values for a regular Maya polycube.
        expectedValues = {
            0: Gf.Vec2f(0.375, 0.0),
            1: Gf.Vec2f(0.625, 0.0),
            2: Gf.Vec2f(0.625, 0.25),
            3: Gf.Vec2f(0.375, 0.25),
            4: Gf.Vec2f(0.375, 0.25),
            5: Gf.Vec2f(0.625, 0.25),
            6: Gf.Vec2f(0.625, 0.5),
            7: Gf.Vec2f(0.375, 0.5),
            8: Gf.Vec2f(0.375, 0.5),
            9: Gf.Vec2f(0.625, 0.5),
            10: Gf.Vec2f(0.625, 0.75),
            11: Gf.Vec2f(0.375, 0.75),
            12: Gf.Vec2f(0.375, 0.75),
            13: Gf.Vec2f(0.625, 0.75),
            14: Gf.Vec2f(0.625, 1.0),
            15: Gf.Vec2f(0.375, 1.0),
            16: Gf.Vec2f(0.625, 0.0),
            17: Gf.Vec2f(0.875, 0.0),
            18: Gf.Vec2f(0.875, 0.25),
            19: Gf.Vec2f(0.625, 0.25),
            20: Gf.Vec2f(0.125, 0.0),
            21: Gf.Vec2f(0.375, 0.0),
            22: Gf.Vec2f(0.375, 0.25),
            23: Gf.Vec2f(0.125, 0.25)
        }

        self._AssertUVSet(mayaCubeMesh, "map1", expectedValues,
            expectedNumValues=14, expectedNumUVShells=1)

    def testImportOneMissingFaceUVSet(self):
        """
        Tests that a USD cube mesh with values for all but one face in the
        default UV set (named 'st' in USD) gets imported correctly.
        """
        mayaCubeMesh = testUsdImportUVSets._GetMayaMesh('OneMissingFaceCubeShape')

        expectedValues = {
            0: Gf.Vec2f(0.375, 0),
            1: Gf.Vec2f(0.625, 0),
            2: Gf.Vec2f(0.625, 0.25),
            3: Gf.Vec2f(0.375, 0.25),
            4: Gf.Vec2f(0.375, 0.25),
            5: Gf.Vec2f(0.625, 0.25),
            6: Gf.Vec2f(0.625, 0.5),
            7: Gf.Vec2f(0.375, 0.5),
            12: Gf.Vec2f(0.375, 0.75),
            13: Gf.Vec2f(0.625, 0.75),
            14: Gf.Vec2f(0.625, 1),
            15: Gf.Vec2f(0.375, 1),
            16: Gf.Vec2f(0.625, 0),
            17: Gf.Vec2f(0.875, 0),
            18: Gf.Vec2f(0.875, 0.25),
            19: Gf.Vec2f(0.625, 0.25),
            20: Gf.Vec2f(0.125, 0),
            21: Gf.Vec2f(0.375, 0),
            22: Gf.Vec2f(0.375, 0.25),
            23: Gf.Vec2f(0.125, 0.25)
        }

        self._AssertUVSet(mayaCubeMesh, "st", expectedValues,
            expectedNumValues=14, expectedNumUVShells=2)

    def testImportOneAssignedFaceUVSet(self):
        """
        Tests that a USD cube mesh with values for only one face in the default
        UV set (named 'st' in USD) gets imported correctly.
        """
        mayaCubeMesh = testUsdImportUVSets._GetMayaMesh('OneAssignedFaceCubeShape')

        expectedValues = {
            8: Gf.Vec2f(0.375, 0.5),
            9: Gf.Vec2f(0.625, 0.5),
            10: Gf.Vec2f(0.625, 0.75),
            11: Gf.Vec2f(0.375, 0.75)
        }

        self._AssertUVSet(mayaCubeMesh, "st", expectedValues,
            expectedNumValues=4, expectedNumUVShells=1)

    def testImportCompressedUVSets(self):
        """
        Tests that UV sets on a USD cube mesh that were compressed to constant,
        uniform, and vertex interpolations are imported correctly.

        Note that the actual values here don't really make sense as UV sets.
        We also do not perform any compression when exporting from Maya, so UV
        sets like this would have to come from some other source.
        """
        mayaCubeMesh = testUsdImportUVSets._GetMayaMesh('CompressedUVSetsCubeShape')

        # We should not see the default "map1" UV set:
        self.assertNotIn("map1", mayaCubeMesh.getUVSetNames())

        # ALL face vertices should have the same value.
        uvSetName = 'ConstantInterpSet'
        expectedValues = {}
        for i in range(24):
            expectedValues[i] = Gf.Vec2f(0.25, 0.25)
        self._AssertUVSet(mayaCubeMesh, uvSetName, expectedValues,
            expectedNumValues=1, expectedNumUVShells=1)

        # All face vertices within the same face should have the same value.
        uvSetName = 'UniformInterpSet'
        expectedValues = {}
        for i in range(0, 4):
            expectedValues[i] = Gf.Vec2f(0.0, 0.0)
        for i in range(4, 8):
            expectedValues[i] = Gf.Vec2f(0.1, 0.1)
        for i in range(8, 12):
            expectedValues[i] = Gf.Vec2f(0.2, 0.2)
        for i in range(12, 16):
            expectedValues[i] = Gf.Vec2f(0.3, 0.3)
        for i in range(16, 20):
            expectedValues[i] = Gf.Vec2f(0.4, 0.4)
        for i in range(20, 24):
            expectedValues[i] = Gf.Vec2f(0.5, 0.5)
        self._AssertUVSet(mayaCubeMesh, uvSetName, expectedValues,
            expectedNumValues=6, expectedNumUVShells=6)

        # All face vertices on the same mesh vertex (indices 0-7 for a cube)
        # should have the same value.
        uvSetName = 'VertexInterpSet'
        expectedValues = {
            0 : Gf.Vec2f(0.0, 0.0),
            1 : Gf.Vec2f(0.1, 0.1),
            2 : Gf.Vec2f(0.3, 0.3),
            3 : Gf.Vec2f(0.2, 0.2),
            4 : Gf.Vec2f(0.2, 0.2),
            5 : Gf.Vec2f(0.3, 0.3),
            6 : Gf.Vec2f(0.5, 0.5),
            7 : Gf.Vec2f(0.4, 0.4),
            8 : Gf.Vec2f(0.4, 0.4),
            9 : Gf.Vec2f(0.5, 0.5),
            10 : Gf.Vec2f(0.7, 0.7),
            11 : Gf.Vec2f(0.6, 0.6),
            12 : Gf.Vec2f(0.6, 0.6),
            13 : Gf.Vec2f(0.7, 0.7),
            14 : Gf.Vec2f(0.1, 0.1),
            15 : Gf.Vec2f(0.0, 0.0),
            16 : Gf.Vec2f(0.1, 0.1),
            17 : Gf.Vec2f(0.7, 0.7),
            18 : Gf.Vec2f(0.5, 0.5),
            19 : Gf.Vec2f(0.3, 0.3),
            20 : Gf.Vec2f(0.6, 0.6),
            21 : Gf.Vec2f(0.0, 0.0),
            22 : Gf.Vec2f(0.2, 0.2),
            23 : Gf.Vec2f(0.4, 0.4)
        }
        self._AssertUVSet(mayaCubeMesh, uvSetName, expectedValues,
            expectedNumValues=8, expectedNumUVShells=1)

    def testImportSharedFacesUVSets(self):
        """
        Tests that UV sets on a USD cube mesh that use the same UV ranges for
        multiple faces are imported correctly.
        """
        mayaCubeMesh = testUsdImportUVSets._GetMayaMesh('SharedFacesCubeShape')

        # All six faces share the same range 0.0-1.0.
        uvSetName = 'AllFacesSharedSet'
        expectedValues = {}
        for i in range(0, 24, 4):
            expectedValues[i] = Gf.Vec2f(0.0, 0.0)
        for i in range(1, 24, 4):
            expectedValues[i] = Gf.Vec2f(1.0, 0.0)
        for i in range(2, 24, 4):
            expectedValues[i] = Gf.Vec2f(1.0, 1.0)
        for i in range(3, 24, 4):
            expectedValues[i] = Gf.Vec2f(0.0, 1.0)
        self._AssertUVSet(mayaCubeMesh, uvSetName, expectedValues,
            expectedNumValues=4, expectedNumUVShells=1)

        # The faces alternate between ranges 0.0-0.5 and 0.5-1.0.
        uvSetName = 'PairedFacesSet'
        expectedValues = {}
        for i in range(0, 24, 8):
            expectedValues[i] = Gf.Vec2f(0.0, 0.0)
        for i in range(1, 24, 8):
            expectedValues[i] = Gf.Vec2f(0.5, 0.0)
        for i in range(2, 24, 8):
            expectedValues[i] = Gf.Vec2f(0.5, 0.5)
        for i in range(3, 24, 8):
            expectedValues[i] = Gf.Vec2f(0.0, 0.5)
        for i in range(4, 24, 8):
            expectedValues[i] = Gf.Vec2f(0.5, 0.5)
        for i in range(5, 24, 8):
            expectedValues[i] = Gf.Vec2f(1.0, 0.5)
        for i in range(6, 24, 8):
            expectedValues[i] = Gf.Vec2f(1.0, 1.0)
        for i in range(7, 24, 8):
            expectedValues[i] = Gf.Vec2f(0.5, 1.0)
        self._AssertUVSet(mayaCubeMesh, uvSetName, expectedValues,
            expectedNumValues=7, expectedNumUVShells=2)
    
    def testImportUVSetForMeshWithCreases(self):
        """
        Tests that importing a mesh with creases doesn't crash when importing
        UVs and that the UV set is imported properly.
        """

        # We need to load this mesh from a separate USD file because importing
        # it caused a crash (that this test verifies should no longer happen).
        if self.asFloat2:
            usdFile = os.path.join(self.inputPath, 'UsdImportUVSetsFloatTest', 'UsdImportUVSetsTestWithCreases_Float.usda')
        else:
            usdFile = os.path.join(self.inputPath, 'UsdImportUVSetsTest', 'UsdImportUVSetsTestWithCreases.usda')

        # We also need to load it using the Maya file import command because
        # going through the usdImport command works fine but using the file
        # translator caused a crash.
        cmds.file(usdFile, i=True, options="remapUVSetsTo=[['','']]")

        mayaCubeMesh = testUsdImportUVSets._GetMayaMesh('CreasedCubeShape')

        # These are the default UV values for a regular Maya polycube.
        expectedValues = {
            0: Gf.Vec2f(0.375, 0.0),
            1: Gf.Vec2f(0.625, 0.0),
            2: Gf.Vec2f(0.625, 0.25),
            3: Gf.Vec2f(0.375, 0.25),
            4: Gf.Vec2f(0.375, 0.25),
            5: Gf.Vec2f(0.625, 0.25),
            6: Gf.Vec2f(0.625, 0.5),
            7: Gf.Vec2f(0.375, 0.5),
            8: Gf.Vec2f(0.375, 0.5),
            9: Gf.Vec2f(0.625, 0.5),
            10: Gf.Vec2f(0.625, 0.75),
            11: Gf.Vec2f(0.375, 0.75),
            12: Gf.Vec2f(0.375, 0.75),
            13: Gf.Vec2f(0.625, 0.75),
            14: Gf.Vec2f(0.625, 1.0),
            15: Gf.Vec2f(0.375, 1.0),
            16: Gf.Vec2f(0.625, 0.0),
            17: Gf.Vec2f(0.875, 0.0),
            18: Gf.Vec2f(0.875, 0.25),
            19: Gf.Vec2f(0.625, 0.25),
            20: Gf.Vec2f(0.125, 0.0),
            21: Gf.Vec2f(0.375, 0.0),
            22: Gf.Vec2f(0.375, 0.25),
            23: Gf.Vec2f(0.125, 0.25)
        }

        self._AssertUVSet(mayaCubeMesh, "st", expectedValues,
            expectedNumValues=14)

    def testImportUVSetWithNameRemapping(self):
        """
        Tests the importing a mesh honors specified UVSet name remappings
        """
        if self.asFloat2: 
            usdFile = os.path.join(self.inputPath, "UsdImportUVSetsFloatTest", "UsdImportUVSetsTest_Float.usda")
        else:
            usdFile = os.path.join(self.inputPath, "UsdImportUVSetsTest", "UsdImportUVSetsTest.usda")
        cmds.file(new=True, force=True)
        cmds.usdImport(file=usdFile, shadingMode=[["none", "default"], ], remapUVSetsTo=[['st','sst'],['map1','mmap1']])

        mayaCubeMesh = testUsdImportUVSets._GetMayaMesh('DefaultUVSetCubeShape')

        # These are the default UV values for a regular Maya polycube.
        expectedValues = {
            0: Gf.Vec2f(0.375, 0.0),
            1: Gf.Vec2f(0.625, 0.0),
            2: Gf.Vec2f(0.625, 0.25),
            3: Gf.Vec2f(0.375, 0.25),
            4: Gf.Vec2f(0.375, 0.25),
            5: Gf.Vec2f(0.625, 0.25),
            6: Gf.Vec2f(0.625, 0.5),
            7: Gf.Vec2f(0.375, 0.5),
            8: Gf.Vec2f(0.375, 0.5),
            9: Gf.Vec2f(0.625, 0.5),
            10: Gf.Vec2f(0.625, 0.75),
            11: Gf.Vec2f(0.375, 0.75),
            12: Gf.Vec2f(0.375, 0.75),
            13: Gf.Vec2f(0.625, 0.75),
            14: Gf.Vec2f(0.625, 1.0),
            15: Gf.Vec2f(0.375, 1.0),
            16: Gf.Vec2f(0.625, 0.0),
            17: Gf.Vec2f(0.875, 0.0),
            18: Gf.Vec2f(0.875, 0.25),
            19: Gf.Vec2f(0.625, 0.25),
            20: Gf.Vec2f(0.125, 0.0),
            21: Gf.Vec2f(0.375, 0.0),
            22: Gf.Vec2f(0.375, 0.25),
            23: Gf.Vec2f(0.125, 0.25)
        }

        self._AssertUVSet(mayaCubeMesh, "sst", expectedValues,
            expectedNumValues=14, expectedNumUVShells=1)

        mayaCubeMesh = testUsdImportUVSets._GetMayaMesh('Map1UVSetCubeShape')

        # These are the default UV values for a regular Maya polycube.
        expectedValues = {
            0: Gf.Vec2f(0.375, 0.0),
            1: Gf.Vec2f(0.625, 0.0),
            2: Gf.Vec2f(0.625, 0.25),
            3: Gf.Vec2f(0.375, 0.25),
            4: Gf.Vec2f(0.375, 0.25),
            5: Gf.Vec2f(0.625, 0.25),
            6: Gf.Vec2f(0.625, 0.5),
            7: Gf.Vec2f(0.375, 0.5),
            8: Gf.Vec2f(0.375, 0.5),
            9: Gf.Vec2f(0.625, 0.5),
            10: Gf.Vec2f(0.625, 0.75),
            11: Gf.Vec2f(0.375, 0.75),
            12: Gf.Vec2f(0.375, 0.75),
            13: Gf.Vec2f(0.625, 0.75),
            14: Gf.Vec2f(0.625, 1.0),
            15: Gf.Vec2f(0.375, 1.0),
            16: Gf.Vec2f(0.625, 0.0),
            17: Gf.Vec2f(0.875, 0.0),
            18: Gf.Vec2f(0.875, 0.25),
            19: Gf.Vec2f(0.625, 0.25),
            20: Gf.Vec2f(0.125, 0.0),
            21: Gf.Vec2f(0.375, 0.0),
            22: Gf.Vec2f(0.375, 0.25),
            23: Gf.Vec2f(0.125, 0.25)
        }

        self._AssertUVSet(mayaCubeMesh, "mmap1", expectedValues,
            expectedNumValues=14, expectedNumUVShells=1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
