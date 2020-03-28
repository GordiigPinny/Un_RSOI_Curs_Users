from TestUtils.models import BaseTestCase
from django.contrib.auth.models import User, Group


class RegisterTestCase(BaseTestCase):
    """
    Тесты для регистрации
    """
    def setUp(self):
        super().setUp()
        self.path = self.url_prefix + 'register/'
        self.data_201 = {
            'username': 'Hello',
            'password': 'World',
            'password_confirm': 'World',
        }
        self.data_400_1 = {
            'username': self.user_username,
            'password': 'RaNd0m',
        }
        self.data_400_2 = {
            'password': 'RaNd0M',
        }
        self.data_400_3 = {
            'username': 'RND',
            'password': 'RaNd0m',
        }

    def testRegisterOk(self):
        response = self.post_response_and_check_status(url=self.path, data=self.data_201, auth=False)
        self.fields_test(response, needed_fields=['username', 'email'], allow_extra_fields=False)

    def testRegisterFail_ExistingUsername(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_1, expected_status_code=400,
                                                auth=False)

    def testRegisterFail_WrongJson(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_2, expected_status_code=400,
                                                auth=False)

    def testRegisterFail_NoConfirm(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_3, expected_status_code=400,
                                                auth=False)


class UsersListTestCase(BaseTestCase):
    """
    Тест для спиского представления юзеров
    """
    def setUp(self):
        super().setUp()
        self.path = self.url_prefix + 'users/'

    def testGetUsers(self):
        response = self.get_response_and_check_status(url=self.path, auth=False)
        self.fields_test(response, needed_fields=['id', 'username', 'profile_pic_link', 'is_superuser', 'is_moderator'],
                         allow_extra_fields=False)
        self.list_test(response, User)
        self.assertEqual(len(response), 1, msg='More than one user in response')
        self.assertEqual(response[0]['username'], self.user_username, msg='Unknown user in response')


class UserDetailTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.path = self.url_prefix + f'users/{self.user.id}/'
        self.path_404 = self.url_prefix + 'users/101010101/'

    def testGetUserOk(self):
        response = self.get_response_and_check_status(url=self.path, auth=False)
        self.fields_test(response, needed_fields=['id', 'username', 'email', 'pin_sprite', 'geopin_sprite',
                                                  'unlocked_pins', 'unlocked_geopins', 'profile_pic_link',
                                                  'created_dt', 'is_superuser', 'is_moderator'],
                         allow_extra_fields=False)
        self.assertEqual(response['id'], self.user.id)

    def testGetUserFail_404(self):
        _ = self.get_response_and_check_status(url=self.path_404, expected_status_code=404, auth=False)

    def testDeleteOk(self):
        _ = self.delete_response_and_check_status(url=self.path, auth=False)

    def testDeleteFail_404(self):
        _ = self.delete_response_and_check_status(url=self.path_404, expected_status_code=404, auth=False)


class ChangePasswordTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.path = self.url_prefix + f'users/{self.user.id}/change_password/'
        self.path_404 = self.url_prefix + 'users/101010101/change_password/'
        self.new_password = self.user_password + '1'
        self.data_202 = {
            'old_password': self.user_password,
            'password': self.new_password,
            'password_confirm': self.new_password,
        }
        self.data_400_1 = {
            'old_password': self.user_password,
            'password': self.new_password,
        }
        self.data_400_2 = {
            'old_password': self.user_password,
            'password': self.new_password,
            'password_confirm': self.new_password + '1',
        }
        self.data_403 = {
            'old_password': 'EHEHE',
            'password': self.new_password,
            'password_confirm': self.new_password,
        }

    def test202_OK(self):
        self.patch_response_and_check_status(url=self.path, data=self.data_202, expected_status_code=202, auth=False)

    def test404_WrongUserId(self):
        self.patch_response_and_check_status(url=self.path_404, data=self.data_202, expected_status_code=404, auth=False)

    def test400_WrongJSON(self):
        self.patch_response_and_check_status(url=self.path, data=self.data_400_1, expected_status_code=400, auth=False)

    def test400_WrongConfirm(self):
        self.patch_response_and_check_status(url=self.path, data=self.data_400_2, expected_status_code=400, auth=False)

    def test403_WrongOldPassword(self):
        self.patch_response_and_check_status(url=self.path, data=self.data_403, expected_status_code=403, auth=False)
