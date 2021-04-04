from django.test import TestCase
from site_settings.models import Setting, SettingGroup
from site_settings.helper import get_setting, get_setting_group


class SettingTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Setting.objects.create(
            alias='test_int',
            value_type=1,
            value='569'
        )

        grp = SettingGroup.objects.create(alias='test_group_1', name='Test Group 1')
        Setting.objects.create(
            alias='p1',
            value_type=2,
            value='<a href="#">Some Data</a>',
            group=grp
        )
        Setting.objects.create(
            alias='p2',
            value_type=3,
            value='1',
            group=grp
        )
        Setting.objects.create(
            alias='p3',
            value_type=3,
            value='0',
            group=grp
        )

    def test_get_setting_one(self):
        self.assertEqual(get_setting('test_int'), 569)

    def test_get_setting_group(self):
        result_group_1 = get_setting_group('test_group_1')
        self.assertEqual(result_group_1, dict(
            p1='<a href="#">Some Data</a>',
            p2=True,
            p3=False
        ))

    def test_create_setting(self):
        self.assertEqual(get_setting('some_cfg', default=567, get_or_create=True), 567)
        self.assertTrue(Setting.objects.filter(alias='some_cfg').exists())
