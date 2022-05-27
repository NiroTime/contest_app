from users.models import UserActions


def action_collect(user, description, action_url):
    action = UserActions(
        user=user,
        description=description,
        action_url=action_url,
    )
    action.save()


def uniq_action_collect(user, description, action_url):
    action = UserActions.objects.filter(
        user=user,
        description=description,
        action_url=action_url,
    ).first()
    if not action:
        action = UserActions(
            user=user,
            description=description,
            action_url=action_url,
        )
        action.save()
