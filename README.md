# App Inventor - Backend

⚠️ Deprecated 

Previously called as **app-builder-backend**

Installation on local machine :
- Install `python 3.7.6`.
- Run `pip install -r requirements.txt` for installing project dependencies.
- Decouple is used for env variables, add database variables in `.env` file in root directory
```
DB_NAME=app-builder
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
```
- Run migrations : `python manage.py makemigrations`, `python manage.py migrate`
- Run the application : `python manage.py runserver`

**Frontend for app-inventor**
- https://github.com/addu390/app-inventor-frontend
- Ionic 5 application.

**Application APIs**
- Since the application swagger link is not exposed (Security concerns), here is a breif note on APIs used.

1. **User CRUD Operations**
- API path : `{{host}}/v1/user/<user-id>`
- Request (`POST`) :
```
{
  "userId": "xxx",
  "displayName": "Adesh Nalpet",
  "imageUrl": "http://example.com",
  "refreshToken": "xxxx-xxxx",
  "email": "390.adesh@gmail.com",
  "serverAuthCode": "",
  "accessToken": "xxxx-xxxxx",
  "idToken": "xxxx-xxxxx",
}
```
- `UserId` cannot to UPDATED once CREATED.
- `GET` request on the same path returns user details.

2. Token refresh
- API path : `{{host}}/v1/token/<user-id>`
- By default `access_token` expires in 3600 seconds and can be refreshed with this API.

3. **Application CRUD Operations**
- API path : `{{host}}/v1/application/<user-id>`
- Request (`POST`) :
```
{
	"name": "Todos",
	"description": "JSON Placeholder API"
}
```
- `GET`, `PUT` and `DELETE` on `{{host}}/v1/token/<user-id>/<app-id>` to get application details, update and delete.

4. **Component CRUD Operations**
- API path : `{{host}}/v1/application/<user-id>/<app-id>`
- Request (`PUT`) : (This is an example for TEXT_INPUT_FIELD component)
```
{
    "component_type": 1,
    "uuid": "xxxx-xxxx",
    "values": "Default value",
    "header": "Username",
    "regex": "*",
    "placeholder": "Enter username",
    "input_type": 1
}
```
- `GET`, `PUT` and `DELETE` on `{{host}}/v1/application/<user-id>/<app-id>/<component-id>` to get component details, update and delete.

5. **All APIs are authenticated**
- `access_token` stored during `user` CREATION will be validated with every request to have the same access token in query params (Similar to Firebase).
- Further, validate the expiry of the access token.
- Auto login and logout funtionality is supported in FE (**app-inventor-frontend**)


