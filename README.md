# workable
This is an unofficial python wrapper for the Workable API. You can download a list of jobs, candidates and detailed candidate information for one or all candidates.

Usage:

```python
from Workable import Workable

workable = Workable(account='youraccount',apikey='yourapikey')
```

## Available functions

Returns a list of candidates for a given job, by Job Shortcode
```python
from Workable import Workable

workable = Workable(account='youraccount',apikey='yourapikey')

candidate_list = workable.candidate_list(job='Job Shortcode')
```

Get detail information for a given candidate for a job, identified by candidate id and job shortcode
```python
from Workable import Workable

workable = Workable(account='youraccount',apikey='yourapikey')

candidate = workable.single_candidate_detail(candidate_id='candidate id',job='Job Shortcode')
```

Return the list of all jobs in your account, or jobs with a certain publication state

```python
from Workable import Workable

workable = Workable(account='youraccount',apikey='yourapikey')

all_jobs = workable.job_list()

# Job States can be draft, published, archived, closed
published_jobs = workable.job_list(state='published')
```

Return detail information about a single job

```python
from Workable import Workable

workable = Workable(account='youraccount',apikey='yourapikey')

job = workable.job_detail(job='job shortcode')
```