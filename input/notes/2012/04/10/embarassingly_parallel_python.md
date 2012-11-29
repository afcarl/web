title: Embarassing problems in python
post: embarassingly parallel python
date: 2012-04-10
---

I have an embarassing problem... an [embarassingly parallel problem][epp]!
Look at all of this squandered potential!

![problem](http://homepages.see.leeds.ac.uk/~eeaol/images/embarassing-problem.png)

[epp]: http://en.wikipedia.org/wiki/Embarrassingly_parallel

I have a load of lab data sorted into individual runs. Each run has its own
input files (raw data) and it's own output files. The processing of any one run
does not depend on the outputs or inputs or process of any other run and
basically consists of some cpu-intensive image processing, making this a
situation ripe for concurrent processing.

Of course, python has a [multiprocessing] module that makes this easy to
implement. Let's say that the process that chomps through an individual run
is called `process(run)` and I can get a list of all the runs by 
`runs = get_runs()`. The simplest way to get this to multiprocess is to
create a pool of workers, with each worker working on a separate run (total
number is around 60).

    #!python
    from multiprocessing import Pool
    
    def pool(proc, runs):
        p = Pool(processes=len(runs))
        p.map(proc, runs)
        p.close()
        p.join()

    if __name__ == '__main__':
        runs = get_runs()
        pool(process, runs)

Edit 12/04/2012: putting `p.close()` on the end is quite important, as it
closes the processes after they have finished. 

Now, htop looks like this:

![solved](http://homepages.see.leeds.ac.uk/~eeaol/images/embarassing-solution.png)

Problem solved!   

--------

### Further reading ###

Similar situation on [stackoverflow][]. Here's a [similar post][ptone] by
someone doing parallel image processing, with a discussion about
hyperthreading. The [Python documentation][multiprocessing].   

[multiprocessing]: http://docs.python.org/dev/library/multiprocessing.html
[stackoverflow]: http://stackoverflow.com/questions/2359253/solving-embarassingly-parallel-problems-using-python-multiprocessing/
[ptone]: http://ptone.com/dablog/2010/01/pythonmultiprocessinghyperthreading-and-image-resizing/

--------

#### Postscript (12/04/2012): #####

Note: there are 24 processors in the above screenshots, but they are only
logical processors. There are actually two physical processors, each with six
cores and hyperthreading enabled.

In my script I've told Pool to make as many processes as there are runs.

    pool = Pool(processes=len(runs))

Alternatively I could leave this argument blank, then Pool will create as many
processes as the number returned by `cpu_count()` (24 in this case). Or I can
choose a smaller number if I don't want to hog the whole system.

If I do choose a smaller number, another argument is maxtasksperchild, which
makes sure worker processes are closed down after a certain number of tasks.
From the [documentation][]:

[documentation]: http://docs.python.org/library/multiprocessing.html#module-multiprocessing.pool

> New in version 2.7: maxtasksperchild is the number of tasks a worker process
> can complete before it will exit and be replaced with a fresh worker process,
> to enable unused resources to be freed. The default maxtasksperchild is None,
> which means worker processes will live as long as the pool.
> 
> Note Worker processes within a Pool typically live for the complete duration of
> the Pool’s work queue. A frequent pattern found in other systems (such as
> Apache, mod_wsgi, etc) to free resources held by workers is to allow a worker
> within a pool to complete only a set amount of work before being exiting, being
> cleaned up and a new process spawned to replace the old one. The
> maxtasksperchild argument to the Pool exposes this ability to the end user.
