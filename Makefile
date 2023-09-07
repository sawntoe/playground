install:
	-rm -r /etc/playground
	mkdir /etc/playground
	cp -r ./examples /etc/playground
	chmod -R a+r /etc/playground/examples
	cp ./playground.py /usr/bin/playground
	chmod a+x /usr/bin/playground

