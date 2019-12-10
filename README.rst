PAM System
====================

Pam system (Patent approximation matches system) is a textual analysis tool for matching legal type entities with its patent portfolio, for pairing entities the Pam system relies on the company name and combines full text search techniques using elasticsearch with some of the most famous approximate string matching algorithms such as Jaro-Winkler, Levensthein and Ratcliff. Moreover, it uses each of these scores for calculating its own pam score in order to select the best candidates and dismiss the wrong ones. Some interesting features are:

- Cleaning system for harmonizing company names (Stripping away organization suffix, removing stop words, using stemming words and synonyms).
- Highly modular so it can be easily extended.
- Use of a configuration language to facilitate the implementation of custom filters on the selector module.
- Opportunistic method since it takes as accurate some low score matches just based on results.
- A command-line interface for parameterizing  the system.
- 100% Foss using GPLv3 License.


Quick start
-------------

To run Pam System you can use `venv <https://pip.pypa.io>`_::

    $ python3 -m venve pam_env
    $ source pam_env/bin/active

Now, you can install all the dependencies using `pip <https://pip.pypa.io>`_ and downloading some required `nltk data <https://www.nltk.org/data.html>`_ ::

    (pam_env)$ pip install -r requeriments.txt
    (pam_env)$ python setup.py install
    (pam_env)$ python -m nltk.downloader all

Finally you can run Pam using the csv file that contains the entity list that you want to match::

    (pam_env)$ python -m pam --csv data/loads/you_company_list_file.csv

Maintainer
-----------

`@gnupablo <https://github.com/gnupablo>`_ (Juan Pablo O)


Contributing
-------------

Pam system happily accepts contributions. Below are some of the things that you can do to contribute:

-  `Fork us`_ and `request a pull`_ to the `develop branch`_.
-  Submit `bug reports or feature requests`_

.. _Fork us: https://github.com/cortext/PAM-System/fork)
.. _request a pull: https://github.com/cortext/PAM-System/pulls
.. _develop branch: https://github.com/cortext/PAM-System/tree/develop
.. _bug reports or feature requests: https://github.com/cortext/PAM-Systeme/issues

Funding
-----------

.. |tideliftlogo| image:: https://www.risis2.eu/wp-content/themes/risis2-theme/images/logo-risis-2.png
   :width: 75
   :alt: Tidelift

.. list-table::
   :widths: 10 100

   * - |tideliftlogo|
     - `The RISIS project`_ aims at creating a distributed research infrastructure to support and advance science and innovation studies. The project is funded by the European Union under Horizon2020 Research and Innovation Programme Grant Agreement n°82409.

.. _The RISIS project: https://www.risis2.eu/

