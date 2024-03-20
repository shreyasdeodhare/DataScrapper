import re
import json
import logging

import requests
from lxml import html

__all__ = ['gargl']

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


at_pattern = re.compile(r'[^@]*(@\w+@)[^@]*', re.IGNORECASE)

def _replace_variables(template_dict, values):
    if not template_dict:
        return {}

    k_v = {}
    k_v_format = {}
    k_v_value = {}

    # name & value -> name: value
    for item in template_dict:
        k_v[item['name']] = item['value']

    # @@ -> {}
    for key in k_v:
        matches = at_pattern.findall(k_v[key])
        tpl_vars = {v: '{{{}}}'.format(v.strip('@')) for v in matches}

        tmp = k_v[key]
        for v_orig, v_new in tpl_vars.items():
            tmp = tmp.replace(v_orig, v_new)

        k_v_format[key] = tmp

    # {} -> <value>
    for key, value in k_v_format.items():
        k_v_value[key] = value.format(**values)

    return k_v_value



class gargl:
   
   
    def __init__(self, gtf):
        self._gtf = gtf
        self._conf = None

        with open(self._gtf, 'r') as conf_file:
            self._conf = json.load(conf_file)


    def __getattr__(self, name):
        log.debug('prepping function {}'.format(name))

        try:
            f_desc = [f for f in self._conf['functions'] if f['functionName'] == name][0]
        except IndexError:
            raise AttributeError('function {} is not defined in GTF'.format(name))

        # prepare method
        def method(var_dict):
            log.info('calling function {}'.format(name))

            response = None
            url = f_desc['request']['url']
            qs = _replace_variables(f_desc['request'].get('queryString', {}),
                var_dict)
            data = _replace_variables(f_desc['request'].get('postData', {}),
                var_dict)
            headers = _replace_variables(f_desc['request'].get('headers', {}),
                var_dict)

            if f_desc['request']['method'] == 'GET':
                response = requests.get(url, headers=headers,
                    params=qs, data=data)
            else:
                response = requests.post(url, headers=headers,
                    params=qs, data=data)

            # throw an exception if necessary
            response.raise_for_status()
            return self._parse_response(f_desc.get('response', {}), response.text)

        # "cache it"
        if name not in dir(self):
            self.__setattr__(name, method)

        return method

   
    def _parse_response(self, response_rules, response):
        if not len(response_rules.get('fields', {})):
            return response

        res = []
        a=[]

        tree = html.fromstring(response)
        root = tree.xpath('/html/body')[0]


        for item in response_rules['fields']:
            # compatibility with GTFv1.0
            if item.get('cssSelector'):
                res.append({item['name']: root.cssselect(item['cssSelector'])})
            # extension
            if item.get('xpath'):
                res.append({item['name']: root.xpath(item['xpath'])})

        a=res[0]
        b=a.get('searchResultTitles')
        l = len(b)
        print("The search results for python:")
        for i in range(0,l):
            print(b[i].text_content())
        c=res[1]
        d=c.get('suggestions')
        la = len(d)
        print("#####################################")
        print("The suggestions for python:")
        for j in range(0,la):

            print(d[j].text_content())
        return res


if __name__ == '__main__':
    ARG_GTF = 'sample/yahoosearch.gtf'
    g = gargl(ARG_GTF)
    g.Search({'query': 'python'})
    g.Search({'query': 'pygargl'})