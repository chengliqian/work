from urllib.parse import urlunsplit, urlsplit, urlencode, parse_qs

def set_query_parameter(url, param_name, param_value):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)
    print("----",type(query_params),query_params)

    query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))

url = 'http://qa.business.ka.163.com/omp/priceVersion/search'
param_name = 'token'
param_value = '84a6cb9448770959656f7f6ba3dbc475'

print(set_query_parameter(url, param_name, param_value))