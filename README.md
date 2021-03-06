# Instructions
- Live demo is available at http://134.122.83.34:8082

- Admin panel at http://134.122.83.34:8082/admin

- GraphiQL is available at http://134.122.83.34:8082/graphql

- Dataset is used to populate database (https://www.kaggle.com/rounakbanik/the-movies-dataset/data)

- Suggestion runs on Celery, it'd take 1-2 minutes to complete (runs every time user follow/unfollow movie, star or genre)

# TODO
- Suggestion score multipliers hardcoded, can be added to settings or Config model

- Hits db in unusual counts

- GraphQL only for retrieving data, mutation needs to be added for follow and unfollow processes

- More detailed documentation

- More tests (only covers user app) 

- Search through movies and stars (for now, can be done via Django Admin)

# Endpoints

## Users

### Signup

Description: Creates a new user with given data

Endpoint `POST /user/register/`

Payload:

```
{
    "username": "string",
    "password": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
}
```

Response: 201 and UserMe object

Note: `password` and `email` are going through validators. Weak passwords or invalid emails will cause errors.

### Login

Description: Authenticates given user

Endpoint `POST /user/login/`

Payload:

```
{
    "username": "string",
    "password": "string"
}
```

Response: 200 and token object

Note: You can login with username or email. Just pass the input as "username", API will accept both.

### Logout

`Authentication token is required in this endpoint`

Description: Logout the current user

Endpoint `GET /user/logout/

Response: 204

### Auth

Authentication token is required in this endpoint`

Description: Returns the information about authed user (current user)

Endpoint `GET /user/me/`

Response: 200 and user object

## Movie

### Movie List
Authentication token is required in this endpoint`

Endpoint `GET /movie/`

Response: 200 and list of movie objects

### Movie Retrieve

Authentication token is required in this endpoint`

Endpoint `GET /movie/<:id>`

Response: 200 and movie object

### Movie Follow

Authentication token is required in this endpoint`

Endpoint `POST /movie/<:id>/follow/`

Response: 204 

### Movie Unfollow

Authentication token is required in this endpoint`

Endpoint `POST /movie/<:id>/unfollow/`

Response: 204 

## Genre

### Genre List
Authentication token is required in this endpoint`

Endpoint `GET /genre/`

Response: 200 and list of genre objects

### Genre Retrieve

Authentication token is required in this endpoint`

Endpoint `GET /genre/<:id>`

Response: 200 and genre object

### Genre Follow

Authentication token is required in this endpoint`

Endpoint `POST /genre/<:id>/follow/`

Response: 204 

### Genre Unfollow

Authentication token is required in this endpoint`

Endpoint `POST /genre/<:id>/unfollow/`

Response: 204 

## Artist

### Artist List
Authentication token is required in this endpoint`

Endpoint `GET /artist/`

Response: 200 and list of movie objects

### Artist Retrieve

Authentication token is required in this endpoint`

Endpoint `GET /artist/<:id>`

Response: 200 and movie object

### Artist Follow

Authentication token is required in this endpoint`

Endpoint `POST /artist/<:id>/follow/`

Response: 204 

### Artist Unfollow

Authentication token is required in this endpoint`

Endpoint `POST /artist/<:id>/unfollow/`

Response: 204 