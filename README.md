# Movie Catalog Service
This service manages the movie catalog with Movie Content Service. Movie catalog service requests [Movie Content Service](https://github.com/salimildere/MovieContent) to access the content it needs.


### Run the app in Docker

Everything is containerized. So all you need is Docker installed, and then you can build and run:

```
docker-compose up -d --build
```

And your app will be up on the *port 8080*

### Test

```
docker exec -it log-movie_catalog_djangoCatalog_1 python manage.py test
```

### Swagger OPENAPI Documentation

- http://localhost:8080/swagger/


### Django Admin Dashboard


You can create a super user to access admin Dashboard

```
docker exec -it log-movie_catalog_djangoCatalog_1 python manage.py createsuperuser
```

Then you can be visit this url for admin page:

- http://localhost:8080/admin

