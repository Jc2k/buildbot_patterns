=================
Buildbot patterns
=================

** THIS IS NOT IMPLEMENTED YET **

Getting started with buildbot can be daunting. As I often tell people, its a
framework not an end user point + click tool. buildbot_patterns tries to
encapsulate some common configurations to ease you into running a buildbot.

Thoughts
========

 * Make the easy stuff easy. The point of this effort is that newcomers find
   buildbot daunting enough that they stop before building their first thing.

 * Leave the hard stuff alone. If we expose all of buildbots power through a
   "simple" interface it will cease to be simple.


Simple builds
=============

Setting up an Git project could be as simple as::

    build_on_commit(c,
        name = "buildbot",
        repository = "git://github.com/buildbot/buildbot",
        steps = [
            "virtualenv --no-site-packages .",
            "bin/python setup.py develop",
            "bin/pip install mock",
            "bin/trial buildbot",
            ]
        slaves = ['windows-1', 'windows-2']
        )

What are you going to get? A single builder that runs on one of 2 slaves
whenever anyone commits. The code will be checked out and 4 ShellCommands will
run. If you want builds to start quicker, then in 0.8.7 the
``/change_hooks/pollers`` mechanism can be used.

Warnings and fails will make the build warn and fail.

You haven't had to think about schedulers, change sources, filters, builders or
factories. You've just had to give up some code and a list of commands.

Using more advanced BuildStep objects
=====================================

Just mix in actual buildbot steps::

    build_on_commit(c,
        name = "buildbot",
        repository = "git://github.com/buildbot/buildbot",
        steps = [
            "virtualenv --no-site-packages .",
            "bin/python setup.py develop",
            "bin/pip install mock",
            "bin/trial buildbot",
            DirectoryUpload(.....),
            ]
        slaves = ['windows-1', 'windows-2']
        )


Schedulers
==========

The 2 common use cases are "on commit" and "nightly"::

    build_on_commit(c,
        name = "buildbot",
        repository = "git://github.com/buildbot/buildbot",
        steps = [
            "virtualenv --no-site-packages .",
            "bin/python setup.py develop",
            "bin/pip install mock",
            "bin/trial buildbot",
            ]
        slaves = ['windows-1', 'windows-2']
        )

    build_nightly(c,
        name = "buildbot",
        hour = "1",
        minute = "23",
        repository = "git://github.com/buildbot/buildbot",
        steps = [
            "virtualenv --no-site-packages .",
            "bin/python setup.py develop",
            "bin/pip install mock",
            "bin/trial buildbot",
            ]
        slaves = ['windows-1', 'windows-2']
        )


Multiple codebases
==================

::

    build_on_commit(c,
        name = "buildbot",
        repositories = {
            "": "git://github.com/buildbot/buildbot",
            "src/dep1": "git://github.com/buildbot/dep1",
            "src/dep2": "git://github.com/buildbot/dep2",
            },
        steps = [
            "virtualenv --no-site-packages .",
            "bin/python setup.py develop",
            "bin/pip install mock",
            "bin/trial buildbot",
            ]
        slaves = ['windows-1', 'windows-2']
        )


Using properties
================

We should just wrap the generated commands in WithProperties by default::

    build_on_commit(c,
        name = "buildbot",
        repositories = {
            "": "git://github.com/buildbot/buildbot",
            "src/dep1": "git://github.com/buildbot/dep1",
            "src/dep2": "git://github.com/buildbot/dep2",
            },
        steps = [
            "echo %(revision)s",
            "virtualenv --no-site-packages .",
            "bin/python setup.py develop",
            "bin/pip install mock",
            "bin/trial buildbot",
            ]
        slaves = ['windows-1', 'windows-2']
        )


Variations of same build
========================

Uses the underlying API of the config wrapper::

    template = BuildTemplate(
        repositories = {
            "": "git://github.com/buildbot/buildbot",
            "src/dep1": "git://github.com/buildbot/dep1",
            "src/dep2": "git://github.com/buildbot/dep2",
            },
        steps = [
            "echo %(revision)s",
            "virtualenv --no-site-packages .",
            "bin/python setup.py develop",
            "bin/pip install mock",
            "bin/pip install sqlalchemy-migrate == %(sqlalchemy_migrate)s",
            "bin/trial buildbot",
            ]
        )

    template.on_commit(c,
        name = "windows-sql-0.7",
        properties = {
            "sqlalchemy_migrate": "0.7",
             },
        slaves = ['windows-1', 'windows-2'],
        )

    template.on_commit(c,
        name = "osx-sql-0.7",
        properties = {
            "sqlalchemy_migrate": "0.7",
             },
        slaves = ['osx-1'],
        )


More thoughts
=============

VCS guessing
------------

For my own things, looking for things like this would be sufficient. For
others, a ``repository_type`` would be supported::

    http[s]://svn.*/ -> SVN
    http[s]://*/svn/* -> SVN
    svn*://* -> SVN

    git*:// -> GIT
    http[s]://git.*/ -> GIT
    http[s]://github.com/ -> GIT
    http[s]://*/git/* - > GIT
    http[s]://*/..../*.git -> GIT

    hg*:// -> Mercurial
    http[s]://hg.*/ -> Mercurial
    http[s]://*/hg/* -> Mercurial

Be more of a DSL
----------------

The BuildTemplate thing can probably be a lot more expressive. I'm sort of
imagining something like the ORM in Django where you can build an expression by
chaining multiple things together - but each chain is something that could be
reused multiple times::

    b = BasicBuild(steps=[....]).what(repository = "....", username="...")

    when = [b.when("commit", ...), b.when("nightly", hour=1)]
    where = ["windows", "osx"]

    for w1 in when:
        for w2 in where:
            w1.configure(c, slaves=[w2])

Here ``configure`` is the thing that pulls all the declaratively defined
information together and emits the various standard Buildbot objects.


Support loading YAML
--------------------

The first example might look like::

    builds:
      - name: buildbot
        repository: git://github.com/buildbot/buildbot
        steps:
          - virtualenv --no-site-packages .
          - bin/python setup.py develop
          - bin/pip install mock
          - bin/trial buildbot
        slaves:
          - windows-1
          - windows-2

Support export
--------------

As this is meant to be a gateway to writing real configs, the output of this
thing should be easy to turn into a "real" buildbot config.


