test:
	@for i in *_test.py; do python $$i; done


clean:
	rm -f *~ *.pyc