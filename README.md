# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/edx/edx-name-affirmation/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                          |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| edx\_name\_affirmation/\_\_init\_\_.py                        |        1 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/admin.py                               |       14 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/api.py                                 |       68 |        0 |       24 |        1 |     99% | 227-\>230 |
| edx\_name\_affirmation/apps.py                                |        6 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/exceptions.py                          |       10 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/handlers.py                            |       56 |        2 |       14 |        1 |     96% |     72-73 |
| edx\_name\_affirmation/models.py                              |       59 |        1 |        6 |        0 |     98% |        17 |
| edx\_name\_affirmation/name\_change\_validator.py             |       35 |        0 |       10 |        0 |    100% |           |
| edx\_name\_affirmation/serializers.py                         |       44 |        0 |        4 |        0 |    100% |           |
| edx\_name\_affirmation/services.py                            |       16 |        0 |        8 |        0 |    100% |           |
| edx\_name\_affirmation/signals.py                             |       12 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/statuses.py                            |       10 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/tasks.py                               |       65 |        0 |       22 |        0 |    100% |           |
| edx\_name\_affirmation/tests/\_\_init\_\_.py                  |        0 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/tests/test\_api.py                     |      134 |        0 |       10 |        1 |     99% | 121-\>124 |
| edx\_name\_affirmation/tests/test\_handlers.py                |      163 |        0 |        6 |        0 |    100% |           |
| edx\_name\_affirmation/tests/test\_models.py                  |       59 |        1 |        4 |        1 |     97% |       112 |
| edx\_name\_affirmation/tests/test\_name\_change\_validator.py |       21 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/tests/test\_services.py                |       17 |        0 |        4 |        0 |    100% |           |
| edx\_name\_affirmation/tests/test\_signals.py                 |       33 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/tests/test\_tasks.py                   |       55 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/tests/test\_views.py                   |      239 |        0 |       22 |        0 |    100% |           |
| edx\_name\_affirmation/tests/utils.py                         |       26 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/urls.py                                |        4 |        0 |        0 |        0 |    100% |           |
| edx\_name\_affirmation/views.py                               |      106 |        0 |       20 |        0 |    100% |           |
| **TOTAL**                                                     | **1253** |    **4** |  **154** |    **4** | **99%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/edx/edx-name-affirmation/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/edx/edx-name-affirmation/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/edx/edx-name-affirmation/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/edx/edx-name-affirmation/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fedx%2Fedx-name-affirmation%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/edx/edx-name-affirmation/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.