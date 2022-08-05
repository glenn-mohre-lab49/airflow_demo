import pendulum
from airflow.decorators import task, dag
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator

from coinrequest import BTCPrice
from os import getenv

default_args=dict(
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    tags=["btc", "api"],
)
EMAIL_RECIPIENT = getenv('PRICE_USER')

@dag(dag_id="btc_price_operator",schedule_interval=None, catchup=False, default_args=default_args)
def taskflow():
    """
    https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/example_dags/tutorial_taskflow_api_etl.html#tutorial_taskflow_api_etl
    """

    @task
    def get_btc():
        """### Gets BTC Prices from Coindesk"""
        return {'prices': BTCPrice.get_btc_prices()}
    
    @task
    def process_prices(prices: list):
        """### Transforms BTCPrices based on policy"""
        return BTCPrice.process_prices(prices)

    @task
    def compose_price_email(price_json):
        """### EmailsBTCPrices to list of defined users"""
        return BTCPrice.compose_price_email(price_json)

    message = compose_price_email(process_prices(get_btc()))
    EmailOperator(
        task_id='send_price_email',
        to=EMAIL_RECIPIENT,
        subject=message['subject'],
        html_content=message['body']
    )
    

dag = taskflow()
