
def get_children(qs_child):
    res = []
    for comment in qs_child:
        c = {
            'id': comment.id,
            'text': comment.body,
            'timestamp': comment.date.strftime('%Y-%m-%d %H:%m'),
            'author': comment.author,
            'is_child': comment.is_child,
            'parent_id': comment.get_parent,
        }
        if comment.comment_parent.exists():
            c['children'] = get_children(comment.comment_parent.all())
        res.append(c)
    return res


def create_comments_tree(qs):
    res = []
    for comment in qs:
        c = {
            'id': comment.id,
            'text': comment.body,
            # 'timestamp': comment.date.strftime('%Y-%m-%d %H:%m'),
            'author': comment.author,
            'is_child': comment.is_child,
            'parent_id': comment.get_parent,
        }
        if comment.comment_parent:
            c['children'] = get_children(comment.comment_parent.all())
        if not comment.is_child:
            res.append(c)
    return res
