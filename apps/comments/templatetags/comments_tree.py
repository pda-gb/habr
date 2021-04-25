from django.template import Library, Template, Context
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
    comment_div = """
    {% load static %}
    <li class="li-reply-comment">
        <div class="main-comment-section col-md-12">
            <div>
                <a href="#" class="post-author comment-author">
                    <img src="/static/img/avatar.jpg" alt=""/>
                    <small>{{author}}</small>
                </a>
                <span>{{timestamp}}</span>
            </div>
            <div class="comment-text">
                <div>{{text}}</div>
            </div>
            <span class='reply reply-comment' data-id="{{id}}" "data-prent={{parent_id}}>Ответить</span>
            <form action="#" method="POST" class="comment-form form-group" id="form-{{id}}" style="display:none;">
                <textarea type="text" class="form-control text-area-comment-reply" name="comment-text"></textarea><br>
                <input type="submit" class="btn btn-primary submit-reply" data-id="{{id}}" data-submit-reply="{{parent_id}}" value="отправить"></input>
            </form>
            <div class="post-status">
                {% if liked is True %}
                    <img src="{% static 'svg/like(filled).svg' %}" alt="" id="like-{{id}}" class="comment_like"/>
                {% else  %}
                    <img src="{% static 'svg/like.svg' %}" alt="" id="like-{{id}}" class="comment_like"/>
                {% endif %}
                <small class="green" id="likes{{id}}">{{ likes }}</small>
                {% if disliked is True %}
                    <img src="{% static 'svg/dislike(filled).svg' %}" alt="" id="dislike-{{id}}" class="comment_dislike"/>
                {% else %}
                    <img src="{% static 'svg/dislike.svg' %}" alt="" id="dislike-{{id}}" class="comment_dislike"/>
                {% endif %}
                <small class="red" id="dislikes{{id}}">{{ dislikes }}</small>
            </div>
        </div>
    </li>
    """
    template = Template(comment_div)
    i = ""
    for comment in comments_list:
        i += template.render(Context(comment))

        if comment.get("children"):
            i += comments_filter(comment["children"])
    return mark_safe(res.format(i))
