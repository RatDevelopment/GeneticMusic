run:
	@python -m app.src.main -d

test:
	@coverage run -m app.test.chromosomes.intervalschromosome-tests
