title: Test Driven Development
post: TDD
date: 2012-11-19
---

### TDD ###

Testing programs is boring and everyone does it. *No one* writes a
perfect program straight away - they all get tested at some point,
even if that testing just consists of running the program.

Your program might work fine, but then inexplicably breaks: Maybe
some formatting changed in your input, maybe you made a supposedly
trivial modification to your program. You have to find the root of
the problem to solve it. It's much quicker to do this if you have a
bunch of automated tests than if you have to crawl through the
traceback from the python output.

Guess what? Writing tests after you've written the program is
boring. Coming up with tests forces you to understand the method to
which they apply - doing this on a load of little methods that you
wrote months ago is a tedious exercise.

A better way is to integrate testing into your development workflow.
If it becomes a core part of how you write programs, you won't even
think about doing it. Writing tests as you go along leads to a
deeper understanding of what you're writing at the point that it is
most relevant.

This is TDD. But there's more to it than testing as you go along;
in TDD, you *write the test before the function*. Then write some
code until the test passes and **STOP** - you can't write any more
code until there is a test for it.

