def get_gene_symbol(gene_ids: str) -> str:
    """The function that make an API request to my mygene.info, requesting for symbol using gene ID

    Args:
        gene_id (str): the id of the gene

    Returns:
        (str) the symbol of the gene
    """
    headers = {"content-type": "application/x-www-form-urlencoded"}
    params = f"ids={gene_ids}&fields=symbol"

    try:
        res = requests.post("http://mygene.info/v3/gene", data=params, headers=headers)
        res.raise_for_status()
    except requests.RequestException as e:
        return {}

    return json.loads(res.content.decode("utf-8"))


def pairUp_seq_info(value_dict: dict) -> list:
    """Pair up all the elements in each value of the dictionary

    Args:
        value_dict (dict): values that need to be paired up

    Returns:
        list[dict]: A list of dictionaries where each dict contains a pairing
        of keys with corresponding elements from the value lists.
    >>> pairUp_seq_info({"a": "1, 2", "b": "3, 4"})
    [{'a': '1', 'b': '3'}, {'a': '2', 'b': '4'}]
    >>> pairUp_seq_info({"a": '1'})
    [{'a': '1'}]
    """
    keys = list(value_dict.keys())
    values = [str_to_list(value) for value in value_dict.values()]

    # when there is mismatch gene and its symbol, we will get gene symbol form my.gene API
    if not all(len(v) == len(next(iter(values))) for v in values):
        gene_ids = ", ".join(
            [
                gene_id
                for gene_id in str_to_list(value_dict["geneid"])
                if gene_id.casefold() != "na" and gene_id != ""
            ]
        )
        symbols = get_gene_symbol(gene_ids)

        return [
            {"geneid": gene_info["_id"], "genesymbol": gene_info["symbol"]}
            for gene_info in symbols
        ]

    return [dict(zip(keys, combination)) for combination in zip(*values)]
