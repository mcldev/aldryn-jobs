############
Installation
############


*******************
Installing packages
*******************

We'll assume you have a django CMS (version 3.x) project up and running.

If you need to set up a new django CMS project, follow the instructions in the `django CMS tutorial
<http://docs.django-cms.org/en/develop/introduction/install.html>`_.

Then run either::

    pip install aldryn-jobs

or to install from the latest source tree::

    pip install -e git+https://github.com/aldryn/aldryn-jobs.git#egg=aldryn-jobs


***********
settings.py
***********

In your project's ``settings.py`` make sure you have all of::

    'absolute',
    'aldryn_common',
    'aldryn_boilerplates',
    'aldryn_apphooks_config',
    'aldryn_categories',
    'aldryn_jobs',
    'aldryn_translation_tools',
    'adminsortable2',
    'bootstrap3',
    'emailit',
    'parler',
    'sortedm2m',
    'standard_form',

listed in ``INSTALLED_APPS``, *after* ``'cms'``.


Aldryn Boilerplates
===================

This application uses (and will install) `Aldryn Boilerplates <https://github.com/aldryn/aldryn-boilerplates>`_,
which requires some basic configuration to get you started.

Edit your settings so that they conform to::

    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        # important - place immediately before AppDirectoriesFinder
        'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'OPTIONS': {
                'context_processors': [
                    ...
                    'aldryn_boilerplates.context_processors.boilerplate',
                    ...
                ],
                'loaders': [
                    ...
                    # important! place right before django.template.loaders.app_directories.Loader
                    'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
                    'django.template.loaders.app_directories.Loader',
                    ...
                ],
            },
        },
    ]

Now set the name of the boilerplate you'll use in your project::

    ALDRYN_BOILERPLATE_NAME = 'bootstrap3'

.. note::
   Note that Aldryn Jobs doesn't use the the traditional Django ``/templates`` and ``/static
   directories``. Instead, it employs `Aldryn Boilerplates
   <https://github.com/aldryn/aldryn-boilerplates>`_, which makes it possible to to support
   multiple different frontend schemes ('Boilerplates')and switch between them without the need for
   project-by-project file overwriting.

   Aldryn Jobs's templates and staticfiles will be found in named directories in the
   ``/boilerplates`` directory.


****************************
Prepare the database and run
****************************

Now run ``python manage.py migrate`` to prepare the database for the new
application, then ``python manage.py runserver``.


****************
For Aldryn users
****************

On the Aldryn platform, the Addon is available from the `Marketplace
<http://www.aldryn.com/en/marketplace>`_.

You can also `install Aldryn Jobs into any existing Aldryn project
<https://control.aldryn.com/control/?select_project_for_addon=aldryn-jobs>`_.

At installation time on Aldryn, you will be asked to provide a ``Default send to`` value (required),
an email address to which job applications will be sent. You can change this later if required.

You will also need to install and configure **Aldryn Email Settings**, also via *Manage Addons* in
the Control Panel.
