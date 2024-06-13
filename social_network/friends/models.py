from django.db import models
from django.forms import ValidationError
from social_network.users.models import User
from django.utils import timezone
from social_network.mixins import TimestampMixin
from django.utils.translation import gettext_lazy as _
from social_network.friends.exceptions import AlreadyFriendsError, AlreadyExistsError

# Create your models here.
class FriendshipManager(models.Manager):
    """ Friendship manager """
    def get_friend_requests(self, user):
        """ Return a list of friendship requests user got """
        pen_req = list(FriendshipRequest.objects.select_related("to_user", "from_user").filter(to_user=user, status="pending").all())
        return pen_req
    
    def friends(self, user):
        """ Return a list of all friends """
        qs = (
            Friend.objects.select_related("from_user", "to_user")
                .filter(to_user=user)
                .all()
        )
        friends = [u.from_user for u in qs]

        return friends
    
    def are_friends(self, user1, user2):
        """ Are these two users friends? """
        try:
            Friend.objects.get(to_user=user1, from_user=user2)
            return True
        except Friend.DoesNotExist:
            return False
        except Exception as e:
            return False
        
    def add_friend(self, from_user, to_user, message=None):
        """ Create a friendship request """
        if from_user == to_user:
            raise ValidationError("Users cannot be friends with themselves")

        if self.are_friends(from_user, to_user):
            raise AlreadyFriendsError("Users are already friends")

        if FriendshipRequest.objects.filter(from_user=from_user, to_user=to_user, status="pending").exists():
            raise AlreadyExistsError("This user already requested friendship from you.")

        if FriendshipRequest.objects.filter(from_user=to_user, to_user=from_user, status="pending").exists():
            raise AlreadyExistsError("You already requested friendship from this user.")

        if message is None:
            message = ""

        frd_req, created = FriendshipRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user
        )

        if created is False:
            if frd_req.status == "rejected":
                raise  AlreadyExistsError("Friendship Rejected By User")
            raise AlreadyExistsError("Friendship already requested")

        if message:
            frd_req.message = message
            frd_req.save()

        return frd_req
    
class FriendshipRequest(TimestampMixin):
    """ Model to represent friendship requests """

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_friend_requests",
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_friend_requests",
    )

    message = models.TextField(_("Message"), blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending", null=True)

    objects = FriendshipManager()

    class Meta:
        verbose_name = _("Friendship Request")
        verbose_name_plural = _("Friendship Requests")
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"User #{self.from_user_id} friendship requested #{self.to_user_id}"
    
    def accept(self):
        """ Accept this friendship request """
        Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
        Friend.objects.create(from_user=self.to_user, to_user=self.from_user)
        
        self.delete()

        # Delete any reverse requests
        FriendshipRequest.objects.filter(
            from_user=self.to_user, to_user=self.from_user
        ).delete()

        return True

    def reject(self):
        """ Reject this friendship request """
        self.status = "rejected"
        self.save()
        return True

    def cancel(self):
        """ cancel this friendship request """
        self.delete()
        return True


class Friend(TimestampMixin):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Friend")
        verbose_name_plural = _("Friends")
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"User #{self.to_user_id} is friends with #{self.from_user_id}"

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super().save(*args, **kwargs)