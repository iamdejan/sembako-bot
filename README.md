# Sembako Bot

Send price of "sembako" automatically. For now, I will focus on cooking oil price in Indonesia, which has been in increase since December 2021.

## How to Use

### Install dependencies
Run `pip3 install -r requirements.txt`.

If you are using Mac M1 series and you cannot install `psycopg2`, follow [this guide](https://stackoverflow.com/a/67166417).

### Run Locally
Run `uvicorn main:app --reload`.

## References
- [Setup GCP Cloud functions Triggering by Cloud Schedulers with Terraform](https://medium.com/geekculture/setup-gcp-cloud-functions-triggering-by-cloud-schedulers-with-terraform-1433fbf1abbe)
- [Deploy a Dockerized FastAPI App to Google Cloud Platform](https://towardsdatascience.com/deploy-a-dockerized-fastapi-app-to-google-cloud-platform-24f72266c7ef)
- [The 'ABC' of Abstract Base Classes](https://python-course.eu/oop/the-abc-of-abstract-base-classes.php)
