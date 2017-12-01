import inspect
import sys
from collections import defaultdict, namedtuple


OptionalArg = namedtuple('OptionalArg', ['full', 'abbrev', 'default'])


def _parse(args):
    """Parse passed arguments from shell."""

    ordered = []
    opt_full = dict()
    opt_abbrev = dict()

    args = args + ['']  # Avoid out of range
    i = 0

    while i < len(args) - 1:
        arg = args[i]
        arg_next = args[i+1]
        if arg.startswith('--'):
            if arg_next.startswith('-'):
                raise ValueError('{} lacks value'.format(arg))
            else:
                opt_full[arg[2:]] = arg_next
                i += 2
        elif arg.startswith('-'):
            if arg_next.startswith('-'):
                raise ValueError('{} lacks value'.format(arg))
            else:
                opt_abbrev[arg[1:]] = arg_next
                i += 2
        else:
            ordered.append(arg)
            i += 1
    
    return ordered, opt_full, opt_abbrev


def _construct_ordered(params):
    args = [key for key, arg in params.items() if arg.default == inspect._empty]
    return args


def _construct_optional(params):
    """Construct optional args' key and abbreviated key from signature."""

    args = []
    filtered = {key: arg.default for key, arg in params.items() if arg.default != inspect._empty}
    for key, default in filtered.items():
        arg = OptionalArg(full=key, abbrev=key[0].lower(), default=default)
        args.append(arg)

    args_full, args_abbrev = dict(), dict()

    # Resolve conflicts
    known_count = defaultdict(int)
    for arg in args:
        args_full[arg.full] = arg

        if known_count[arg.abbrev] == 0:
            args_abbrev[arg.abbrev] = arg
        elif known_count[arg.abbrev] == 1:
            new_abbrev = arg.abbrev.upper()
            args_full[arg.full] = OptionalArg(full=arg.full, abbrev=new_abbrev, default=arg.default)
            args_abbrev[new_abbrev] = args_full[arg.full]
        else:
            new_abbrev = arg.abbrev.upper() + str(known_count[arg.abbrev])
            args_full[arg.full] = OptionalArg(full=arg.full, abbrev=new_abbrev, default=arg.default)
            args_abbrev[new_abbrev] = args_full[arg.full]
        known_count[arg.abbrev] += 1
    return args_full, args_abbrev


def _resolve(args, signature):
    ordered, opt_parsed_full, opt_parsed_abbrev = _parse(args[1:])

    ordered_def = _construct_ordered(signature.parameters)
    if len(ordered) != len(ordered_def):
        raise Exception

    opt_parsed = dict()
    opt_parsed.update(opt_parsed_full)
    opt_parsed.update(opt_parsed_abbrev)

    opt_def_full, opt_def_abbrev = _construct_optional(signature.parameters)
    optional = {o.full: o.default for o in opt_def_full.values()}
    opt_def = dict()
    opt_def.update(opt_def_full)
    opt_def.update(opt_def_abbrev)

    for key, val in opt_parsed.items():
        if key not in opt_def:
            raise Exception
        d = opt_def[key]
        optional[d.full] = val

    return ordered, optional


def _usage_oneline(signature):
    ordered = _construct_ordered(signature.parameters)
    full, _ = _construct_optional(signature.parameters)

    ordered_str = ' '.join(name.upper() for name in ordered)
    optional_str = ' '.join('[-{} {} | --{} {}]'.format(
        opt.abbrev, opt.full.upper(), opt.full, opt.full.upper()) for opt in full.values())

    return '{} {}'.format(optional_str, ordered_str)


def bind_args(fn):
    def inner():
        sig = inspect.signature(fn)
        try:
            ordered, optional = _resolve(sys.argv, sig)
        except Exception:
            print('Usage:', sys.argv[0], _usage_oneline(sig))
            return
        fn(*ordered, **optional)

    return inner
