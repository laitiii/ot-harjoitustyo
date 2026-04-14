# PyTD

This project is a tower defense game. The goal of the game is to defeat enemies moving along a path by placing different types of towers along the path.

In its current state the game only creates the level and there is no actual gameplay. 

## Notice about Python version

The game is tested to work on Python 3.12.3, newer versions might be incompatible. 

## Documentation

- [Vaatimusmäärittely](https://github.com/laitiii/ot-harjoitustyo/blob/main/dokumentaatio/vaatimusmaarittely.md)
- [Tuntikirjanpito](https://github.com/laitiii/ot-harjoitustyo/blob/main/dokumentaatio/tuntikirjanpito.md)
- [Changelog](https://github.com/laitiii/ot-harjoitustyo/blob/main/dokumentaatio/changelog.md)
- [Arkkitehtuurikuvaus](https://github.com/laitiii/ot-harjoitustyo/blob/main/dokumentaatio/arkkitehtuuri.md)

## Installation 

1. Install dependencies:

```bash
poetry install
```

2. Start the game:

```bash
poetry run invoke start
```

## Commands

### Testing

Tests are run with:

```bash
poetry run invoke test
```

### Test coverage

A test coverage report can be generated with the following command:

```bash
poetry run invoke coverage-report
```

The report is generated in the htmlcov folder and can be viewed by opening the index.html in your browser of choice. 

### Test pylint

A pylint code quality check can be done with:

```bash
poetry run invoke pylint
```
