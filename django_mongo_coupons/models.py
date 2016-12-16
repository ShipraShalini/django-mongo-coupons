import random
from datetime import datetime

from django.conf import settings
from django.db import IntegrityError
from django.db import models
from django.dispatch import Signal
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_mongoengine import Document as DjangoDocument
from django_mongoengine import fields as dj
from mongoengine import *

from django_mongoengine.mongo_auth.models import User
from django_mongoengine.queryset import QuerySetManager

from .coupon_settings import (
    COUPON_TYPES,
    CODE_LENGTH,
    CODE_CHARS,
    SEGMENTED_CODES,
    SEGMENT_LENGTH,
    SEGMENT_SEPARATOR,
)


try:
    user_model = settings.AUTH_USER_MODEL
except AttributeError:
    from django.contrib.auth.models import User as user_model
redeem_done = Signal(providing_args=["coupon"])


class CouponManager(QuerySetManager):
    def create_coupon(self, type, value, users=[], valid_until=None, prefix="", campaign=None, user_limit=None):
        coupon = self.create(
            value=value,
            code=Coupon.generate_code(prefix),
            type=type,
            valid_until=valid_until,
            campaign=campaign,
        )
        if user_limit is not None:  # otherwise use default value of model
            coupon.user_limit = user_limit
        try:
            coupon.save()
        except IntegrityError:
            # Try again with other code
            coupon = Coupon.objects.create_coupon(type, value, users, valid_until, prefix, campaign)
        if not isinstance(users, list):
            users = [users]
        for user in users:
            if user:
                CouponUser(user=user, coupon=coupon).save()
        return coupon

    def create_coupons(self, quantity, type, value, valid_until=None, prefix="", campaign=None):
        coupons = []
        for i in range(quantity):
            coupons.append(self.create_coupon(type, value, None, valid_until, prefix, campaign))
        return coupons

    def used(self):
        return self.exclude(users__redeemed_at__isnull=True)

    def unused(self):
        return self.filter(users__redeemed_at__isnull=True)

    def expired(self):
        return self.filter(valid_until__lt=timezone.now())


# @python_2_unicode_compatible
class Coupon(DjangoDocument):
    value = dj.IntField(verbose_name="Value", help_text=_("Arbitrary coupon value"))
    code = dj.StringField(required=False, verbose_name="Code", unique=True, max_length=30, null=True)
    type = dj.StringField(verbose_name="Type", max_length=20, choices=COUPON_TYPES)
    user_limit = dj.IntField(verbose_name="User limit", default=1, min_value=1)
    created_at = dj.DateTimeField(verbose_name="Created at", default=datetime.utcnow())
    valid_until = dj.DateTimeField(verbose_name="Valid until", blank=True, null=True,)
        # help_text=str(_(str("Leave empty for coupons that never expire"))))
    campaign = dj.ReferenceField('Campaign', verbose_name="Campaign", blank=True, null=True,
                                 related_name='coupons', dbref=True)

    # objects = CouponManager()

    meta = {
        'collection': "coupons",
        # 'indexes': ['email', 'username', 'EmpId']
    }

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = Coupon.generate_code()
        super(Coupon, self).save(*args, **kwargs)

    def expired(self):
        return self.valid_until is not None and self.valid_until < timezone.now()

    @property
    def is_redeemed(self):
        """ Returns true is a coupon is redeemed (completely for all users) otherwise returns false. """
        return self.users.filter(
            redeemed_at__isnull=False
        ).count() >= self.user_limit and self.user_limit is not 0

    @property
    def redeemed_at(self):
        try:
            return self.users.filter(redeemed_at__isnull=False).order_by('redeemed_at').last().redeemed_at
        except self.users.through.DoesNotExist:
            return None

    @classmethod
    def generate_code(cls, prefix="", segmented=SEGMENTED_CODES):
        code = "".join(random.choice(CODE_CHARS) for i in range(CODE_LENGTH))
        if segmented:
            code = SEGMENT_SEPARATOR.join([code[i:i + SEGMENT_LENGTH] for i in range(0, len(code), SEGMENT_LENGTH)])
            return prefix + code
        else:
            return prefix + code

    def redeem(self, user=None):
        try:
            coupon_user = self.users.get(user=user)
        except CouponUser.DoesNotExist:
            try:  # silently fix unbouned or nulled coupon users
                coupon_user = self.users.get(user__isnull=True)
                coupon_user.user = user
            except CouponUser.DoesNotExist:
                coupon_user = CouponUser(coupon=self, user=user)
        coupon_user.redeemed_at = timezone.now()
        coupon_user.save()
        redeem_done.send(sender=self.__class__, coupon=self)


# @python_2_unicode_compatible
class Campaign(Document):
    name = StringField()
    description = StringField()

    meta = {
        'collection': "campaign",
        # 'indexes': ['email', 'username', 'EmpId']
    }
    #
    # def __str__(self):
    #     return self.name


@python_2_unicode_compatible
class CouponUser(DjangoDocument):
    coupon = dj.ReferenceField(Coupon, dbref=True)
    user = dj.ReferenceField(User, dbref=False, verbose_name=_("User"), null=True, blank=True)
    redeemed_at = dj.DateTimeField(verbose_name="Redeemed at", blank=True, null=True)

    class Meta:
        unique_together = (('coupon', 'user'),)

    def __str__(self):
        return str(self.user)
