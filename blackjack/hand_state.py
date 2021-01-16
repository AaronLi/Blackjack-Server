import enum


class HandState(enum.IntFlag):
    INACTIVE = 0
    STANDING = enum.auto()
    ACTIVE = enum.auto()
    DOUBLING = enum.auto()