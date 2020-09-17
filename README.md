# pytdsbconnects
![Python 3](https://img.shields.io/pypi/pyversions/pytdsbconnects)
[![MIT License](https://img.shields.io/pypi/l/pytdsbconnects)](https://github.com/tylertian123/pytdsbconnects/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pytdsbconnects)](https://pypi.org/project/pytdsbconnects/)

A basic Python TDSB Connects API using aiohttp.

Made with info and help from @mincrmatt12.

Example usage:
```py
import asyncio
import datetime
import tdsbconnects
from getpass import getpass

async def main():
    async with tdsbconnects.TDSBConnects() as session: # type: tdsbconnects.TDSBConnects
        print("loggin in")
        await session.login(input("Username: "), getpass())
        print("getting info")
        info = await session.get_user_info()
        print(info.name, "is a", info.roles[0], "at", info.schools[0].name, "with code",
              info.schools[0].code, "in the school year", info.schools[0].school_year, "starting on",
              info.schools[0].school_year_start, "and ending on", info.schools[0].school_year_end)
        date = datetime.datetime.strptime(input("enter a date to get your timetable for (YYYY-MM-DD): "), "%Y-%m-%d")
        timetable = await info.schools[0].timetable(date)
        if timetable:
            print("that day is a day", timetable[0].course_cycle_day, "and here are your courses:")
            for item in timetable:
                print("In period", item.course_period, "(starting at", item.course_start, "and ending at",
                item.course_end, ") you have class", item.course_name, "with code", item.course_code, "(block",
                item.course_block, ") with teacher", item.course_teacher_name, "(email:", item.course_teacher_email, ")")
        else:
            print("no timetable for that day.")


asyncio.get_event_loop().run_until_complete(main())
```
