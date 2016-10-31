import subprocess
import random
import requests

def send_mysql(sql):
    command = ("mysql -uroot -ppass -D'capstone_icu' -e" + sql).replace("\n", "")
    print command
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# Important: make sure 'names' package isnstalled in pip
def get_rand_name():
    p = subprocess.Popen(['names', ''], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    name = p.communicate()[0].split(' ')
    return {"firstname" : name[0], "lastname": name[1]}
    
    
def compose_user(device_id = None):
    name = get_rand_name()
    firstname = name['firstname']
    lastname = name['lastname']
    username = firstname + "." + lastname
    # password is firstname
    password = firstname
    # random phone number
    phone = "".join( (str(x) for x in random.sample(xrange(10), 10)) )
    email = firstname + "." + lastname + "@test.com"

    # # Send to api for insert
    # url = "http://localhost:5000/user/add/"
    # data = {
    #     "first_name" : firstname,
    #     "last_name" : lastname,
    #     "device_id" : device_id,
    #     "username" : username,
    #     "password" : password,
    #     "phone_number" : phone,
    #     "email" : email
    # }

    sql = "\"INSERT INTO users value (DEFAULT, "+ str(device_id) + ", \'"+firstname+"\', \'" + lastname +"\', \'" + username + "\', \'" + password + "\', \'" + phone + "\', \'" + email + "\');\""
    send_mysql(sql)
    print device_id;


def create_users():
    for i in range(0, 10):
        compose_user(device_id=i)


# def create_images():
#     for i in range(0, 10):
#         create_image(user_id=i)

# def create_image(user_id):
    



if __name__ == '__main__':
    create_users()