import subprocess
import random
import requests

NUM_USERS = 10
NUM_IMAGES = NUM_USERS * 10



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
    for i in range(0, NUM_USERS):
        compose_user(device_id=i)


def create_images():
    for i in range(0, NUM_IMAGES):
        create_image()

def create_image():
    # Get random user id
    user_id = random.sample(xrange(NUM_USERS), 1)[0]
    # Get image name (one of three)
    imageNumber = random.sample(xrange(3), 1)[0]
    if imageNumber == 0:
        filename = "Mario_png.png"
    elif imageNumber == 1:
        filename = "squirrel.jpg"
    else:
        filename = "victor-surge-e569f5dc-0425-4d09-a45b-0edd9b0d9478.jpg"
    sql = "\"INSERT INTO images value (DEFAULT, "+ str(user_id) +", '"+ filename +"', DEFAULT)\""
    send_mysql(sql)

if __name__ == '__main__':
    # create_users()
    create_images()