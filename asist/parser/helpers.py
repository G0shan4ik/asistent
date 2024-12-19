parsing_list = {
    'dollar_ruble_by': 'https://myfin.by/ajaxnew/currency-best-chart?currency_id=1&city_id=5&days=1',
    'dollar_ruble_ru': 'https://myfin.by/ajaxnew/currency-best-chart?currency_id=10&city_id=5&days=1',
    'rouble_ru_by': 'https://myfin.by/ajaxnew/currency-best-chart?currency_id=5&city_id=5&days=1',
    'euro_ru_by': 'https://bankibel.by/kursy-valut/evro/brest'
}

def merge_dictionaries(list_of_dicts: list[dict]) -> dict:
  result_dict = {}
  for d in list_of_dicts:
      for key, value in d.items():
          result_dict[key] = value
  return result_dict