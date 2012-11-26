build: buildabs

buildabs:
	poole --build --md-ext='codehilite(guess_lang=False)' --md-ext='footnotes' --base-url="http://homepages.see.leeds.ac.uk/~eeaol/"
	cp -r input/* output/ # so that there is plaintext on the site
	cp htaccess output/.htaccess

buildrel:
	poole --build --md-ext='codehilite(guess_lang=False)' --md-ext='mathjax()' 
	cp -r input/* output/ # so that there is plaintext on the site
	cp htaccess output/.htaccess

test:
	poole --build --md-ext='codehilite(guess_lang=False)' --base-url="/home/eeaol/web/output/"
	cp htaccess output/.htaccess

deploy:
	cp -rv output/* /home/eeaol/public_html/

redeploy: build deploy
