PASSWORD: xXxkHH48gYphBzPt USER: root

### Настройка БД (mysql) на новой машине (Ubuntu)

https://tproger.ru/articles/django-sqlite-to-mysql/

### Настройка БД (mysql) на новой машине (Arch-based distros)
```shell
sudo pacman -S mariadb
```
```shell
sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
```
```shell
sudo systemctl start mysqld
```
```shell
sudo systemctl enable mysqld
```
```shell
sudo mysql_secure_installation
```
```shell
NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
 SERVERS IN PRODUCTION USE! PLEASE READ EACH STEP CAREFULLY!

In order to log into MariaDB to secure it, we'll need the current
password for the root user. If you've just installed MariaDB, and
you haven't set the root password yet, the password will be blank,
so you should just press enter here.

Enter current password for root (enter for none):
OK, successfully used password, moving on...
Setting the root password ensures that nobody can log into the MariaDB
root user without the proper authorisation.

Set root password? [Y/n] Y
New password:
Re-enter new password:
Password updated successfully!
Reloading privilege tables..
 ... Success!

By default, a MariaDB installation has an anonymous user, allowing anyone
to log into MariaDB without having to have a user account created for
them. This is intended only for testing, and to make the installation
go a bit smoother. You should remove them before moving into a
production environment.
Remove anonymous users? [Y/n] Y
 ... Success!

Normally, root should only be allowed to connect from 'localhost'. This
ensures that someone cannot guess at the root password from the network.
Disallow root login remotely? [Y/n] Y
 ... Success!

By default, MariaDB comes with a database named 'test' that anyone can
access. This is also intended only for testing, and should be removed
before moving into a production environment.
Remove test database and access to it? [Y/n] Y
 - Dropping test database...
 ... Success!
 - Removing privileges on test database...
 ... Success!

Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.
Reload privilege tables now? [Y/n] Y
 ... Success!

Cleaning up...

All done! If you've completed all of the above steps, your MariaDB
installation should now be secure.

Thanks for using MariaDB!
```
```shell
CREATE DATABASE alphabet DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
```
```shell
CREATE USER 'django'@'localhost' IDENTIFIED BY 'xXxkHH48gYphBzPt';
```
```shell
GRANT ALL PRIVILEGES ON alphabet.* TO 'django'@'localhost';
```
```shell
FLUSH PRIVILEGES;
```
```shell
CTRL-D
```

## IN VENV:
```shell
pip install mysqlclient
```
**Save your nudes:**
```shell
python manage.py dumpdata --indent=2 --exclude=contenttypes > fixtures/datadump.json
```