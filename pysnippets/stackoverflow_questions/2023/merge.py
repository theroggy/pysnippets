import pandas as pd


def main():
    df1 = pd.DataFrame({"SA4_CODE21": ["foo"]})
    df2 = pd.DataFrame({"SA4_CODE21": ["foo", "bar", "foo", "bar"], "c": [1, 2, 3, 4]})

    result = df2.merge(df1, on="SA4_CODE21", how="inner")
    print(result)

    result = df2.join(df1.set_index("SA4_CODE21"), on="SA4_CODE21", how="inner")
    print(result)


if __name__ == "__main__":
    main()
