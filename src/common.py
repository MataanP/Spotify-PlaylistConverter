headers={
 "html_content_header":("Content-Type", "text/html; charset=utf-8"),
 "cookie_header":("Set-Cookie","cookie=")
}

def header_creator(list_of_header_titles,cookie = None):
    header_array = []
    for string in list_of_header_titles:
        if string == "cookie_header":
            (header_start,header_end) = headers["cookie_header"]
            header_end = header_end+cookie
            header_array.append((header_start,header_end))
        else:
            header_array.append(headers[string])
    return header_array
