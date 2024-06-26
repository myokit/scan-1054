#!/usr/bin/env python3
#
# This script scans Myokit models for equations involving a 'PrefixPlus', that
# is a unary plus operation, which are affected by the bug described at
# https://github.com/myokit/myokit/pull/1055
#
# To use:
#
#    python scan.py my-model.mmt
#
# or
#
#    python scan.py my-directory-with-models
#
import os
import myokit


def has_issue(expression):
    """ Scan an expression for potential issues. """
    if isinstance(expression, myokit.PrefixPlus):
        if isinstance(expression[0], myokit.InfixExpression):
            return True
    if isinstance(expression, myokit.Power):
        if isinstance(expression[0], myokit.Power):
            return True
    for op in expression:
        if has_issue(op):
            return True
    return False


def scan_var_owner(owner, issues):
    """ Scan a component or variable. """
    for var in owner:
        if has_issue(var.rhs()):
            issues.append((f'Equation', var, var.rhs()))
        if var.is_state() and has_issue(var.initial_value()):
            issues.append((f'Initial value', var, var.initial_value()))
        scan_var_owner(var, issues)


def scan_model(filename):
    print(f'Checking model {filename}...', end='')
    try:
        model = myokit.load_model(filename)
    except myokit.SectionNotFoundError:
        print(' [no model section]')
    except myokit.MyokitError as e:
        print(' [error when reading model]')
        print(str(e))
    except IOError as e:
        print(' [i/o error when reading model]')
        print(str(e))
    else:
        issues = []
        for component in model:
            scan_var_owner(component, issues)
        if issues:
            print(' [potential issue detected]')
            for where, var, expression in issues:
                print(f'{where} for {var.qname()}: {expression.code()}')
        else:
            print(' [ok]')


def scan_dir(path):
    for leaf in os.listdir(path):
        full = os.path.join(path, leaf)
        if leaf in ('.', '..'):
            continue
        if os.path.isdir(full):
            scan_dir(full)
        elif leaf.endswith('.mmt'):
            scan_model(full)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Usage: ./scan.py path')
        sys.exit(1)
    path = sys.argv[1]

    if os.path.isdir(path):
        scan_dir(path)
    else:
        scan_model(path)

