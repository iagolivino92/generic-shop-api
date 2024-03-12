### Pre requisites
Python 3.7 installed

`127.0.0.1	generic-shop.com` entry in hosts file:
 - `/private/etc/hosts` for mac
 - `/etc/hosts` for linux
 - `C:\Windows\System32\Drivers\etc\hosts` for windows

### How to install
Just clone the project or download and extract the .zip file.

Open the terminal in the cloned/extracted folder (root) and run the following commands:

`python3.7 pip3 install -r requirements.txt`

`python3.7 main.py`

After executing the commands with success, you will be able to call the api through the following url:

`http://generic-shop.com:5001/api/v1`
  
  
### How to use

Every time this project is executed, it will try to create the local admin instance if it does not exist.
   ###### Credentials:
  `user: admin@local`
  `pass: localadministrator`


- ##### Login: `/token?shop=<shop_name|shop_id>`

| method | description   | body                                                     | headers                                | response code | response body                                        |
|--------|---------------|----------------------------------------------------------|----------------------------------------|---------------|------------------------------------------------------|
| POST   | Perform login | {"email":"<valid_email>", "password":"<valid_password>"} | {"Content-Type":"multipart/form-data"} | 201           | {"access_token": "03055abb1998869831a4783e17f26d7b"} |

   
 - ##### Users: `/users`
| method | description   | body | headers                            | response code | response body                                                                                                                            |
|--------|---------------|------|------------------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get all users | -    | {"Authorization":"<access_token>"} | 200           | [{ "contact": "00000000", "email": "admin@local", "first_name": "admin", "id": 1, "last_name": "local", "role": "admin", "shop_id": 1 }] |

 - ##### Users: `/users/shop/<shop_id>`
| method | description          | body | headers                            | response code | response body                                                                                                                            |
|--------|----------------------|------|------------------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get users by shop id | -    | {"Authorization":"<access_token>"} | 200           | [{ "contact": "00000000", "email": "admin@local", "first_name": "admin", "id": 1, "last_name": "local", "role": "admin", "shop_id": 1 }] |

- ##### User: `/user?[token=<access_token> | email=<email>]`
| method | description                | body                                                                                                                                              | headers                            | response code | response body                                                                                                                            |
|--------|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get user by token or email | -                                                                                                                                                 | -                                  | 200           | [{ "contact": "00000000", "email": "admin@local", "first_name": "admin", "id": 1, "last_name": "local", "role": "admin", "shop_id": 1 }] |
| PUT    | Add new user               | { "email": "test@local", "contact": "11111111", "first_name": "test", "last_name": "local", "password":"12345678", role": "admin", "shop_id": 1 } | {"Authorization":"<access_token>"} | 200           | { "contact": "11111111", "email": "test@local", "first_name": "test", "id": 1, "last_name": "local", "role": "admin", "shop_id": 1 }     |

 - ##### User: `/user/<int:id>`
| method | description                                        | body                   | headers                                                                  | response code | response body                                                                                                                          |
|--------|----------------------------------------------------|------------------------|--------------------------------------------------------------------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get user data by id                                | -                      | {"Authorization":"<access_token>"}                                       | 200           | { "contact": "00000000", "email": "admin@local", "first_name": "admin", "id": 1, "last_name": "local", "role": "admin", "shop_id": 1 } |
| PATCH  | Update user data (must pass the field in the body) | {"contact": 12345678 } | {"Content-Type":"multipart/form-data", "Authorization":"<access_token>"} | 201           | {"success": true, "message": "user successfully updated"}                                                                              |
| DELETE | Remove user from database                          | -                      | {"Authorization":"<access_token>"}                                       | 201           | {"success": true, "message": "user successfully deleted"}                                                                              |

- ##### Shops: `/shops`
| method | description   | body                                                                                                         | headers                            | response code | response body                                                                                                           |
|--------|---------------|--------------------------------------------------------------------------------------------------------------|------------------------------------|---------------|-------------------------------------------------------------------------------------------------------------------------|
| GET    | Get all shops | -                                                                                                            | {"Authorization":"<access_token>"} | 200           | [{"address": "local_admin_shop", "contact": "0000000000", "email": "admin@local", "id": 1, "shop_name": "admin_local"}] |
| PUT    | Add new shop  | {"address": "local_admin_shop", "contact": "0000000000", "email": "admin@local", "shop_name": "admin_local"} | {"Authorization":"<access_token>"} | 201           | [{"address": "local_admin_shop", "contact": "0000000000", "email": "admin@local", "id": 1, "shop_name": "admin_local"}] |

- ##### Shop: `/shop/<int:id>`
| method | description                                         | body                   | headers                                                                  | response code | response body                                                                                                           |
|--------|-----------------------------------------------------|------------------------|--------------------------------------------------------------------------|---------------|-------------------------------------------------------------------------------------------------------------------------|
| GET    | Get shop by id                                      | -                      | {"Authorization":"<access_token>"}                                       | 200           | [{"address": "local_admin_shop", "contact": "0000000000", "email": "admin@local", "id": 1, "shop_name": "admin_local"}] |
| PATCH  | Update shop data (must pass the fields in the body) | {"contact": 12345678 } | {"Content-Type":"multipart/form-data", "Authorization":"<access_token>"} | 201           | {"success": true, "message": "shop successfully updated"}                                                               |
| DELETE | Remove shop from database                           | -                      | {"Authorization":"<access_token>"}                                       | 201           | {"success": true, "message": "shop successfully deleted"}                                                               |

- ##### Shop: `/shop/<name>`
| method | description      | body | headers                            | response code | response body                                                                                                           |
|--------|------------------|------|------------------------------------|---------------|-------------------------------------------------------------------------------------------------------------------------|
| GET    | Get shop by name | -    | {"Authorization":"<access_token>"} | 200           | [{"address": "local_admin_shop", "contact": "0000000000", "email": "admin@local", "id": 1, "shop_name": "admin_local"}] |

- ##### Join Requests: `/join-requests`
| method | description           | body | headers                            | response code | response body                                                                                                                                                                                                                                                                      |
|--------|-----------------------|------|------------------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get all join requests | -    | {"Authorization":"<access_token>"} | 200           | [ { "creation_date": "Wed, 13 Sep 2023 16:53:43 GMT", "data": "{'first_name': 'aaa', 'last_name': 'bbbb', 'email': 'a@aaa.com', 'contact': '1234567890', 'password': '12345678', 'role': 'read', 'shop_id': '1'}", "id": 1, "processed_by": null, "shop_id": 1, "status": null } ] |

- ##### Join Requests: `/join-requests/shop/<shop_id>`
| method | description                  | body | headers                            | response code | response body                                                                                                                                                                                                                                                                      |
|--------|------------------------------|------|------------------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get join requests by shop id | -    | {"Authorization":"<access_token>"} | 200           | [ { "creation_date": "Wed, 13 Sep 2023 16:53:43 GMT", "data": "{'first_name': 'aaa', 'last_name': 'bbbb', 'email': 'a@aaa.com', 'contact': '1234567890', 'password': '12345678', 'role': 'read', 'shop_id': '1'}", "id": 1, "processed_by": null, "shop_id": 1, "status": null } ] |

- ##### Join Request: `/join-request/<id>`
| method | description                             | body                                       | headers                                                                  | response code | response body                                                                                                                                                                                                                                                                |
|--------|-----------------------------------------|--------------------------------------------|--------------------------------------------------------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get join request by id                  | -                                          | {"Authorization":"<access_token>"}                                       | 200           | {"creation_date": "Wed, 13 Sep 2023 16:53:43 GMT", "data": "{'first_name': 'aaa', 'last_name': 'bbbb', 'email': 'a@aaa.com', 'contact': '1234567890', 'password': '12345678', 'role': 'read', 'shop_id': '1'}", "id": 1, "processed_by": null, "shop_id": 1, "status": null} |
| PATCH  | Update join request (accept or decline) | {"email": "a@aaa.com", "action": "accept"} | {"Content-Type":"multipart/form-data", "Authorization":"<access_token>"} | 200           | {"success": true, "message": "join request successfully accepted/user created"}                                                                                                                                                                                              |

- ##### Join Request: `/create-join-request`
| method | description         | body                                                                                                                                              | headers                            | response code | response body                                                     |
|--------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------|---------------|-------------------------------------------------------------------|
| PUT    | Create join request | {"first_name": "aaa", "last_name": "bbbb", "email": "a@aaa.com", "contact": "1234567890", "password": "12345678", "role": "read", "shop_id": "1"} | {"Authorization":"<access_token>"} | 201           | {"success": true, "message": "join request successfully created"} |

- ##### Keys: `/keys`
| method | description            | body           | headers                            | response code | response body                                                                       |
|--------|------------------------|----------------|------------------------------------|---------------|-------------------------------------------------------------------------------------|
| GET    | Get all keys (entries) | -              | {"Authorization":"<access_token>"} | 200           | [{"hash": "fd6119c4757dad902e27f41842e4ae0e", "id": 1, "join_id": 1, "shop_id": 1}] |
| POST   | Create key (entry)     | {"shop_id": 1} | {"Authorization":"<access_token>"} | 201           | {"success": true, "message": "api key successfully created"}                        |

- ##### Key: `/key/<k_hash>`
| method | description             | body | headers                            | response code | response body                                                                     |
|--------|-------------------------|------|------------------------------------|---------------|-----------------------------------------------------------------------------------|
| GET    | Get key by hash (entry) | -    | {"Authorization":"<access_token>"} | 200           | {"hash": "fd6119c4757dad902e27f41842e4ae0e", "id": 1, "join_id": 1, "shop_id": 1} |

 - ##### Employees: `/employees`
| method | description       | body                                                                                                                                          | headers                            | response code | response body                                                                                                                      |
|--------|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get all employees | -                                                                                                                                             | {"Authorization":"<access_token>"} | 200           | [{ "contact": "00000000", "email": "emp@local", "first_name": "emp", "id": 3, "last_name": "local", "role": "emp", "shop_id": 1 }] |
| PUT    | Add new employee  | { "email": "emp@local", "contact": "11111111", "first_name": "emp", "last_name": "local", "password":"12345678", role": "emp", "shop_id": 1 } | {"Authorization":"<access_token>"} | 201           | {"success": true, "message": "user successfully created"}                                                                          |

 - ##### Employee: `/employee/<int:id>`
| method | description                                            | body                   | headers                                                                  | response code | response body                                                                                                                    |
|--------|--------------------------------------------------------|------------------------|--------------------------------------------------------------------------|---------------|----------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get employee data by id                                | -                      | {"Authorization":"<access_token>"}                                       | 200           | { "contact": "00000000", "email": "emp@local", "first_name": "emp", "id": 3, "last_name": "local", "role": "emp", "shop_id": 1 } |
| PATCH  | Update employee data (must pass the field in the body) | {"contact": 12345678 } | {"Content-Type":"multipart/form-data", "Authorization":"<access_token>"} | 201           | {"success": true, "message": "user successfully updated"}                                                                        |
| DELETE | Remove employee from database                          | -                      | {"Authorization":"<access_token>"}                                       | 201           | {"success": true, "message": "user successfully deleted"}                                                                        |

 - ##### Employees: `/employees/shop/<shop_id>`
| method | description              | body | headers                            | response code | response body                                                                                                                      |
|--------|--------------------------|------|------------------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get employees by shop id | -    | {"Authorization":"<access_token>"} | 200           | [{ "contact": "00000000", "email": "emp@local", "first_name": "emp", "id": 3, "last_name": "local", "role": "emp", "shop_id": 1 }] |


 - ##### Sales: `/sales`
| method | description   | body                                                                                  | headers                            | response code | response body                                                                                                                                                                          |
|--------|---------------|---------------------------------------------------------------------------------------|------------------------------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get all sales | -                                                                                     | {"Authorization":"<access_token>"} | 200           | [{"commission": "10", "creation_date": "Wed, 13 Sep 2023 14:48:23 GMT", "id": 1, "last_update_date": "Wed, 13 Sep 2023 14:48:23 GMT", "rate": "10", "status": "paid", "value": "100"}] |
| POST   | Add new sale  | {"user_id": 1, "value": "100", "rate": "45", "commission": "45", "status": "pending"} | {"Authorization":"<access_token>"} | 201           | {"success": true, "message": "sale successfully added"}                                                                                                                                |

 - ##### Sales: `/sales/user/<user_id>`
| method | description          | body | headers                            | response code | response body                                                                                                                                                                          |
|--------|----------------------|------|------------------------------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get sales by user id | -    | {"Authorization":"<access_token>"} | 200           | [{"commission": "10", "creation_date": "Wed, 13 Sep 2023 14:48:23 GMT", "id": 1, "last_update_date": "Wed, 13 Sep 2023 14:48:23 GMT", "rate": "10", "status": "paid", "value": "100"}] |

 - ##### Sale: `/sale/<sale_id>`
| method | description                                        | body                  | headers                                                                  | response code | response body                                                                                                                                                                        |
|--------|----------------------------------------------------|-----------------------|--------------------------------------------------------------------------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GET    | Get sale by id                                     | -                     | {"Authorization":"<access_token>"}                                       | 200           | {"commission": "10", "creation_date": "Wed, 13 Sep 2023 14:48:23 GMT", "id": 1, "last_update_date": "Wed, 13 Sep 2023 14:48:23 GMT", "rate": "10", "status": "paid", "value": "100"} |
| PATCH  | Update sale data (must pass the field in the body) | {"commission": "15" } | {"Content-Type":"multipart/form-data", "Authorization":"<access_token>"} | 201           | {"success": true, "message": "sale successfully updated"}                                                                                                                            |
| DELETE | Remove sale from database                          | -                     | {"Authorization":"<access_token>"}                                       | 201           | {"success": true, "message": "sale successfully deleted"}                                                                                                                            |
