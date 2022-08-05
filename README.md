#### Airflow + Celery + Redis https://github.com/glenn-mohre-lab49/airflow_demo

The demo implementation is encapsulated in a Docker container. The need for this
should reflect the heavier infrastructure requirements for this piece of kit.

Configuring docker locally and running docker-compose up should "just work".
The key customization in the docker-compose file was copying the supporting library 
(`coinrequest`) to the site-packages of the running container, making it available to the task definition.

To define a workflow, Airflow use DAGs (Directed Acyclic Graphs) files. 
These files must be in the path defined by the configuration variable [dags_folder](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#dags-folder).

#### MVP Requirements

#### Schedule a job and be notified when it completes

The Airflow [Scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) is the service which provides this functionality.

---

#### Have my job be handled by an agent from a pool

The demo implementation uses a Celery as the [Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/index.html) of the task. Configuration of Celery includes [configuration](https://docs.celeryq.dev/en/3.1/configuration.html#celeryd-concurrency) for managing the number of concurrent workers.

---

#### Have a UI to monitor active jobs

Airflow includes a webserver running a [UI](https://airflow.apache.org/docs/apache-airflow/stable/ui.html) It can be used to monitor active jobs.

---

#### Define a job via API so new job types don't require deployments.

This hasn't been solved.
Understanding the [DagFile Processing](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dagfile-processing.html) will be the key to dynamically creating new types of jobs. 

---


##### Benefits of Airflow

- Provides web interface for monitoring, managing and executing workflows.
- Define jobs by DAGs which are executed with runtime parameters.
- Can execute in isolation, with a Celery executor, a Kubernetes executor or CeleryKubernetes executor.
- The Kubernetes support provides a mechanism for isolating and scaling tasks and workers.
- Built in executors to get quick solutions for MVP.
---
##### Challenges with Airflow

- DAG design is an art, it is key to keep workflow scheduling and task execution in distinct processes.
- Built in executors may not be optimized
  - e.g. The default PythonExecutor should not be used to run task code as it holds onto workflow metadata
  - Best practice is to use the Celery Worker  run that code, isolated from the scheduling.
  - [Execution Types](https://airflow.apache.org/docs/apache-airflow/stable/executor/index.html#executor-types)
- Deployment requirements need to be understood for the context of MS infrastructure.

#### Technology Solutions Glossary
##### Airflow - https://airflow.apache.org/docs/
Airflow is a framework for managing, scheduling and monitoring workflows. It can use a variety of backends,
including support for Kubernetes clusters to scale and isolate work.
---

##### Celery - https://docs.celeryq.dev/
Celery is a distributed task queue. Scheduling and orchestration are best handled using
a DB backed Scheduler or a framework.
---

##### Celery Worker - https://docs.celeryq.dev/en/stable/userguide/workers.html
The Worker handles Tasks from the Celery application, as received from the Broker
---
###### Redis as Celery Broker - https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html#redis

Key-value store, frequently used as the Broker for Celery messages.
---

