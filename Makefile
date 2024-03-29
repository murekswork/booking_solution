.PHONY: test_db dev_db

config=config

test_db:
	docker-compose down
	sed -i "s/'.env'/'test.env'/g" $(config)/settings.py
	docker-compose up test_db

dev_db:
	docker-compose down
	sed -i "s/'test.env'/'.env'/g" $(config)/settings.py
	docker-compose up db
