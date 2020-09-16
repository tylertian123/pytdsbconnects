import enum
import typing


class Role(enum.Enum):
    UNAUTHORIZED = 0
    ADMIN = 1
    STAFF = 2
    STUDENT = 3
    SUPERINTENDENT = 4
    PRINCIPAL = 5
    VICE_PRINCIPAL = 6
    TEACHER = 7
    EXEC_SUPERINTENDENT = 8


class APIObject:
    """
    Base class for all API objects.
    """
    
    def __init__(self, session: "TDSBConnects", data: typing.Dict[str, typing.Any]):
        self._session = session
        self._data = data


class User(APIObject):
    """
    A user.
    """

    @property
    def email(self) -> str:
        return self._data["Email"]
    
    @property
    def id(self) -> str:
        return self._data["UserId"]
    
    @property
    def name(self) -> str:
        return self._data["UserName"]
    
    @property
    def gender(self) -> str:
        return self._data["Gender"]
    
    @property
    def age(self) -> str:
        return self._data["Age"]
    
    @property
    def aw_user_id(self) -> str:
        return self._data["AWUserId"]
    
    @property
    def firstname(self) -> str:
        return self._data["FirstName"]

    @property
    def lastname(self) -> str:
        return self._data["LastName"]
    
    @property
    def picture(self) -> str:
        return self._data["Picture"]
    
    @property
    def thumbnail(self) -> str:
        return self._data["Thumbnail"]
    
    @property
    def principal_emails(self) -> typing.List[str]:
        return self._data["PrincipalEmailsList"]
    
    @property
    def vice_principal_emails(self) -> typing.List[str]:
        return self._data["VicePrincipalEmailsList"]
    
    @property
    def superintendent_emails(self) -> typing.List[str]:
        return self._data["SuperintendentEmailsList"]
    
    @property
    def roles(self) -> typing.List[Role]:
        return [Role(r) for r in self._data["Roles"]]


from .tdsbconnects import * # nopep8
