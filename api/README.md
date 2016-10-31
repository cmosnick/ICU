#API Documentation

###Contents
* [Users](#user-routes)
* [Images](#image-routes)





##User Routes
* __/user/id/\<int:user_id\>__
  * Get user info by user_id
* __/user/device/\<int:device_id\>__
  * Get user info by device id
* __/user/\<username\>__
  * Get user info by username
  ```
{
  "device_id": 0, 
  "email": "Claudie.Hill@test.com", 
  "first_name": "Claudie", 
  "last_name": "Hill", 
  "password": "Claudie", 
  "phone_number": "1025396784", 
  "user_id": 1, 
  "username": "Claudie.Hill"
}
```


* __/users/all/__
  * Get all users (sanity check)
  ```
[
  {
    "device_id": 0, 
    "email": "Claudie.Hill@test.com", 
    "first_name": "Claudie", 
    "last_name": "Hill", 
    "password": "Claudie", 
    "phone_number": "1025396784", 
    "user_id": 1, 
    "username": "Claudie.Hill"
  }, 
  {
    "device_id": 9, 
    "email": "Daniel.Noble@test.com", 
    "first_name": "Daniel", 
    "last_name": "Noble", 
    "password": "Daniel", 
    "phone_number": "8631572904", 
    "user_id": 10, 
    "username": "Daniel.Noble"
  }, 
  {
    "device_id": 5, 
    "email": "Dennis.Culver@test.com", 
    "first_name": "Dennis", 
    "last_name": "Culver", 
    "password": "Dennis", 
    "phone_number": "2605139478", 
    "user_id": 6, 
    "username": "Dennis.Culver"
  }, 
  .....,
  {
    "device_id": 4, 
    "email": "Horace.Kennamore@test.com", 
    "first_name": "Horace", 
    "last_name": "Kennamore", 
    "password": "Horace", 
    "phone_number": "1278530946", 
    "user_id": 5, 
    "username": "Horace.Kennamore"
  }
]
```

* __/user/add/__
  * POST request to add user
  * Request parameters:
    * first_name
    * last_name
    * device_id
    * username
    * password
    * phone_number
    * email
    
  Example POST request body:
  ```
{
  "device_id" = "0001",
  "first_name" = "Christina",
  "last_name" = "Mosnick",
  "username" = "cmosnick",
  "password" = "pass",
  "email" = "cmosnick07@gmail.com",
  "phone_number" = "8159751442"
}
```




##Image Routes
