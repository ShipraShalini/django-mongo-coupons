# django-mongo-coupons

<!--![build status](https://travis-ci.org/byteweaver/django-coupons.png)-->


An implementaion of [django-coupons](https://github.com/byteweaver/django-coupons "Django-coupons"), A reuseable Django application for coupon gereration and handling with mongoengine



## Setup instructions

1. Install `django-mongo-coupons` via pip:
   ```
   $ pip install django-mongo-coupons
   ```

2. Add `'mongo-coupons'` to `INSTALLED_APPS` in `settings.py`.


## Dependencies
    * mongoengine
    * django-mongoengine (unstable release)
    * django-rest-framework
    * django-rest-framework-mongoengine

## Supported use cases of coupons

Supports all coupons supported by  [django-coupons](https://github.com/byteweaver/django-coupons "Django-coupons") and few more:

    * single time (default): coupon can be used one time without being bound to an user.
    * user limited: coupon can be used one time but only by a specific user.
    * limit number: coupon can be used a limited number of times, by any user once.
    * users list: coupon can be used by a defined list of users, each once.
    * unlimited: coupon can be used unlimited times, but only once by the same user.
    * usage limited: type of coupon can be any of the above but can be used only n times
