from src.MyBeans.Gender import Gender


class User:
    """
    该类用于封装用户信息
    """
    _uid = None
    _uname = None
    _gender = None
    _org = None
    _phone = None
    _email = None

    def __init__(self, uname: str, gender: Gender, org: str, phone: str, email: str, uid=None) -> None:
        self.uid = uid
        self.uname = uname
        self.gender = gender
        self.org = org
        self.phone = phone
        self.email = email

    """ 下面是getter和setter方法 """
    """ 注意：uid不能修改 """

    @property
    def uname(self):
        return self._uname

    @uname.setter
    def uname(self, uname: str) -> None:
        self._uname = uname

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender: Gender) -> None:
        self._gender = gender

    @property
    def org(self) -> str:
        return self._org

    @org.setter
    def org(self, org: str) -> None:
        self._org = org

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, phone: str) -> None:
        self._phone = phone

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        self._email = email
