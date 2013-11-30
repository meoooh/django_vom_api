django_api_vom
==============

* 초기설정
  * pip install -r requirement.txt
  * ./manage syncdb
  * ./manage.py schemamigration vom --initial
  * vi vom/migrations/0001_initial.py
     * http://django-rest-framework.org/api-guide/authentication#schema-migrations
  * ./manage.py migrate vom --fake
  * 