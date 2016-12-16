from mongoengine import fields
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer

from django_mongo_coupons.models import Coupon, Campaign, CouponUser


class CouponGenSerializer(DocumentSerializer):
    campaign_name = serializers.CharField(required=False)
    
    class Meta:
        model = Coupon
        depth = 4
        fields = '__all__'

    def create(self, validated_data):
        campaign_name = validated_data.pop('campaign_name', None)
        instance = super(CouponGenSerializer, self).create(validated_data)
        if campaign_name:
            campaign = Campaign.objects.get(name=campaign_name)
            instance.campaign = campaign
            instance.save()
        return instance


class CampaignSerializer(DocumentSerializer):
    class Meta:
        model = Campaign
        depth = 4
        fields = '__all__'


class CouponUserSerializer(DocumentSerializer):
    class Meta:
        model = CouponUser
        depth = 4
        fields = '__all__'

