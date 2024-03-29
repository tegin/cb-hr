======================
Hr Holidays Extendable
======================

.. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-tegin%2Fcb--hr-lightgray.png?logo=github
    :target: https://github.com/tegin/cb-hr/tree/13.0/hr_holidays_extendable
    :alt: tegin/cb-hr

|badge1| |badge2| |badge3| 

Allows a certain type of holidays to be extended.

A much easier solution would be to just create a new leave, but this module can
be interesting if you want to keep the chatter and everything in one record.
It is also more realistic, since at the end, you are having just one leave,
not two or three.

**Table of contents**

.. contents::
   :local:

Usage
=====

The first thing to do is select which holiday types can be extended.
To do so go the configuration menu in the Leaves app, and select the check
box *Extendable*.

Holidays can only be extended by the Human Resources Manager and when they are
in *Approved* state. A new button will appear automatically when all these
conditions are met.

Clicking on it will open a small wizard that will allow you to select the new
end date for the holiday. After clicking *Extend* the original holiday will be
updated with the new values.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/tegin/cb-hr/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/tegin/cb-hr/issues/new?body=module:%20hr_holidays_extendable%0Aversion:%2013.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Creu Blanca

Contributors
~~~~~~~~~~~~

* Jaime Arroyo <jaime.arroyo@creublanca.es>

Maintainers
~~~~~~~~~~~

This module is part of the `tegin/cb-hr <https://github.com/tegin/cb-hr/tree/13.0/hr_holidays_extendable>`_ project on GitHub.

You are welcome to contribute.
