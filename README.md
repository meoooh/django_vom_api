django_api_vom
==============

##초기설정

    pip install -r requirement.txt
    vi django_vom/settings.py # INSTALLED_APPS에서 'south' 주석.
    ./manage.py syncdb # settings.py에 'south' 주석처리되어있는 상태로 이 명령 실행해야함.
    vi django_vom/settings.py # INSTALLED_APPS에서 'south' 주석해제.
    ./manage.py syncdb # settings.py에 'south' 주석 해제된 상태로명령 실행
    rm -rf vom/migrations
    ./manage.py schemamigration vom --initial
    vi vom/migrations/0001_initial.py # http://django-rest-framework.org/api-guide/authentication#schema-migrations
    
    needed_by = (
        ('authtoken', '0001_initial'),
    )
    
    ./manage.py migrate vom --fake
