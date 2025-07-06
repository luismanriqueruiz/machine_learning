import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    # env: zanalytics
    import marimo as mo
    import random
    import pandas as pd
    return mo, pd, random


@app.cell
def _():
    n_users = 1000
    return (n_users,)


@app.cell
def _(n_users, random):
    random_numbers = [random.random() for _ in range(n_users)]
    return (random_numbers,)


@app.cell
def _(pd, random_numbers):
    all_users_prob = pd.Series(random_numbers)
    return (all_users_prob,)


@app.cell
def _(mo):
    mo.md(r"""## Loading functions""")
    return


@app.function
def get_buckets(n_choices):
    n_prob = 1/n_choices
    buckets = [0] + [x * n_prob for x in range(1, n_choices + 1)]
    return buckets


@app.cell
def _(mo):
    mo.md(r"""## There are 2 choices""")
    return


@app.cell
def _(all_users_prob, pd):
    pd.qcut(all_users_prob, 2).value_counts()
    return


@app.cell
def _(all_users_prob, pd):
    print(pd.cut(all_users_prob, get_buckets(2)).value_counts(normalize=True).sort_index())
    return


@app.cell
def _(mo):
    mo.md(r"""## There are 3 choices""")
    return


@app.cell
def _(all_users_prob, pd):
    print(pd.cut(all_users_prob, get_buckets(2)).value_counts(normalize=True).sort_index())
    return


@app.cell
def _(mo):
    mo.md(r"""## There are 4 choices""")
    return


@app.cell
def _(all_users_prob, pd):
    print(pd.cut(all_users_prob, get_buckets(4)).value_counts(normalize=True).sort_index())
    return


@app.cell
def _(mo):
    mo.md(r"""## There are 5 choices""")
    return


@app.cell
def _(all_users_prob, pd):
    print(pd.cut(all_users_prob, get_buckets(5)).value_counts(normalize=True).sort_index())
    return


if __name__ == "__main__":
    app.run()
