import enum


class UserType(enum.Enum):
    """ user type choices """
    SUPER_ADMIN = "super-admin"
    TEACHER = "teacher"
    STUDENT = "student"
