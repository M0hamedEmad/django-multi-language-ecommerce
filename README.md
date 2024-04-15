# DjangoEcommerce
### home page
![home page](https://i.ibb.co/h2xpcHG/Screenshot-from-2024-04-15-22-00-16.png)

### CheckOut Page
![CheckOut](https://i.ibb.co/VmZnK75/Screenshot-from-2024-04-15-22-08-08.png)

# Usage
It's best to install Python projects in a Virtual Environment. Once you have set up a Virtual Environment, clone this project
 ```
 git clone https://github.com/M0hamedEmad/django-multi-language-ecommerce.git
 ```
 then cd to file and Run
 ```
pip install -r requirements.txt #install required packages
python manage.py migrate # run first migration
python manage.py runserver # run the server
 ```
 then open in your browser http://127.0.0.1:8000/
 
 # Make a Superuser
 Run
 ```
 python manage.py createsuperuser
 ```
 then write a username, email, password 
 go to http://127.0.0.1:8000/admin  a Django admin
