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
    i = ""
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
             """.format(
            id=comment["id"],
            author=comment["author"],
            timestamp=comment["timestamp"],
            text=comment["text"],
            parent_id=comment["parent_id"],
        )

        if comment.get("children"):
            i += comments_filter(comment["children"])
    return mark_safe(res.format(i))
