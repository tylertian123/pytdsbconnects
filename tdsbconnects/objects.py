import datetime
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


class School(APIObject):
    """
    A school.
    """

    @property
    def name(self) -> str:
        return self._data["SchoolName"]
    
    @property
    def code(self) -> int:
        return self._data["SchoolCode"]
    
    @property
    def is_onboard(self) -> str:
        return self._data["IsOnboard"]
    
    @property
    def id(self) -> int:
        """
        The ID of the school *for this user* (NOT an absolute ID; for that use the school code).
        """
        return self._data["SchoolSetting"]["Id"]
    
    @property
    def school_year(self) -> str:
        return self._data["SchoolSetting"]["CurrentSession"]
    
    @property
    def track(self) -> str:
        return self._data["SchoolSetting"]["SchoolYearTrack"]
    
    @property
    def school_year_start(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._data["SchoolSetting"]["SessionStart"], "%Y-%m-%dT%H:%M:%S")
    
    @property
    def school_year_end(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._data["SchoolSetting"]["SessionEnd"], "%Y-%m-%dT%H:%M:%S")


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
        return [Role(r) for r in self._data["Role"]]
    
    @property
    def birthdate(self) -> datetime.datetime:
        return datetime.datetime.strptime(self._data["BirthDate"], "%Y-%m-%dT%H:%M:%S")
    
    @property
    def schools(self) -> typing.List[School]:
        return [School(self._session, school) for school in self._data["SchoolList"]]


from .tdsbconnects import * # nopep8
