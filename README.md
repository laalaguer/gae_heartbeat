### GAE heartbeat module
Google App Engine (GAE) `heartbeat` api for various purpose

### GAE queue-related stuff
Google App Engine (GAE) has produced a lot of good features like:


1. `pull queue`, where you can fetch tasks and execute it outside app engine.
2. `push queue`, where you create task and execute it inside app engine.
3. `cron job`, where you can schedule tasks that execute periodically.


However GAE also has limits:


1. `pull queue` is waiting for external worker to pull the queue.
2. GAE has a `28 instance` hours limit each day, which means you cannot pull frequently.
3. `push queue` has a timely deadline on each task execution, 60s.  But my task may run for up to 7 days till final success.
4. `cron job` has the same limit in number 2, which means we cannot pull frequently. Plus, each task is limit to 60s.

### A Real Problem
I design this `heartbeat` module to solve this problem:


1. Server publish a `heartbeat` info, which contains `name`, `is_on`, `come_back`.
2. `is_on` indicates that if the worker shall wake up or not.
3. `come_back` indicates the minutes interval worker shall come back to check the heartbeat.
4. `name` is the name of the `heartbeat`.

How this will work in real life:


1. I have a `heartbeat` which `name` is cat.
2. At 8:00 I adjust it to `is_on=True`, `come_back=5`. So the worker come back every 5mins and do the job.
3. At 19:00 I adjust it to `is_on=False`, `come_back=20`, so the worker is going idle and come back every 10 mins.
4. At 7:30 I adjust it again to `is_on=False`, `come_back=5`, so the worker is idle but come back more frequently.
5. You can adjust the above paremeters through web page api or GAE cron jobs.

### How the resources are saved:
1. If we combine `heartbeat` with any pull queue in GAE, then the worker can reduce the frequency to query the pull queue.
2. As we only keep a record of `heartbeat` in NDB database, we delete the historical heartbeats, so the query time of `heartbeat` is O(1).
3. You have the possibilities to adjust the worker frequency on the GAE side, not on your worker side.
4. GAE frontend instance time is reduced by up to 50%-60%.

### How to use this module
1. Include the heartbeat module into your python project.
2. Adjust your frequency by cron jobs and through web apis.
3. Take a look at `app.yaml` and `main.py` , these are examples.
4. Dont forget to change your app id inside `app.yaml`
