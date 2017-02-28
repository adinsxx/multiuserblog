from base_handler import BaseHandler
import webapp2
from models import Post, User, Comment


class PostHandler(BaseHandler):
    def render_posts(self, **params):
        if "user_posts" in params:
            posts = params['user_posts']
        else:
            posts = Post.get_all()

        rendered_posts = ""
        for post in posts:
            rendered_posts += self.render_post(post, **params)

        self.render("blog/blog.html", rendered_posts=rendered_posts)

    def render_post(self, post, **params):
        if "comment_to_edit" in params:
            rendered_comment = self.render_comments(
                post=post, comment_to_edit=params['comment_to_edit'])
        else:
            rendered_comments = self.render_comments(
                post=post, comment_to_edit=None)

        return self.render_str("blog/singlepost.html",
                               p=post,
                               comments=rendered_comments)

    def render_comments(self, post, comment_to_edit=None):
        rendered_comments =
        for comment in post.comments:
            if (comment_to_edit and
                    comment.get_id() == comment_to_edit.get_id()):
                rendered_comments += self.render_str(
                    "blog/editcomment.html", comment=comment_to_edit)
            else:
                rendered_comments += self.render_str(
                    "blog/singlecomment.html", p=post, comment=comment)
            return rendered_comments

class BlogHandler(PostHandler):
    def get(self):
        self.render_posts()

class UserPostHandler(PostHandler):
    def get(self):
        user_posts = Post.get_by_user(self.user.get_id())
        self.render_posts(user_posts=user_posts)

class AddPostHandler(BaseHandler):
    def get(self):
        if self.user:
            self.render("blog/addpost.html")
        else:
            self.redirect("/login")

    def post(self):
        post_title = self.request.get("post_title")
        post_content = self.request.get("post_content")
        param_list = dict(post_title=post_title, post_content=post_content)
        any_error = False

        if not post_title:
            param_list['title_error'] = "Missing title"
            any_error = True
        if not post_content:
            param_list['content_error'] = "Missing content"
            any_error = True

        if any_error:
            self.render("blog/addpost.html", **param_list)
        else:
            p = Post.add_post(post_title, post_content, self.user)
            self.redirect('/blog/%s' % str(p.key().id()))

class SinglePostHandler(PostHandler):
    def get(self, post_id):
        single_post = self.render_post(Post.by_id(int(post_id)))
        self.render("blog/permalink.html",
                    single_post=single_post)

class EditPostHandler(BaseHandler):
    def get(self, post_id):
        post = Post.by_id(int(post_id))

        if self.user and post.author.get_id() == self.user.get_id():
            post.content = post.content.replace('<br>', '\n')
            self.render("/blog/editpost.html", post=post)
        else:
            self.render("/base.html", error="Not allowed to edit post.")

    def post(self, post_id):
        post = Post.by_id(int(post_id))
        post_title = self.request.get("post_title")
        post_content = self.request.get("post_content")
        param_list = dict(post=post, post_title=pot_title,
                          post_content=post_content)
        any_error = False

        if not post_title:
            param_list['title_error'] = "No title!"
            any_error = True
        if not post_content:
            param_list['content_error'] = "No content!"
            any_error = True

        if any_error:
            self.render("blog/editpost.html", **param_list)
        else:
            p = Post.update_post(int(post_id), post_title, post_content)
            self.redirect('/blog/%s' % str(p.get_id()))

class LikePostHandler(BaseHandler):
    def get(self, post_id):
        Post.add_like(int(post_id), self.user.get_id())
        self.redirect('/blog')

class DeletePostHandler(BaseHandler):
    def get(self, post_id):
        post = Post.by_id(int(post_id))
        if self.user and post.author.get_id() == self.user.get_id():
            Post.delete_post(post_id)
            self.redirect('/blog')
        else:
            self.render("/base.html", error="Not allowed to delete post.")


#############for the comments##############

class PostCommentsHandler(PostHandler):
    def get(self, post_id):
        pass
    
    def post(self, post_id):
        comment_content = self.request.get("comment_content")
        Post.add_comment(int(post_id), int(
            self.user.get_id()), comment_content)
        self.redirect("/blog/" + post_id + "/comments")


class CommentEditHandler(PostHandler):
    def get(self, post_id, comment_id):
        post = Post.by_id(int(post_id))
        comment = Comment.by_id(int(comment_id)
        if self.user and self.user.get_id() == comment.user.get_id():
            self.render_posts(comment_to_edit=comment, post_id_comments=post_id)

        else:
            self.render("/base.html", error="Not allowed to edit comment.")

    def post(self, post_id, comment_id):
        comment_content = self.request.get("comment_content")
        comment = Comment.by_id(int(comment_id))
        comment.set_content(comment_content)
        self.redirect("/blog/" + post_id + "/comments")

class CommentDeleteHandler(BaseHandler):
    def post(self, post_id, comment_id):
        comment = Comment.by_id(int(comment_id))
        if self.user and self.user.get_id() == comment.user.get_id():
            comment.delete_comment()
            self.redirect("/blog/" + post_id + "/comment")
        else:
            self.render("/base.html", error="Not allowed to delete comment.")
                                
