init:
	pip install -r requirements.txt

test:
#	py.test tests

sample:
	./mbg.py --ifile templates/eight.json \
	--izfile zoom/auto_eight.json --ofile images/sz1920x1080.bmp \
	--display display/sz1920x1080.json --nogui --verbose

.PHONY: init test sample
