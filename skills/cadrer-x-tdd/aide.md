# cadrer-x tests — a behaviour, through the entry, one at a time

Loaded by `realiser` (writing tests), `ranger` (the tests of today, before a move) and `examiner` (judging them). Adapted from Matt Pocock's `tdd`
skill (MIT, github.com/mattpocock/skills).

## What a good test is

A test checks a behaviour through the module's public entry, never how the code does it. The code can
change entirely; the test should not. A good test reads like the spec: « une facture payée n'est plus due »
says what the product does.

```python
# Good: what a customer gets, through the entry
def test_a_paid_invoice_is_no_longer_due(self):
    billing.api.pay(invoice_id=7, amount=120)
    self.assertEqual(billing.api.amount_due(7), 0)

# Bad: how the code does it
def test_pay_updates_the_row(self):
    billing.api.pay(invoice_id=7, amount=120)
    self.assertEqual(db.execute("SELECT paid FROM invoices WHERE id = 7").fetchone()[0], 1)
```

## Where tests go

At the entry of the module the task builds (`{docs}/architecture.md` → **Modules**: its `api.<ext>`, its
route, its page). `decouper` already chose them: each box of the task is a test at that entry, named
like the box, with the spec's own values. No test against a private function. The file goes where
**Modules** puts that module's tests; with no line for them, where the framework puts its tests, else
in `tests/modules/<module>/`.

## Three tests to avoid

- **Stuck to the code**: mocks the project's own modules, tests a private function, or checks through
  a side door (a query on the table instead of the entry). The sign: it breaks on a refactor that kept
  the behaviour. To prove « nothing stored », read it back through the entry. If the module has no
  reader, a direct read is allowed; say so once.
- **Tautological**: the expected value is computed the way the code computes it
  (`assertEqual(total(items), sum(i.price for i in items))`), so it can never disagree. The expected
  value is a literal from the spec or a worked example: `assertEqual(total(items), 15)`.
- **All written first**: every test, then all the code. Those tests check an imagined shape.

## Mocks

Only at the edges of the system: an outside service (payment, email), time, randomness, the file
system outside a temp folder: tests point `HOME`, the XDG folders and any path the app writes data or
config to at temp folders. Never the project's own modules. The project's own database in tests (the
test database or SQLite in memory) beats a mock of it. An outside service is easiest to mock when the
code receives it (`charge(order, client)`) instead of building it.

## The loop

1. One test, for one behaviour. Run it: it fails **on its assertion**, because the behaviour is
   missing. An import error or a missing function is not red yet: add the empty function, run again.
2. The least code that passes it. Run it. No code for a test not written yet.
3. The next behaviour.
4. All green: tidy if it helps, tests untouched, run them again.

**Would it fail?** Before moving on, name the one-line change that would break the behaviour (`>`
for `>=`, the transaction removed, the owner check skipped). If the test does not catch it, fix the
test.

## Red flags

| Thought | Instead |
|---|---|
| "I'll check the row in the table." | Through the entry; a direct read only when the module has none. |
| "I'll mock `members.api`." | It is ours: use the real one. |
| "Expected: the same formula as the code." | A literal from the spec. |
| "All the tests now, the code after." | One test, its code, the next. |
| "It fails with ImportError: red." | Red is the assertion failing. |
| "A test wrote a real file in the home folder: harmless." | A failure: isolate the tests now. |
