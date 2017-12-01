from naam import bind_args


@bind_args
def hello(first_name, last_name):
    print('Hello world! My name is {} {}.'.format(first_name, last_name))


hello()
