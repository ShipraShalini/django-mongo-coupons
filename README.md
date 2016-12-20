# django-mongo-coupons

<!--![build status](https://travis-ci.org/byteweaver/django-coupons.png)-->


A mongoengine implementaion of [django-coupons](https://github.com/byteweaver/django-coupons "Django-coupons"), A reuseable Django application for coupon gereration and handling.



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


## Example

    $ curl -H 'Accept: application/json; indent=4' -u http://127.0.0.1:8000/coupons/

    ```JSON
    {
        "value": 50,
        "code": "",
        "type": "percentage",
        "user_limit": 3,
        "campaign": "5249afavhe55c75703521a5b783",
        "max_discount": "500"
    }
    ```
<sup>* campain: _id of the campain</sup>