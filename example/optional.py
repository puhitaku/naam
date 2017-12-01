from naam import bind_args


@bind_args
def hello(first_name, last_name=None):
    msg = 'Hello world! My name is %s.'
    if last_name is None:
        print(msg % first_name)
    else:
        print(msg % '{} {}'.format(first_name, last_name))


hello()
g