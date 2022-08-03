from django import template

register = template.Library()


def ReplaceWithSpace(value, arg):
    return value.replace(arg, " ")


register.filter('empty', ReplaceWithSpace)