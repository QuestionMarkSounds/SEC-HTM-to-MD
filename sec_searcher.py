from edgar import *



def sec_search(self, ticker, name, email):
    set_identity("{} {}".format(name, email))

    try:
        filings = Company(ticker).get_filings(form="10-K").latest(1)

        # markdown_text = filings.markdown()
        # if __debug__:
        #     print(markdown_text[-50:-1])
        # with open('{}.md'.format(ticker), 'w', encoding="utf-8") as f:
        #     f.write(markdown_text)
        return filings
    except AttributeError:
        raise Exception("Invalid ticker - {}".format(ticker))


# sec_search("RBLX", "Marks Docenko", "marksdocenko@outlook.com")