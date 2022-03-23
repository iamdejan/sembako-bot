# Sembako Bot

A Telegram chat bot to send daily prices of various `sembako`.

## What is Sembako?

`Sembako` is an shorthand in Indonesian language for `sembilan bahan pokok` (English translation: `nine main (food) commodities`). It refers to 9 necessities for daily living. These commodities are:
- Rice, sago and corn
- Sugar (esp. granulated sugar)
- Vegetables dan fruits
- Meat and fish
- Cooking oil and margarine
- Milk
- Egg
- Kerosene (for cooking) and/or liquefied petroleum gas (LPG)
- Salt

While initially this bot doesn't cover *every* item in `sembako`, it is easy to add more items.

## How to Use
1) Add `@tele_sembako_bot` in Telegram.
2) Start by using `/start` command.

## Run Locally

### Install Dependencies

1) Install Python 3.9.10 and `pip3`.
2) Run `pip3 install -r requirements.txt`.
    - If you are using Mac M1 series and you cannot install `psycopg2`, follow [this guide](https://stackoverflow.com/a/67166417).

### Run The Server

Run `uvicorn main:app --reload`. Now, you can access the server at port `8000`.

## Tech Stack

- Programming language: Python 3.9.10
- Framework: [FastAPI](https://fastapi.tiangolo.com/)
- Server: serverless, using Google Cloud Run.
- Scheduler: Google Cloud Scheduler.

## How to Contribute

### Financial Support (for Indonesians only)

You can use `/donate` menu to see the information regarding available methods of donation.

### Technical Support

You can contribute in this repo, by helping me making unit tests, refactor, or adding other features.

## References
- [Setup GCP Cloud functions Triggering by Cloud Schedulers with Terraform](https://medium.com/geekculture/setup-gcp-cloud-functions-triggering-by-cloud-schedulers-with-terraform-1433fbf1abbe)
- [Deploy a Dockerized FastAPI App to Google Cloud Platform](https://towardsdatascience.com/deploy-a-dockerized-fastapi-app-to-google-cloud-platform-24f72266c7ef)
- [The 'ABC' of Abstract Base Classes](https://python-course.eu/oop/the-abc-of-abstract-base-classes.php)
