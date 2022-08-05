import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

from get_price import BTCPrice

with DAG(
    dag_id="btc_price_operator",
    schedule_interval=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["btc", "api"],
    ) as dag:
        get_btc = PythonOperator(task_id="get_btc_price", python_callable=BTCPrice.get_btc_price)



