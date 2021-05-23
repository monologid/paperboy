# PAPERBOY

A very simple and customizable task/worker + cron tool. 

And yes, you can create your own plugin to be used in the job!

The name of `Paper Boy` is inspired by a game called [Paper Boy](https://www.google.com/search?client=firefox-b-d&q=paper+boy+game) released in 1984.

### Why is this tool created?

With so many years of software engineering development, we always write a customized worker.
Instead of writing it several times, by using this, we only need to create a plugin that reusable for other projects.

### Why is this tool created using Python?

The easiest programming language for data manipulation. =9

### Getting started

Please make sure that you have install Python 3.x and Redis (currently used as main storage, but you can customize it).

Run `make install` to install the requirements. Configure the `.env`.

Open a new terminal, run `make server` to run the web app.

Open another new terminal, run `make worker` to run the worker.

### How-to change the Storage engine

You can create the storage engine according to your preferences by implementing all required methods in `interfaces/storage`.

And go to `core/storage.py` and add the storage engine.

### Author

[Ais](https://github.com/madebyais)

### License

[Apache-2.0](LICENSE)