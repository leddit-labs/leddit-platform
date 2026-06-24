#force write because generator can't generate if unstashed commits
generate:
	asyncapi.yaml @asyncapi/html-template -o html --force-write 

docs:
	cd html && python -m http.server 1234