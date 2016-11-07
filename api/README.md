#API Documentation

###Contents
* [Users](#user-routes)
* [Notifications](#notification-settings-routes)
* [Images](#image-routes)





##User Routes

* __/user/id/\<int:user_id\>__
  * GET user info by user_id
* __/user/device/\<int:device_id\>__
  * GET user info by device id
* __/user/\<username\>__
  * GET user info by username
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
  * GET all users (sanity check)
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


##Notification Settings Routes

* __/notification_options/\<int:not_id\>__
 * GET notification settings by notification id
* __/notification_options/user/\<username\>__
 * GET notification settings by user name
* __/notification_options/user/id/\<int:user_id\>__
 * GET notfication settings by user id


```

```





##Image Routes

* __/image/info/id/\<int:image_id\>__
 * GET image info (metadata, not actual image) by image id
 
 _http://localhost:5000/image/info/id/2_ :
 ```
 {
  "date_time": "Mon, 31 Oct 2016 16:36:46 GMT", 
  "image": "46b4fe09-b0c9-4f8e-aec1-c0c133180024.jpg", 
  "image_id": 2, 
  "user_id": 2
 }
 ```

* __/image/info/user/id/\<int:user_id\>__
 * GET image ids for a user by user_id
* __/image/info/user/\<username\>__
 * GET image ids for a user by username

 _http://localhost:5000/image/info/user/id/2_ :
 ```
 [{
    "date_time": "Mon, 31 Oct 2016 16:46:27 GMT", 
    "image": "17980316-0b5b-46f2-9ca6-91ee1f2aa677.png", 
    "image_id": 5, 
    "user_id": 2
  }, 
  {
    "date_time": "Mon, 31 Oct 2016 17:37:59 GMT", 
    "image": "Mario_png.png", 
    "image_id": 13, 
    "user_id": 2
  }, 
  {
    "date_time": "Mon, 31 Oct 2016 17:37:59 GMT", 
    "image": "squirrel.jpg", 
    "image_id": 20, 
    "user_id": 2
  }
]
 ```

* __/image/add/\<int:device_id\>__
 * POST image to database
 * Request parameters:
  * header:
   * content-type: application/x-www-form-urlencoded
  * body
   * file : \<file\>
 
