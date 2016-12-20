from rest_framework.status import HTTP_400_BAD_REQUEST


class BaseCustomException(Exception):
    """
    Used as the base class for all other exceptions
    Why? So that custom exceptions can be caught at the views
    """
    def _init__(self):
        super(BaseCustomException, self).__init__()
        self.code = 0000
        self.message = "An unknown BaseCustomException occurred"


class InvalidCouponCode(BaseCustomException):
    def __init__(self):
        super(InvalidCouponCode, self).__init__()
        self.code = HTTP_400_BAD_REQUEST
        self.message = "Invalid Coupon Code"


class CouponExpiredOrUsed(BaseCustomException):
    def __init__(self):
        super(CouponExpiredOrUsed, self).__init__()
        self.code = HTTP_400_BAD_REQUEST
        self.message = "The Coupon is either expired or used"


class CouponAlreadyUsed(BaseCustomException):
    def __init__(self):
        super(CouponAlreadyUsed, self).__init__()
        self.code = HTTP_400_BAD_REQUEST
        self.message = "The Coupon is already used"

