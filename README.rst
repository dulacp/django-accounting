django-accounting
=================

    In the beginning God created man, and the costs followed afterwards.

|Build Status| |Coverage Status|

Check the associated project
`Accountant <https://github.com/dulaccc/Accountant>`__, a concrete
integration of the *django-accounting* application that you can deploy
with one click to Heroku.

Requirements
------------

-  Python 3.x
-  Django 1.7+
-  `dj-static <https://github.com/kennethreitz/dj-static>`__

Features supported
------------------

*with inspiration from already existing very good services (Xero,
Freshbooks, etc)*

    Those crossed are not yet supported

Books
~~~~~

-  **Estimating** generate estimates that can lead to an invoice or not
-  **Invoicing** generate invoices
-  **Billing** share the maximum of logic with the invoicing system
-  **Payments** to track partial/complete payments of invoices and bills
-  **ExpenseClaim** for employees of organizations that used their
   personnal accounts
-  **Dashboard / Current balance** displayed the current balance
-  **Dashboard / Overdued invoices & bills** to track what's late

Clients
~~~~~~~

-  **Creation/Update**
-  [STRIKEOUT:**Deletion** inform the user of the cascade deletion of
   invoices and bills]
-  **Professional address** specify the address on the client model
-  **Linked to organization** to implicitly create the bill when
   cross-invoicing between organizations

Reports
~~~~~~~

-  **Profit and Loss** to know how much you've collected, and how much
   you've spent
-  **Tax Report** to know how much you need to keep for taxes
   declarations
-  **Payroll Report** to know how much you need to keep for payroll
   taxes
-  **Invoice details Report** to understand the calculations that lead
   to the tax report and the payroll report
-  [STRIKEOUT:**Expense claims Report** to compute what the company owes
   to whom quickly]

Contact
-------

| `Pierre Dulac <http://github.com/dulaccc>`__
| [@dulaccc](https://twitter.com/dulaccc)

License
-------

Accounting is available under the MIT license. See the LICENSE file for
more info.

.. |Build Status| image:: https://travis-ci.org/dulaccc/django-accounting.svg
   :target: https://travis-ci.org/dulaccc/django-accounting
.. |Coverage Status| image:: https://coveralls.io/repos/dulaccc/django-accounting/badge.svg
   :target: https://coveralls.io/r/dulaccc/django-accounting
