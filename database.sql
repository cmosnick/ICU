/*
  The following few sections create the tables for the database
*/

/*
	To be able to use the commands "DROP TABLE IF EXISTS.." we must first
	delete the foreign keys referencing that table. Because we are starting
	the database from scratch everytime we run this script, we are deleting
	all the foreign keys every time.
*/
delimiter $$
DROP procedure IF EXISTS drop_keys;$$
create procedure drop_keys()
begin

IF EXISTS( SELECT table_name
  FROM INFORMATION_SCHEMA.TABLES
  WHERE (table_name LIKE 'user_settings'
    or table_name LIKE 'log'
    or table_name LIKE 'images'
    or table_name LIKE 'sent_images')
  and table_schema LIKE 'capstone_icu')
THEN
  ALTER TABLE user_settings DROP FOREIGN KEY user_settings_ibfk_1;
  ALTER TABLE user_settings DROP FOREIGN KEY user_settings_ibfk_2;
  ALTER TABLE log DROP FOREIGN KEY log_ibfk_1;
  ALTER TABLE images DROP FOREIGN KEY images_ibfk_1;
  ALTER TABLE sent_images DROP FOREIGN KEY sent_images_ibfk_1;
  ALTER TABLE sent_images DROP FOREIGN KEY sent_images_ibfk_2;
END IF;

end $$

call drop_keys();
/*
  The table "users" will contain all the users for the security system

  user_id is the unique identifier for each user
  device_id is the identifier for the security system device
  first_name and last_name are simply the first and last names of the user
  username is the name that the user uses to sign in to the website
  password is the password used to sign in to the website (We should definitely
    rework this table or add an authentication table for password hashing)
  phone_number and email are going to be used to send the images and information
    to the user
  Compound primary key of user_id and device_id because a user can own more than
    one device, and a device can be registered to one or more users
*/
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
	user_id INTEGER AUTO_INCREMENT,
	device_id INTEGER,
  first_name VARCHAR(30) NOT NULL,
  last_name VARCHAR(40) NOT NULL,
  username VARCHAR(20) NOT NULL,
  password VARCHAR(20) NOT NULL,
  phone_number VARCHAR(11) NOT NULL,
  email VARCHAR(50) NOT NULL,
  PRIMARY KEY (user_id, device_id)
);

/*
  This table contains the available notification options the user can choose.

  notification_id is the unique identifier for each notification option
  name is the name of the option (text, email, both)
*/
DROP TABLE IF EXISTS notification_options CASCADE;
CREATE TABLE notification_options (
	notification_id INTEGER AUTO_INCREMENT,
  name ENUM ('text', 'email', 'both'),
	PRIMARY KEY(notification_id)
);

/*
  This table contains the settings the user sets their account to. For example,
    a user can set the time of day they want the security system to be active,
    and they can choose whether they want a text, email, or both sent to them
    when the camera goes off.

  setting_id is the unique identifier of this specific setting
  user_id is the id referencing a user in the users table
  notification_option_id references the notification_options table
  start_time is the time the user would like this notification to begin
  end_time is the time the user would like this notiication to end
  Compound primary key of setting_id and user_id because users can choose one or
    more settings
*/
DROP TABLE IF EXISTS user_settings CASCADE;
CREATE TABLE user_settings (
	setting_id INTEGER AUTO_INCREMENT,
	user_id INTEGER,
  notification_option_id INTEGER,
	start_time TIME,
	end_time TIME,
	FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
	FOREIGN KEY (notification_option_id) REFERENCES notification_options(notification_id) ON DELETE CASCADE,
	PRIMARY KEY(setting_id, user_id)
);

/*
  This table keeps a log of all the users' actions when interacting with
    the web application.

  log_id is the unique identifier for each entry in the log table
  user_id references the users table
  action is the action that is being logged into the database
    options include: image taken, text sent, sign in, sign out, alter accout,
      initial activation
  date_time is the date and time of when the action took place
*/
DROP TABLE IF EXISTS log CASCADE;
CREATE TABLE log (
  log_id INTEGER AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  action ENUM ('image taken', 'text sent', 'email sent', 'sign in', 'sign out', 'alter accout', 'initial activation'),
  date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  PRIMARY KEY(log_id)
);

/*
  This table contains all the images that the camera takes

  image_id is a unique identifier for each image
  user_id references a user in the users table
  image is the image taken by the security system hardware
  date_time is the date and time of when the image was taken
*/
DROP TABLE IF EXISTS images CASCADE;
CREATE TABLE images (
  image_id INTEGER AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  image VARCHAR(200) NOT NULL,
  date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  PRIMARY KEY(image_id)
);

/*
  This table keeps tabs on which images the security device took were sent
    to a user of the system.

  image_id references an image in the images table
  user_id references the user in the user table
  date_time refers to the date and time of when the email or text was sent
  action refers to whether an email or a text were sent to the user
  Compound primary key because users can have one or many images sent to them
    and an image can have one or more users to send to
*/
DROP TABLE IF EXISTS sent_images CASCADE;
CREATE TABLE sent_images (
	image_id INTEGER AUTO_INCREMENT,
	user_id INTEGER,
	date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  action ENUM ('text', 'email'),
  FOREIGN KEY (image_id) REFERENCES images(image_id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
	PRIMARY KEY(image_id, user_id)
);

/*
  Creates indexes on the tables in the database

	Creates four indexes on the user_id field for tables log, sent_images, user_settings, and images.
	This is done because most queries will have user_id in the search criteria,
	and since these fields are not in the primary key/not the first field in the
	primary key in any of these tables, we need to create an index for quick
	retrieval.
*/
CREATE INDEX user_id_log_idx ON log(user_id);
CREATE INDEX user_id_images_idx ON images(user_id);
CREATE INDEX user_id_sent_images_idx ON sent_images(user_id);
CREATE INDEX user_id_user_settings_idx ON user_settings(user_id);

/*
  Creates triggers for the database
*/
