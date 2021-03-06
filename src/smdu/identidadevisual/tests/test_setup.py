# -*- coding: utf-8 -*-
from plone import api
from plone.browserlayer.utils import registered_layers
from smdu.identidadevisual.config import PROJECTNAME
from smdu.identidadevisual.interfaces import IAddOnLayer
from smdu.identidadevisual.testing import INTEGRATION_TESTING

import unittest


class InstallTestCase(unittest.TestCase):

    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = self.portal['portal_quickinstaller']
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        self.assertIn(IAddOnLayer, registered_layers())

    def test_setup_permission(self):
        permission = 'smdu.identidadevisual: Setup'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Manager', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_version(self):
        profile = 'smdu.identidadevisual:default'
        setup_tool = self.portal['portal_setup']
        version = setup_tool.getLastVersionForProfile(profile)[0]
        self.assertEqual(version, '1')


class UninstallTestCase(unittest.TestCase):

    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        self.assertNotIn(IAddOnLayer, registered_layers())
