import sys
import os

# This is to include the other folders paths for python to look in
PROJECT_ROOT = os.path.dirname('/application/')  # NOQA
sys.path.insert(0, os.path.join(PROJECT_ROOT, "source"))  # NOQA

from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

from dag_helpers import (
    noop,
)

# Variables hit the database, better to get once and store
sample_variable = Variable.get('sample_variable')


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 3, 20),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,
    "provide_context": True,
}

SampleDag = DAG(
    "sample-dag",
    default_args=default_args,
    schedule_interval=None,
    on_success_callback=noop,
    on_failure_callback=noop,
)

with SampleDag:
    start = DummyOperator(
        task_id='start'
    )

    no_operation = PythonOperator(
        task_id='no_operation',
        python_callable=noop,
        op_kwargs={
            'sample_variable': sample_variable,
        }
    )

    start >> no_operation
