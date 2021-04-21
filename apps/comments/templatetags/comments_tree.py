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
        <li class="li-reply-comment">
             <div class="main-comment-section col-md-12">
                <div>
                    <a href="#" class="post-author comment-author">
                        <img src="/static/img/avatar.jpg" alt=""/>
                        <small>{author}</small>
                    </a>
                    <span>{timestamp}</span>
                </div>  
                <div class="comment-text">
                    <div>{text}</div>
                </div>
                    <span class='reply reply-comment' data-id="{id} "data-prent={parent_id}>Ответить</span>
                    <form action="#" method="POST" class="comment-form form-group" id="form-{id}" style="display:none;">
                        <textarea type="text" class="form-control text-area-comment-reply" name="comment-text"></textarea><br>
                        <input type="submit" class="btn btn-primary submit-reply" data-id="{id}" data-submit-reply="{parent_id}" value="отправить"></input>
                    </form>
            </div>        
        </li>
             """.format(id=comment['id'],
                        author=comment['author'],
                        timestamp=comment['timestamp'],
                        text=comment['text'],
                        parent_id=comment['parent_id']
                        )

        if comment.get('children'):
            i += comments_filter(comment['children'])
    print(mark_safe(res.format(i)))
    return mark_safe(res.format(i))


'''
 <div class="comment-row">
                    <h2 class="mb-4">Комментарии</h2>
                    <hr/>
                    <div class="m-4">
                        <div>
                            <a href="#" class="post-author">
                                <img src="{% static 'img/avatar.jpg' %}" alt=""/>
                                Username
                            </a>
                            <span>сегодня в 13:00</span>
                            <div class="comment-rating">
                                <a href="#"><img src="{% static 'svg/like.svg' %}" alt=""/></a>
                                <small class="text-muted">-9</small>
                                <a href="#"><img src="{% static 'svg/dislike(filled).svg' %}" alt=""/></a>
                            </div>
                        </div>
                        <div class="comment-text">
                            <div>Прочитал, ничего не понял, гугл переводчик тож тупит</div>
                        </div>
                    </div>
'''