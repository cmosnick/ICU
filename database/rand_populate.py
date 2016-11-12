import subprocess
import random
import requests
from passlib.hash import md5_crypt


NUM_USERS = 1000
NUM_IMAGES = NUM_USERS * 10

phone_numbers = [
    "6363528647",
    "6362845566",
    "5734246735",
    "6362299752",
    "8159751442"
]



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
    password = md5_crypt.encrypt(firstname)
    # random phone number
    phone = random.choice(phone_numbers)
    email = firstname + "." + lastname + "@test.com"

    # insert into database
    sql = "\"INSERT INTO users value (DEFAULT, "+ str(device_id) + ", \'"+firstname+"\', \'" + lastname +"\', \'" + username + "\', \'" + password + "\', \'" + phone + "\', \'" + email + "\');\""
    send_mysql(sql)
    print device_id;


def create_users():
    for i in range(0, NUM_USERS):
        compose_user(device_id=i)


def create_images():
    for i in range(0, NUM_IMAGES):
        create_image()

# Todo convert random xrange to randint
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
    # Insert into database
    sql = "\"INSERT INTO images value (DEFAULT, "+ str(user_id) +", '"+ filename +"', DEFAULT)\""
    send_mysql(sql)


def create_all_user_settings():
    for user_id in range(0, NUM_USERS):
        create_user_settings_for_user(user_id)


def create_user_settings_for_user(user_id=1):
    # Choose random text email or both
    enumName = random.randint(1,3)
    if enumName == 0:
        notType = 'text'
    elif enumName == 1:
        notType = 'email'
    else:
        notType = 'both'    

    #Start time
    startTime = str(random.randint(0,23)) + ":" + str(random.randint(0, 59)) 
    #End time
    endTime   = str(random.randint(0,23)) + ":" + str(random.randint(0, 59)) 

    sql = "\"INSERT INTO user_settings value( DEFAULT, '"+str(user_id)+"', "+ str(enumName) +", '"+startTime+"', '"+endTime+"');\""
    send_mysql(sql)




if __name__ == '__main__':
    create_users()
    create_images()
    create_all_user_settings()
