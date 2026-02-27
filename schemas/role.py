"""User role enumeration for authorization.

This module defines the available user roles for
role-based access control.
"""

from enum import Enum


class Role(Enum):
    """Enumeration of user roles for authorization.

    Used to control access to different API endpoints
    and functionality based on user privileges.

    Attributes:
        MEMBER: Standard user with basic access.
        ADMIN: Administrator with full access.
    """

    MEMBER = 'MEMBER'
    ADMIN = 'ADMIN'