from django import template
register = template.Library()


@register.inclusion_tag("organization/category_tree_part.html")
def category_tree(cate):
    return {'categories': cate.categories.all()}

