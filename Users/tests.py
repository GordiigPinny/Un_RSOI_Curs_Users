from TestUtils.models import BaseTestCase
from Users.models import Profile


class LocalBaseTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.path_prefix = self.url_prefix + 'profiles/'
        self.profile = Profile.objects.create(user_id=100)


class ProfilesListTestCase(LocalBaseTestCase):
    """
    Тест для /profiles/
    """
    def setUp(self):
        super().setUp()
        self.path = self.path_prefix
        self.data_201 = {
        }

    def testGet200_OK(self):
        response = self.get_response_and_check_status(url=self.path)
        self.fields_test(response, needed_fields=['id', 'user_id', 'profile_pic_link'], allow_extra_fields=False)
        self.list_test(response, Profile)

    def testPost201_OK(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201)

    def testPost401_UnknownUser(self):
        self.token.set_authenticate(False)
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201, expected_status_code=401)

    def testPost400_UnexpectedResultFromAuthServer(self):
        self.token.set_error(self.token.ERRORS_KEYS.AUTH, self.token.ERRORS.BAD_CODE_400_TOKEN)
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201, expected_status_code=400)

    def testPost500_ServerError(self):
        self.token.set_error(self.token.ERRORS_KEYS.AUTH, self.token.ERRORS.ERROR_TOKEN)
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201, expected_status_code=500)


class ProfileTestCase(LocalBaseTestCase):
    def setUp(self):
        super().setUp()
        self.profile = Profile.objects.create(user_id=1)
        self.path = self.path_prefix + f'{self.profile.user_id}/'
        self.path_404 = self.path_prefix + f'{self.profile.user_id + 1000}/'
        self.data_202 = {
            'pin_sprite': 2,
        }

    def testGet200_OK(self):
        response = self.get_response_and_check_status(url=self.path)
        self.fields_test(response, needed_fields=['id', 'user_id', 'pin_sprite', 'geopin_sprite', 'created_dt',
                                                  'unlocked_pins', 'unlocked_geopins', 'profile_pic_link',
                                                  'achievements'],
                         allow_extra_fields=False)

    def testGet404_WrongId(self):
        _ = self.get_response_and_check_status(url=self.path_404, expected_status_code=404)

    def testPatch202_OK(self):
        _ = self.patch_response_and_check_status(url=self.path, data=self.data_202)

    def testPatch401_WrongId(self):
        _ = self.patch_response_and_check_status(url=self.path_404, data=self.data_202, expected_status_code=401)

    def testDelete204_OK(self):
        _ = self.delete_response_and_check_status(url=self.path)

    def testDelete401_WrongId(self):
        _ = self.delete_response_and_check_status(url=self.path_404, expected_status_code=401)


class AddAwardTestCase(LocalBaseTestCase):
    def setUp(self):
        super().setUp()
        self.profile = Profile.objects.create(user_id=1)
        self.path = self.path_prefix + f'{self.profile.user_id}/add_awards/'
        self.data_201_1 = {
            'award_type': 'ppin',
            'award_ids': [2, 3]
        }
        self.data_201_2 = {
            'award_type': 'upin',
            'award_ids': [2, 3]
        }
        self.data_201_3 = {
            'award_type': 'achievement',
            'award_ids': [2, 3]
        }
        self.data_400_1 = {
            'award_type': 'Not enough',
        }
        self.data_400_2 = {
            'award_type': 'no',
            'award_ids': [2, 3]
        }
        self.data_400_3 = {
            'award_type': 'ptype',
            'award_ids': 1,
        }

    def testPost201_Ppin(self):
        self.token.set_another_key('award_type', 'pin')
        response = self.post_response_and_check_status(url=self.path, data=self.data_201_1)
        for aid in self.data_201_1['award_ids']:
            self.assertTrue(aid in response['unlocked_pins'], msg='Not all pins was added')

    def testPost201_Upin(self):
        self.token.set_another_key('award_type', 'pin')
        response = self.post_response_and_check_status(url=self.path, data=self.data_201_2)
        for aid in self.data_201_2['award_ids']:
            self.assertTrue(aid in response['unlocked_geopins'], msg='Not all pins was added')

    def testPost201_Achievement(self):
        self.token.set_another_key('award_type', 'achievement')
        response = self.post_response_and_check_status(url=self.path, data=self.data_201_3)
        for aid in self.data_201_3['award_ids']:
            self.assertTrue(aid in response['achievements'], msg='Not all achievements was added')

    def testPost400_WrongJSON(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_1, expected_status_code=400)

    def testPost400_WrongType(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_2, expected_status_code=400)

    def testPost400_WrongIds(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_3, expected_status_code=400)
