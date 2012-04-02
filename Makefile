build: 
	poole --build --md-ext='codehilite' --base-url="http://homepages.see.leeds.ac.uk/~eeaol/"

test:
	poole --build --md-ext='codehilite' --base-url="/home/eeaol/web/output/"

deploy:
	cp -rv output/* /home/eeaol/public_html/

redeploy: build deploy
