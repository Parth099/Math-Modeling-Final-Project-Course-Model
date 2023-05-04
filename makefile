install-deps:
	sudo add-apt-repository universe
	sudo apt update
	sudo apt-get install python-dev graphviz libgraphviz-dev pkg-config
	pip install Cython
	pip install pipreqsnb
	pipreqsnb . --force
	pip install -r ./requirements.txt

run:
	python abm.py

clean:
	rm -rf ./img/sem*

reset:
	rm -rf ./CC-venv