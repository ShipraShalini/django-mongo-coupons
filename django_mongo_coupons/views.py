from django.conf import settings
from django.http import Http404
from mongoengine import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_mongoengine.viewsets import ModelViewSet

from django_mongo_coupons.coupon_settings import User
from django_mongo_coupons.models import Coupon, Campaign, CouponUser
from django_mongo_coupons.serializer import CouponGenSerializer, CampaignSerializer


class CouponGenerationView(ModelViewSet):
    model = Coupon
    serializer_class = CouponGenSerializer
    lookup_field = 'code'
    queryset = Coupon.objects

    def get_queryset(self):
        return Coupon.objects.all()

    def retrieve(self, request, *args, **kwargs):
        amount = int(request.query_params.get('amount', None))
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        amount = instance.apply_coupon(amount)
        return_dict = serializer.data
        return_dict['amount'] = amount
        return Response(return_dict)


class CampaignView(ModelViewSet):
    model = Campaign
    serializer_class = CampaignSerializer
    queryset = Campaign.objects
    lookup_field = 'name'


    def get_queryset(self):
        return Campaign.objects.all()


class CouponView(APIView):

    def post(self, request):
        code = request.data['code']
        types = request.data['types']
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            raise ValidationError(_("This code is not valid."))

        if request.user is None and coupon.user_limit is not 1:
            # coupons with can be used only once can be used without tracking the user, otherwise there is no chance
            # of excluding an unknown user from multiple usages.
            raise ValidationError(_(
                "The server must provide an user to this form to allow you to use this code. Maybe you need to sign in?"
            ))

        if coupon.is_redeemed:
            raise ValidationError(_("This code has already been used."))

        try:  # check if there is a user bound coupon existing
            user = User.objects.get(request.user)
            user_coupon = CouponUser.objects.get(user=user)
            if user_coupon.redeemed_at is not None:
                raise ValidationError(_("This code has already been used by your account."))
        except CouponUser.DoesNotExist:
            if coupon.user_limit is not 0:  # zero means no limit of user count
                # only user bound coupons left and you don't have one
                if coupon.user_limit is coupon.users.filter(user__isnull=False).count():
                    raise ValidationError(_("This code is not valid for your account."))
                if coupon.user_limit is coupon.users.filter(redeemed_at__isnull=False).count():  # all coupons redeemed
                    raise ValidationError(_("This code has already been used."))
        if types is not None and coupon.type not in types:
            raise ValidationError(_("This code is not meant to be used here."))
        if coupon.expired():
            raise ValidationError(_("This code is expired."))
        return code



