import unittest
import os
import sys
import shutil

sys.path.append('../../')
from JFlink import read, write



class TestJ2F(unittest.TestCase):
    def setUp(self):
        neutron = read.readj('./j2f/neutron.OUT')
        dis = read.readg('./j2f/Model_test.gdml')
        write.writef('./j2f/output', 7.8E+18, neutron, dis)

    def tearDown(self):
        shutil.rmtree('./j2f/output')

    def test_JtoF_DirName(self):
        oriDirs = os.listdir('./j2f/fisp')
        actDirs = os.listdir('./j2f/output')
        self.assertListEqual(oriDirs, actDirs)

    def test_JtoF_FileName(self):
        oriDirs = os.listdir('./j2f/fisp')
        name = oriDirs[0]
        oriFiles = os.listdir('./j2f/fisp/%s' % name)
        actFiles = os.listdir('./j2f/output/%s' % name)
        self.assertListEqual(oriFiles, actFiles)

    def test_JtoF_collapx(self):
        oriDirs = os.listdir('./j2f/fisp')
        name = oriDirs[0]
        with open('./j2f/fisp/%s/collapx.i' % name) as f:
            ori = f.read()
        with open('./j2f/output/%s/collapx.i' % name) as f:
            act = f.read()
        self.assertEqual(ori, act)

    def test_JtoF_arrayx(self):
        oriDirs = os.listdir('./j2f/fisp')
        name = oriDirs[0]
        with open('./j2f/fisp/%s/arrayx.i' % name) as f:
            ori = f.read()
        with open('./j2f/output/%s/arrayx.i' % name) as f:
            act = f.read()
        self.assertEqual(ori, act)

    def test_JtoF_input(self):
        oriDirs = os.listdir('./j2f/fisp')
        name = oriDirs[0]
        with open('./j2f/fisp/%s/input.i' % name) as f:
            ori = f.read()
        with open('./j2f/output/%s/input.i' % name) as f:
            act = f.read()
        self.assertEqual(ori, act)

    def test_JtoF_fluxes(self):
        oriDirs = os.listdir('./j2f/fisp')
        name = oriDirs[0]
        with open('./j2f/fisp/%s/fluxes' % name) as f:
            ori = f.read()
        with open('./j2f/output/%s/fluxes' % name) as f:
            act = f.read()
        self.assertEqual(ori, act)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestJ2F())
    runner = unittest.TextTestRunner()
    runner.run(suite)
