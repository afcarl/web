build: 
	poole --build --md-ext='codehilite' --base-url="http://homepages.see.leeds.ac.uk/~eeaol/"
	cp htaccess output/.htaccess

test:
	poole --build --md-ext='codehilite' --base-url="/home/eeaol/web/output/"
	cp htaccess output/.htaccess

deploy:
	cp -rv output/. /home/eeaol/public_html/

redeploy: build deploy
