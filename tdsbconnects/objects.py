import datetime
import enum
import typing
import re
from .util import *


class Role(enum.Enum):
    """
    Represents a user's role in a school. Multiple roles may exist.
    """
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


class TimetableItem(APIObject):
    """
    An item in a (student's) timetable.
    """

    @property
    def student_number(self) -> str:
        return self._data["StudentNumber"]
    
    @property
    def course_key(self) -> str:
        return self._data["CourseKey"]
    
    @property
    def course_code(self) -> str:
        return self._data["StudentCourse"]["ClassCode"]
    
    @property
    def course_period(self) -> str:
        return self._data["StudentCourse"]["Period"]
    
    @property
    def course_block(self) -> str:
        return self._data["StudentCourse"]["Block"]
    
    @property
    def course_teacher_name(self) -> str:
        return self._data["StudentCourse"]["TeacherName"]
    
    @property
    def course_room(self) -> str:
        return self._data["StudentCourse"]["RoomNo"]
    
    @property
    def course_school_code(self) -> str:
        return self._data["StudentCourse"]["SchoolCode"]
    
    @property
    def course_date(self) -> datetime.datetime:
        return parse_datetime(self._data["StudentCourse"]["Date"])
    
    @property
    def course_cycle_day(self) -> int:
        return self._data["StudentCourse"]["CycleDay"]
    
    @property
    def course_start(self) -> datetime.datetime:
        return parse_datetime(self._data["StudentCourse"]["StartTime"])
    
    @property
    def course_end(self) -> datetime.datetime:
        return parse_datetime(self._data["StudentCourse"]["EndTime"])
    
    @property
    def course_name(self) -> str:
        return self._data["StudentCourse"]["ClassName"]
    
    @property
    def course_teacher_email(self) -> str:
        return self._data["StudentCourse"]["TeacherEmail"]
    
    @property
    def course_semester(self) -> int:
        return self._data["StudentCourse"]["Semester"]
    
    @property
    def course_term(self) -> int:
        return self._data["StudentCourse"]["Term"]
    
    @property
    def course_timeline(self) -> str:
        return self._data["StudentCourse"]["Timeline"]
    
    @property
    def course_track(self) -> str:
        return self._data["StudentCourse"]["SchoolYearTrack"]


class School(APIObject):
    """
    A school.
    """

    DAY_CYCLE_REGEX = re.compile(r"\w{3}\(([D\d]*)\)")

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
        return parse_datetime(self._data["SchoolSetting"]["SessionStart"])
    
    @property
    def school_year_end(self) -> datetime.datetime:
        return parse_datetime(self._data["SchoolSetting"]["SessionEnd"])
    
    async def timetable(self, date: datetime.date) -> typing.List[TimetableItem]:
        """
        Get the user's timetable for this school for a date as a list of timetable items.

        :param date: The date to get the timetable for (a datetime or a date).
        """
        url = f"api/TimeTable/GetTimeTable/Student/{self.code}/{date.day:02d}{date.month:02d}{date.year}"
        data = await self._session._get_endpoint(url)
        return [TimetableItem(self._session, item) for item in data["CourseTable"]]

    async def day_cycle_names(self, start_date: datetime.date, end_date: datetime.date):
        """
        Get the cycle names for a range of dates, usually observed as <weekday>(D1).

        :param start_date: The start of the range of dates to query (the first entry in the returned list corresponds to this date)
        :param end_date: The end of the range of dates to query (the last entry in the returned list corresponds to this date)
        """

        url = f"api/TimeTable/GetDayNameDayCycle/{self.code}/{self.school_year}/{self.track}/{start_date.day:02d}{start_date.month:02d}{start_date.year}/{end_date.day:02d}{end_date.month:02d}{end_date.year}"
        data = await self._session._get_endpoint(url)
        return [School.DAY_CYCLE_REGEX.match(x).group(1) for x in data]


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
        return parse_datetime(self._data["BirthDate"])
    
    @property
    def schools(self) -> typing.List[School]:
        return [School(self._session, school) for school in self._data["SchoolList"]]


from .tdsbconnects import * # nopep8
