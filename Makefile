#!/bin/bash -ex

checkin: upload
	git add . && git commit -m "updating common" && git push github main

upload: build
	echo "run twine upload step" 2> /dev/null
	twine upload --repository-url https://api.packagr.app/keSRuRE/ dist/* -u tinwald@gmail.com

build: clean
	echo "run sdist build step"
	/usr/local/bin/python3 setup.py sdist

clean: 
	echo "run clean step"
	rm -f dist/*

all: checkin
