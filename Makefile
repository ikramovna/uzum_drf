mig:
	./manage.py makemigrations
	./manage.py migrate
admin:
	python3 manage.py createsuperuser  --username admin --email  admin@mail.com

req:
	pip3 freeze > requirements.txt

install-req:
	pip3 install -r requirements.txt
