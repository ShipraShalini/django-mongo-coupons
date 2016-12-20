# django-mongo-coupons

<!--![build status](https://travis-ci.org/byteweaver/django-coupons.png)-->


A mongoengine implementaion of [django-coupons](https://github.com/byteweaver/django-coupons "Django-coupons"), A reuseable Django application for coupon gereration and handling.

Is not compatible with relational db User


## Setup instructions

1. Install `django-mongo-coupons` via pip:
   ```
   $ pip install django-mongo-coupons
   ```

2. Add `'mongo_coupons'` to `INSTALLED_APPS` in `settings.py`.


    ```Python
    INSTALLED_APPS = [
        ...
        'mongoengine'
        'rest_framework_mongoengine',
        'mongo_coupons'
        ...
    ]
    ```

3. Include `mongo_coupons.urls` in urls.py
    ```Python
    urlpatterns += [ url(r'^coupons/', include(coupon_urls)) ]
    ```

## Dependencies
* [mongoengine]('http://mongoengine.org/')
* [django-rest-framework]('http://www.django-rest-framework.org/')
* [django-rest-framework-mongoengine]('https://github.com/umutbozkurt/django-rest-framework-mongoengine.git')
* [django-mongoengine]('https://github.com/MongoEngine/django-mongoengine.git') # unstable project, needed if`AUTH_USER_MODEL` is not defined.

## Supported use cases of coupons

Supports all coupons supported by  [django-coupons](https://github.com/byteweaver/django-coupons "Django-coupons") and few more:

 * single time (default): coupon can be used one time without being bound to an user.
 * user limited: coupon can be used one time but only by a specific user.
 * limit number: coupon can be used a limited number of times, by any user once.
 * users list: coupon can be used by a defined list of users, each once.
 * unlimited: coupon can be used unlimited times, but only once by the same user.
 * usage limited: type of coupon can be any of the above but can be used only n times


## Example

###### Request

    $     curl 'http://localhost:8000/coupons/coupons/'\
         -H 'Accept: application/json; indent=4'\
         -H 'Content-Type: application/json'\
         -X POST -d '{
             "value": 50,
             "code": "",
             "type": "percentage",
             "user_limit": 3,
             "campaign": "5857afaf86a5c70681a5b783",
             "max_discount": "500"
         }'
    <sup>* campain: _id of the campain</sup>

###### Response

    {
        "id": "58590b3d86a5c770e85db279",
        "value": 50,
        "code": "KijWCoTI8xUI7tc",
        "max_discount": 500,
        "type": "percentage",
        "user_limit": 3,
        "usage_limit": 1,
        "created_at": "2016-12-20T10:42:25.701545",
        "valid_until": null,
        "kwargs": null,
        "campaign": "5857afaf86a5c70681a5b783"
    }
