# Mail Sending Web App Backend

## Authors
[Abhinav Garg](https://github.com/ABHINAVGARG05/Mail_Sender)

## Clone the Repository
```bash 
git clone
https://github.com/ABHINAVGARG05/Mail-sender.git
```
## Create Virtual Environment
```bash
pip install virtualenv
```
```bash
python -m venv myenv
```
## Activate Virtual Environment
```bash
myenv\Scripts\activate
```
## Download Required Dependencies in Virtual Environment
```bash 
 pip install -r requirements.txt
```
### After all the requirements Download

### Make Docker-compose.yml file

### To run on Docker
```bash
docker-compose --up build
```
### To run Locally
```bash 
flask Run
```

## API ENDPOINTS 
### User Register
``` POST /register```
#### Request Body
```json
{
    "username":"username",
    "password":"password"
}
```
### User login
``` POST /login```
#### Request Body
```json
{
    "username":"username",
    "password":"password"
}
```
#### Response Body
```json
{
    "token":"JWT Token"
}
```

### Get All Mails
```GET /get-mails```
 
- Include the following header in your requests:
```http
Authorization: Bearer <your-token-here>
```

### Postman Collection
To access the Postman Collection Click

[Postman Collection](https://elements.getpostman.com/redirect?entityId=36199199-b6433bf4-28da-40b7-8d33-ba3a4b9edfcc&entityType=collection)


