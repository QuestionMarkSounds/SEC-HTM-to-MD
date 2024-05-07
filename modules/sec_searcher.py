from edgar.core import set_identity, Company



def sec_search(ticker, name, email):
    set_identity("{} {}".format(name, email))

    try:
        filings = Company(ticker).get_filings(form="10-K").latest(1)

        return filings
    except AttributeError:
        raise Exception("Invalid ticker - {}".format(ticker))


# sec_search("RBLX", "Marks Docenko", "marksdocenko@outlook.com")