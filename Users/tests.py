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
        self.fields_test(response, needed_fields=['id', 'user_id', 'pic_id'], allow_extra_fields=False)
        self.list_test(response, Profile)

    def testPost201_OK(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201)

    def testPost401_403_UnknownUser(self):
        self.token.set_authenticate(False)
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201, expected_status_code=[401, 403])

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
                                                  'unlocked_pins', 'pic_id', 'achievements', 'money', 'rating'],
                         allow_extra_fields=False)

    def testGet404_WrongId(self):
        _ = self.get_response_and_check_status(url=self.path_404, expected_status_code=404)

    def testPatch202_OK(self):
        _ = self.patch_response_and_check_status(url=self.path, data=self.data_202)

    def testPatch401_403_WrongId(self):
        _ = self.patch_response_and_check_status(url=self.path_404, data=self.data_202, expected_status_code=[401, 403])

    def testDelete204_OK(self):
        _ = self.delete_response_and_check_status(url=self.path)

    def testDelete401_WrongId(self):
        _ = self.delete_response_and_check_status(url=self.path_404, expected_status_code=401)


class AddAwardTestCase(LocalBaseTestCase):
    """
    Тесты для /add_achievement/
    """
    def setUp(self):
        super().setUp()
        self.path = self.path_prefix + f'{self.profile.user_id}/add_achievement/'
        self.data_201 = {
            'achievement_id': 2,
        }
        self.data_400_1 = {

        }
        self.data_400_2 = {
            'achievement_id': self.profile.get_achievements()[0],
        }

    def testPost201_OK(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201)

    def testPost400_WrongJSON(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_1, expected_status_code=400)

    def testPost400_OwnedAchievement(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_2, expected_status_code=400)

    def testPost401_403_AuthServiceError(self):
        self.token.set_error(self.token.ERRORS_KEYS.APP_AUTH, self.token.ERRORS.ERROR_TOKEN)
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201, expected_status_code=[401, 403])

    def testPost401_403_WrongAppToken(self):
        self.token.set_error(self.token.ERRORS_KEYS.APP_AUTH, self.token.ERRORS.BAD_CODE_401_TOKEN)
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201, expected_status_code=[401, 403])


class BuyPinTestCase(LocalBaseTestCase):
    """
    Тесты для /buy_pin/
    """

    def setUp(self):
        super().setUp()
        self.path = self.path_prefix + f'{self.profile.user_id}/buy_pin/'
        self.profile.money = 100
        self.profile.save()
        self.data_201 = {
            'pin_id': 3,
            'price': 10,
        }
        self.data_400_1 = {

        }
        self.data_400_2 = {
            'achievement_id': self.profile.get_unlocked_pins()[0],
            'price': 10,
        }
        self.data_400_3 = {
            'pin_id': 3,
            'price': 1000,
        }

    def testPost201_OK(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201)

    def testPost400_WrongJSON(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_1, expected_status_code=400)

    def testPost400_OwnedAchievement(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_2, expected_status_code=400)

    def testPost400_NotEnoughMoney(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_3, expected_status_code=400)

    def testPost401_403_AuthServiceError(self):
        self.token.set_error(self.token.ERRORS_KEYS.APP_AUTH, self.token.ERRORS.ERROR_TOKEN)
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201, expected_status_code=[401, 403])

    def testPost401_403_WrongAppToken(self):
        self.token.set_error(self.token.ERRORS_KEYS.APP_AUTH, self.token.ERRORS.BAD_CODE_401_TOKEN)
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201, expected_status_code=[401, 403])


class ChangeRatingTestCase(LocalBaseTestCase):
    """
    Тесты для /update_rating/
    """
    def setUp(self):
        super().setUp()
        self.path = self.path_prefix + f'{self.profile.user_id}/update_rating/'
        self.data_202_1 = {
            'd_rating': 100,
        }
        self.data_202_2 = {
            'd_rating': -100,
        }
        self.data_400_1 = {

        }

    def testPost201_OK(self):
        _ = self.patch_response_and_check_status(url=self.path, data=self.data_202_1)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.rating, self.data_202_1['d_rating'], msg='Rating is not zero')

    def testPost201_NegativeRating(self):
        _ = self.patch_response_and_check_status(url=self.path, data=self.data_202_2)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.rating, 0, msg='Rating is not zero')

    def testPost400_WrongJSON(self):
        _ = self.patch_response_and_check_status(url=self.path, data=self.data_400_1, expected_status_code=400)

    def testPost401_403_AuthServiceError(self):
        self.token.set_error(self.token.ERRORS_KEYS.APP_AUTH, self.token.ERRORS.ERROR_TOKEN)
        _ = self.patch_response_and_check_status(url=self.path, data=self.data_202_1, expected_status_code=[401, 403])

    def testPost401_403_WrongAppToken(self):
        self.token.set_error(self.token.ERRORS_KEYS.APP_AUTH, self.token.ERRORS.BAD_CODE_401_TOKEN)
        _ = self.patch_response_and_check_status(url=self.path, data=self.data_202_1, expected_status_code=[401, 403])

