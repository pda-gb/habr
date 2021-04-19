from django.template import Library
from django.utils.html import mark_safe

register = Library()

@register.filter
def comments_filter(comments_list):
    res = """
            <ul style="list-style-type:none;">
                <div class="col-md-12 mt-2">
                    {}
                </div>
            </ul>
          """
    i = ''
    for comment in comments_list:
        i += """
             <li>
                <div class="main-comment-section">
                    <div class="m-4">
                        <a href="#" class="post-author">
                            <img src="/media/img/avatar.jpg" alt=""/>
                            <small>{author}</small>
                        </a>
                    </div>
                    <span>{timestamp}</span>
                    <div class="comment-rating">
                        <small class="text-muted">-9</small>
                    </div>
                    <div class="comment-text">
                        <p>{text} | id={id}</p>
                    </div>
                        <span class='reply' data-id="{id} "data-prent={parent_id}>Ответить</span>
                        <form action="create-child-comment/52" method="POST" class="comment-form form-group" id="form-{id}" style="display:none;">
                            <textarea type="text" class="form-control" name="comment-text"></textarea><br>
                            <input type="submit" class="btn btn-primary submit-reply" data-id="{id}" data-submit-reply="{parent_id}" value="отправить"></input>
                        </form>
                    </div>
                </div>    
             </li>
             """.format(id=comment['id'], author=comment['author'], timestamp=comment['timestamp'], text=comment['text'], parent_id=comment['parent_id'] )

        if comment.get('children'):
            i += comments_filter(comment['children'])

    return mark_safe(res.format(i))


