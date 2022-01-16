<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h2 align="center">JustGram</h2>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/ramazankilimci/grammar-checker)](https://github.com/ramazankilimci/grammar-checker/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/ramazankilimci/grammar-checker)](https://github.com/ramazankilimci/grammar-checker/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Don't worry about your sentences anymore!
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This project will allow you to check your sentences in English or Turkish. It is being developed for SWE599 class in Boğaziçi University.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

* Before you start implementing/installing this project, pick an IDE of your choice. I've used [Visual Studio Code](https://code.visualstudio.com/download). You can go direclty to link and download it.

* Install [docker](https://docs.docker.com/get-docker/) on your desktop. You can use click on docker link and download of your choice.

* Check your docker version to see if everything is working fine.

```
docker -v
```

### Installing

A step by step basic instructions were provided below. This will be extended when project grows time to time.

1) Clone the git repository.

```
git clone https://github.com/ramazankilimci/grammar-checker.git
```

2) Go to application folder.

```
cd grammar-checker
```

3) Run the below docker command.

```
docker compose up
```

4) You will reach the application via http://localhost.

## 🔧 Running the tests <a name = "tests"></a>

Below you can find the detailed information regarding tests.

### How to run unit tests

These tests checks for every method if they are working as expected or not. To run the tests, please execute below command.

```
python manage.py test
```

### And coding style tests

For coding sytle tests, this project uses [pyling-django](https://github.com/PyCQA/pylint-django) which is a pylint plugin for Django. To run linting manually, please execute the below command.

```
pylint --load-plugins pylint_django --django-settings-module=swe599_project.settings
```


## 🚀 Deployment <a name = "deployment"></a>

Please go to the below link to reach local deployment details.    
[Local Deployment Wiki Page](https://github.com/ramazankilimci/grammar-checker/wiki/Local-Deployment)

## ⛏️ Built Using <a name = "built_using"></a>

- [PostgreSQL](https://www.postgresql.org/) - Database
- [Django](https://www.djangoproject.com/) - Web Framework
- [Azure](https://azure.microsoft.com/en-us/) - Cloud Environment

## ✍️ Authors <a name = "authors"></a>

- [@ramazankilimci](https://github.com/ramazankilimci) - Idea & Initial work


## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Suzan Üsküdarlı (Advisor)

