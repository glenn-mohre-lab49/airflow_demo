### Comparing Job Scheduling Implementation Solutions

#### MVP Requirements

-  Run a series of arbitrary python functions
-  Execute immediately, a serial synchronous process
-  Extend to execute at an explicit time as defined by a cron string

#### Technology Solutions

##### Celery
Celery is a distributed task queue. Scheduling and orchestration are best handled using
a DB backed Scheduler or a framework.

A Celery implementation is at the core of all discussed frameworks,
making it a useful candidate for an MVP implementation.

###### Celery Worker
- Worker handles Tasks from the Celery application

###### Celery Beat 
- Built in scheduler, with configuration entries loaded after app configuration
- https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#entries
- Not the best solution for cron jobs created by an API call, since it can only be loaded on configuration.connect
- Could be used to sync from some Alloy endpoint at a regular interval to pick up items marked as jobs.

##### Apache Airflow - https://github.com/apache/airflow

A framework for managing, scheduling and monitoring workflows.

###### Benefits
- Provides web interface for monitoring, managing and executing workflows.
- Define jobs by DAGs which are executed with runtime parameters.
- Can execute in isolation, with a Celery executor, a Kubernetes executor or CeleryKubernetes executor.
- The Kubernetes support provides a mechanism for isolating and scaling tasks and workers.
- Built in executors to get quick solutions for MVP.
 
###### Challenges
- DAG design is an art, it is key to keep workflow scheduling and task execution in distinct processes.
- Built in executors may not be optimized
  - e.g. in my spike I've seen discussion that the default PythonExecutor should not be used as it holds onto workflow metadata,
  - instead you should a celery executor to actually run that code, isolated from the scheduling.
  - https://airflow.apache.org/docs/apache-airflow/stable/executor/index.html#executor-types
- Deployment requirements need to be understood for the context of MS infra.

##### Director - https://github.com/ovh/celery-director
A framework for managing tasks and building workflows with Celery

###### Benefits
- Provides an API for execution any defined workflow
- Workflows are defined by static YML files
- Includes a webserver for monitoring tasks

###### Celery Flower
- Tool for monitoring Celery clusters
- Leveraged by Director for task level monitoring.

#### Best Practices
- Workflows should execute Tasks in their own processes.

#### Future Proofing
- Next steps will be integrating Alloy as the data source for input.
- Any task scheduler should monitor alloy for Job instantiations.